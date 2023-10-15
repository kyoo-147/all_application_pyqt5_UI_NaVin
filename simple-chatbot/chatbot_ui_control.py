# Interfaz grafica con PyQt5
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication, Qt, QThread
from PyQt5.QtGui import QMovie

# Engine del Chatbot
import chatbot_back as eng

# Reconocimiento y sintesis de voz
import speech_recognition as sr
import pyttsx3

qtcreator_file = "chatbot_ui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

errors = ['Mi motor de reconocimiento de voz no te ha comprendido.',
          'Error al conectarme con Google.']

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.send_btn.clicked.connect(self.send_msg)
        self.text_input.returnPressed.connect(self.send_msg)

        self.voice_rec = False
        self.menu_voice_rec.changed.connect(self.voice_rec_changed)
        self.micro_btn.clicked.connect(self.rec)
        self.menu_cerrar.triggered.connect(QCoreApplication.instance().quit)

        eng.LoadEngine()
        self.historial.appendPlainText('BOT >> Hola. Hazme una pregunta.\n')

    # Reconocer activacion/desactivacion del rec y sint de voz
    def voice_rec_changed(self):
        self.voice_rec = self.voice_rec = self.menu_voice_rec.isChecked()

    # Enviar un mensaje al chatbot a traves de texto
    def send_msg(self):
        if bool(self.text_input.text().strip()):
            user_msg = self.text_input.text()
            new_text = 'TÚ >> ' + user_msg + '\n'
            self.text_input.setText('')
            self.historial.appendPlainText(new_text)
            self.process_msg(user_msg)
        else:
            self.text_input.setText('')

    # Procesar mensaje con el engine del chatbot y mostrar respuesta
    def process_msg(self, user_msg):
        response = ''

        # Proesado del mensaje
        if eng.thanks(user_msg) != None:
           response = eng.thanks(user_msg)
        else:
            if eng.saludos(user_msg) != None:
                response = eng.saludos(user_msg)

            else:
                response = eng.response(user_msg)

        # Mostrar respuesta del chatbot
        self.historial.appendPlainText("BOT >> " + response.capitalize() + '\n')
        self.speak(response)

    # Iniciar hilo para el reconocimiento de voz
    def rec(self):
        self.recorder = Rec()
        self.recorder.started.connect(self.lanzar_dialog)
        self.recorder.finished.connect(self.process_voice)

        self.recorder.start()

    '''
    Lanzar dialogo de espera para la escucha y reconocimiento de voz
    Mantiene el hilo principal en suspension temporal hasta que se termine el
    reconocimiento a no ser que se cierre el dialogo
    '''
    def lanzar_dialog(self):
        self.diag = QtWidgets.QDialog()
        self.diag.loading = QtWidgets.QLabel()
        self.diag.setWindowTitle("En escucha...")
        self.diag.setWindowModality(Qt.ApplicationModal)
        self.diag.setWindowFlag(Qt.FramelessWindowHint)

        self.diag.layout = QtWidgets.QVBoxLayout(self.diag)
        self.diag.layout.setContentsMargins(0, 0, 0, 0)
        self.diag.layout.addWidget(self.diag.loading)

        movie = QMovie("listening.gif")
        self.diag.loading.setMovie(movie)
        movie.start()

        if self.diag.exec() == QtWidgets.QDialog.Rejected:
            if self.recorder.isRunning():
                self.recorder.terminate()

    # Mostrar el resultado del reconocimiento de voz
    def process_voice(self):
        self.diag.accept()

        text = self.recorder.text

        if bool(text):
            if text in errors:
                new_text = 'BOT >> ' + text + '\n'
                self.historial.appendPlainText(new_text)
                self.speak(text)
            else:
                new_text = 'TÚ >> ' + text.capitalize() + '\n'
                self.historial.appendPlainText(new_text)
                self.process_msg(text)

    #Sintetizar la voz si esta activa la funcion
    def speak(self, response):
        if self.voice_rec:
            self.sinte = Sint()
            self.sinte.msg = response

            self.sinte.started.connect(self.toggleEnable)
            self.sinte.finished.connect(self.toggleEnable)

            self.sinte.start()
        
    def toggleEnable(self):
        self.hLay.setEnabled(not self.hLay.isEnabled())

# Hilo para reconocimiento de voz
class Rec(QThread):
    def __init__(self):
        super().__init__()
        self.text = ''

    def run(self):
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            self.text = r.recognize_google(audio, language='es')
        except sr.UnknownValueError:
            self.text = errors[0]
        except sr.RequestError:
            self.text = errors[1]


# Configuracion del sintetizador de voz
sint = pyttsx3.init()
voices = sint.getProperty('voices')
sint.setProperty('rate', 170)
sint.setProperty('voice', voices[4].id)

# Hilo para la sintesis de voz
class Sint(QThread):
    def __init__(self):
        super().__init__()
        self.msg = ''

    def run(self):
        sint.say(self.msg)
        sint.runAndWait()


#Inicio del programa
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
