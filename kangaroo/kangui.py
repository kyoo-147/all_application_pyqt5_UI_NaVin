import sys
import os
import signal
import platform
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QCheckBox, QTextEdit, QFileDialog, QGroupBox,QMessageBox, QPlainTextEdit, QSizePolicy
from PyQt5.QtGui import QFont
import multiprocessing
import subprocess

mizogg = f'''

 Made by Mizogg Version 1.0  © mizogg.co.uk 2018 - 2023      {f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"}

'''

class CommandThread(QThread):
    commandOutput = pyqtSignal(str)
    commandFinished = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def run(self):
        self.process = subprocess.Popen(self.command, shell=True)
        self.process.communicate()  # Wait for the process to finish
        self.commandFinished.emit(self.process.returncode)


class ConsoleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.consoleOutput = QPlainTextEdit(self)
        self.consoleOutput.setReadOnly(True)
        self.consoleOutput.setFont(QFont("Courier"))
        self.layout.addWidget(self.consoleOutput)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.consoleOutput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    @pyqtSlot(int)
    def update_console_style(self, index):
        if index == 1:
            self.consoleOutput.setStyleSheet("background-color: white; color: purple; font-size: 14px;")
        elif index == 2:
            self.consoleOutput.setStyleSheet("background-color: black; color: green; font-size: 14px;")
        elif index == 3:
            self.consoleOutput.setStyleSheet("background-color: red; color: blue; font-size: 14px;")

    @pyqtSlot(str)
    def append_output(self, output):
        self.consoleOutput.appendPlainText(output)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("kangui.py")
        self.setGeometry(100, 100, 780, 560)
        self.process = None
        self.commandThread = None
        self.scanning = False
        self.initUI()
        
    def initUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        cpu_count = multiprocessing.cpu_count()
        self.setStyleSheet(
    """
    QMainWindow {
        background-image: url(mizogg.png);
        background-repeat: no-repeat;
        background-position: top left;
    }
    """
)
        main_layout = QVBoxLayout()
        welcome_label = QLabel('<html><b><font color="purple" size="10"> GUI Crypto Scanner</font></b></html>')
        welcome_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(welcome_label)
        line1_label = QLabel('<html><b><center><font color="purple" size="5">Kanagroo.py  </font></center></b></html>')
        main_layout.addWidget(line1_label)
        line2_label = QLabel('<html><b><center><font color="blue" size="3"> Start from a random value in the given range from min:max and search 0XFFFFFFFFFFFFFF values then again take a new random.</font><font color="green" size="3"> First Start from a random value, then go fully sequential, in the given range from min:max</font></center></b></html>')
        main_layout.addWidget(line2_label)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        self.threadLayout = QHBoxLayout()
        self.layout.addLayout(main_layout)
        self.threadGroupBox = QGroupBox(self)
        self.threadGroupBox.setTitle("Thread Configuration Start in Random/Sequence Stop or open in new Window")
        self.threadGroupBox.setStyleSheet("QGroupBox { border: 2px solid green; padding: 5px; }")

        self.threadLayout = QHBoxLayout(self.threadGroupBox)
        self.threadLabel = QLabel('<html><b><font color="green" size="2">Number of CPUS : </font></b></html>', self)
        self.threadLayout.addWidget(self.threadLabel)
        self.threadComboBox = QComboBox()
        for i in range(1, cpu_count + 1):
            self.threadComboBox.addItem(str(i))
        self.threadComboBox.setCurrentIndex(2)
        self.threadLayout.addWidget(self.threadComboBox)
        self.randomButton = QPushButton("Random", self)
        self.randomButton.setStyleSheet("color: green;")
        self.randomButton.clicked.connect(self.run_rand)
        self.threadLayout.addWidget(self.randomButton)
        self.sequenceButton = QPushButton("Sequence", self)
        self.sequenceButton.setStyleSheet("color: blue;")
        self.sequenceButton.clicked.connect(self.run_rand1)
        self.threadLayout.addWidget(self.sequenceButton)
        self.stopButton = QPushButton("Stop scanning", self)
        self.stopButton.setStyleSheet("color: red;")
        self.stopButton.clicked.connect(self.stop_exe)
        self.threadLayout.addWidget(self.stopButton)
        self.NEWButton = QPushButton("New window", self)
        self.NEWButton.setStyleSheet("color: orange;")
        self.NEWButton.clicked.connect(self.new_window)
        self.threadLayout.addWidget(self.NEWButton)
        self.layout.addWidget(self.threadGroupBox)
        
        self.prefixGroupBox = QGroupBox(self)
        self.prefixGroupBox.setTitle("Public Key Search config")
        self.prefixGroupBox.setStyleSheet("QGroupBox { border: 2px solid red; padding: 5px; }")

        prefixLayout = QHBoxLayout(self.prefixGroupBox)
        self.prefixLabel = QLabel("Public Key to search:", self)
        prefixLayout.addWidget(self.prefixLabel)
        self.prefixLineEdit = QLineEdit("02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673", self)
        prefixLayout.addWidget(self.prefixLineEdit)

        self.layout.addWidget(self.prefixGroupBox)
        self.keyspaceGroupBox = QGroupBox(self)
        self.keyspaceGroupBox.setTitle("Key Space Configuration")
        self.keyspaceGroupBox.setStyleSheet("QGroupBox { border: 2px solid green; padding: 5px; }")

        keyspaceLayout = QHBoxLayout(self.keyspaceGroupBox)
        self.keyspaceLabel = QLabel("Key Space:", self)
        keyspaceLayout.addWidget(self.keyspaceLabel)
        self.keyspaceLineEdit = QLineEdit("8000000000000000000000000000000000000000:ffffffffffffffffffffffffffffffffffffffff", self)
        self.keyspaceLineEdit.setPlaceholderText('Example range for 160 = 8000000000000000000000000000000000000000:ffffffffffffffffffffffffffffffffffffffff')
        keyspaceLayout.addWidget(self.keyspaceLineEdit)

        self.layout.addWidget(self.keyspaceGroupBox)

        self.colourLayout = QHBoxLayout()
        self.colorlable = QLabel(
            '<html><b><font color="blue" size="3"> Pick Console Colour </font></b></html>', self
        )
        self.colorlable.setAlignment(Qt.AlignRight)
        self.colorComboBox = QComboBox(self)
        self.colorComboBox.addItem("Pick Console Colour")
        self.colorComboBox.addItem("Option 1: White Background, Purple Text")
        self.colorComboBox.addItem("Option 2: Black Background, Green Text")
        self.colorComboBox.addItem("Option 3: Red Background, Blue Text")
        self.colorComboBox.currentIndexChanged.connect(self.update_console_style)
        self.colourLayout.addWidget(self.colorlable)
        self.colourLayout.addWidget(self.colorComboBox)
        self.layout.addLayout(self.colourLayout)

        self.consoleWindow = ConsoleWindow(self)
        self.layout.addWidget(self.consoleWindow)
        
        mizogg_label = QLabel(f'<html><b><font color="red" size="4">{mizogg}</font></b></html>', self)
        mizogg_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(mizogg_label)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def run_rand(self):
        command = self.construct_command("-rand")
        self.execute_command(command)

    def run_rand1(self):
        command = self.construct_command("-rand1")
        self.execute_command(command)
        
    def construct_command(self, mode):
        public_key = self.prefixLineEdit.text().strip()
        keyspace = self.keyspaceLineEdit.text().strip()
        thread_count = int(self.threadComboBox.currentText())
        command = f'python kangaroo.py -p {public_key} -keyspace {keyspace} -ncore {thread_count} {mode}'
        self.consoleWindow.append_output(command)
        return command
    
    def stop_exe(self):
        if self.commandThread and self.commandThread.isRunning():
            if platform.system() == "Windows":
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(self.commandThread.process.pid)])
            else:
                os.killpg(os.getpgid(self.commandThread.process.pid), signal.SIGTERM)
            
            self.timer.stop()
            self.scanning = False
            returncode = 'Closed'
            self.command_finished(returncode)

            
    def pop_Result(self, message_error):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message_error)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.exec_() 
        
    @pyqtSlot()
    def new_window(self):
        python_cmd = f'start cmd /c "{sys.executable}" kangui.py'
        subprocess.Popen(python_cmd, shell=True)

    @pyqtSlot()
    def execute_command(self, command):
        if self.scanning:
            return

        self.scanning = True

        if self.commandThread and self.commandThread.isRunning():
            self.commandThread.terminate()

        self.commandThread = CommandThread(command)
        self.commandThread.commandOutput.connect(self.consoleWindow.append_output)
        self.commandThread.commandFinished.connect(self.command_finished)
        self.commandThread.start()

        self.timer.start(100)  # Start the timer to update the GUI every 100 milliseconds
    
    @pyqtSlot(int)
    def command_finished(self, returncode):
        self.timer.stop()
        self.scanning = False

        if returncode == 0:
            finish_scan = "Command execution finished successfully"
            self.consoleWindow.append_output(finish_scan)
        if returncode == 'Closed':
            finish_scan = "Process has been stopped by the user"
            self.consoleWindow.append_output(finish_scan)
        else:
            error_scan = "Command execution failed"
            self.consoleWindow.append_output(error_scan)
    
    @pyqtSlot(int)
    def update_console_style(self, index):
        self.consoleWindow.update_console_style(index)
        
    def update_gui(self):
        QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
