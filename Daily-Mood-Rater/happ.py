# Credits
# "faces" icon created by Vector Valley, PK from the Noun Project
# https://thenounproject.com/term/faces/4127357/

import sys, mood_db, json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QPalette, QColor 
from interface import Ui_MainWindow
from pathlib import Path

cur_dir = Path.cwd()
with open(cur_dir / "src/config.json", "r", encoding="utf-8") as cfg:
    config = json.load(cfg)
    theme = config["theme"]
    icon = config["icon"][theme]

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        print("\033[1;35;40mStarting:\033[1;32;40m Daily Mood Rater\033[0;37;40m")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.icon = QIcon((cur_dir / f"src/{icon}").as_posix())

        # Icon customization: https://thenounproject.com/term/faces/4127357/
        self.setWindowIcon(self.icon)
        
        self.setStatusTip(datetime.now().strftime("%A, %d %B, %Y"))

        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")
        self.ui.textEdit_description.setToolTip("You can describe how you feel")

        ### Functionality ###

        # Menubar
        ## Theme
        self.ui.actionDefault.triggered.connect(lambda: self.change_theme("default"))
        self.ui.actionDark.triggered.connect(lambda: self.change_theme("dark"))

        # Populate ComboBox
        self.comboBox_populate()

        # Update label when slider moves
        self.ui.slider_mood.sliderMoved.connect(self.label_update)

        # If checkbox is changed, either enable or disable text area
        self.ui.checkBox_mood.stateChanged.connect(self.enable_text)
        
        # Send slider position (rating) and description to database
        self.ui.btn_save.clicked.connect(self.save_to_db)

        # Create a graph from saved data
        self.ui.btn_graph.clicked.connect(self.show_graph)

    def comboBox_populate(self):
        self.current_months = [month[0] for month in mood_db.current_months()]
        if self.current_months:
            self.ui.comboBox_date.addItems(self.current_months)
            self.ui.comboBox_date.setCurrentIndex(self.current_months.index(str(datetime.now())[:7]))

    def label_update(self):
        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")

    def enable_text(self, value):
        if value == 2:
            self.ui.textEdit_description.setEnabled(True)
        else:
            self.ui.textEdit_description.clear()
            self.ui.textEdit_description.setDisabled(True)

    def save_to_db(self):
        textedit = self.ui.textEdit_description.toPlainText()
        description = textedit if bool(self.ui.textEdit_description.toPlainText()) else " "
        save = mood_db.save_values(
                self.ui.slider_mood.sliderPosition(),
                description
            )

        if save != 1:
            # Cannot save because an entry already exists
            # A prompt to ask whether user wants to update current entry or cancel
            msg = QMessageBox()

            msg.setWindowTitle("Overwrite current entry?")
            msg.setWindowIcon(self.icon)
            msg.setText(f"There is already an existing entry for today. Would you like to overwrite it?")
            msg.setDetailedText(f"Mood Rating: {save[0]}\nDescription: {save[1]}\nDate: {save[2]}")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)

            response = msg.exec_()

            # If user clicks OK, overwrite the current entry
            if response == QMessageBox.Ok:
                try:
                    mood_db.update_values(
                        self.ui.slider_mood.sliderPosition(),
                        description
                    )
                    self.ui.statusbar.showMessage("Entry overwrite was successful!", 4000)
                except:
                    self.ui.statusbar.showMessage("Error: Entry overwrite was unsuccessful!", 4000)
            elif response == QMessageBox.Cancel:
                pass
            else:
                raise Exception(f"Unhandled Exception! Something went wrong.\nQMessageBox responded with: {response}\nExpected: QMessageBox.Ok or QMessageBox.Cancel\n\033[1;37;40mPlease let me know about this error so I can work on it ^^\033[0;37;40m")
        else:
            msg = QMessageBox()

            msg.setWindowTitle("Success!")
            msg.setWindowIcon(self.icon)
            msg.setText("Your mood rating for today was successfully saved into the database.")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.exec_()
            if not self.current_months:
                self.comboBox_populate()

    def show_graph(self):
        # Using a separate window to show Matplotlib Graph, Embedded into a QWidget window
        if self.current_months:
            import mood_graph
            self.graph = mood_graph.AppWindow(self.ui.comboBox_date.currentText())
            self.graph.show()
        else:
            msg = QMessageBox()

            msg.setWindowTitle("Error!")
            msg.setWindowIcon(self.icon)
            msg.setText("There are currently no records available in the database.\nStart saving your mood ratings and they will show up the next time you click 'Show Graph' button")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.exec_()

    def change_theme(self, theme):
        with open(cur_dir / "src/config.json", "r", encoding="utf-8") as cfg:
            config = json.load(cfg)

        config["theme"] = theme

        with open(cur_dir / "src/config.json", "w", encoding="utf-8") as cfg:
            config = json.dump(config, cfg)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # set stylesheet
    if theme == "default":
        app.setStyle("Fusion")
    elif theme == "dark":
        from PyQt5.QtCore import QFile, QTextStream
        import src.breeze_resources
        file = QFile(":/dark/stylesheet.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
    else:
        print("No proper theme selected.")

    win = Application()
    win.show()
    sys.exit(app.exec_())
