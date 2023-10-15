
import sys
import cv2
import time
import datetime
import threading
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class MainWindow(QMainWindow):

    global frame
    global faces
    global smiles

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('mainGUI.ui', self)
        self.setFixedSize(self.size())
        self.setWindowTitle('Smile Detector with Python')

        self.lblTitle.setAlignment(Qt.AlignCenter)
        self.lblFaceDetect.setAlignment(Qt.AlignCenter)

        self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
        self.smileCascade = cv2.CascadeClassifier('data/haarcascade_smile.xml')

        self.timer = QTimer()
        self.timer.timeout.connect(self.detectFaces)
        self.btnControl.clicked.connect(self.controlTimer)

        self.Sec = 0
        self.Min = 0



    def detectFaces(self):

        ret, self.frame = self.cap.read()

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        self.faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)

        self.lblFaceDetect.setText('Face not detected')
        self.lblFaceDetect.setStyleSheet("color: red;")

        self.thread2 = threading.Thread(name='thread2', target=self.countSmiling)

        for (x, y, w, h) in self.faces:

            #cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roiGray = gray[y:y+h, x:x+w] 
            roiColor = self.frame[y:y+h, x:x+w]

            self.lblFaceDetect.setText('Face detected')
            self.lblFaceDetect.setStyleSheet("color: green;")

            self.smiles = self.smileCascade.detectMultiScale(roiGray, 1.8, 20)

            for (sx, sy, sw, sh) in self.smiles: 
                cv2.rectangle(roiColor, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

                self.thread2.start()

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        height, width, channel = self.frame.shape
        step = channel * width

        qImg = QImage(self.frame.data, width, height, step, QImage.Format_RGB888)

        self.lblVideo.setPixmap(QPixmap.fromImage(qImg))



    def countSmiling(self):

        self.Sec += 1
        self.lcdTotalTimeSmiling.display(self.Sec)
        time.sleep(1)



    def controlTimer(self):

        if not self.timer.isActive():

            self.cap = cv2.VideoCapture(0)

            self.cap.set(3,610)
            self.cap.set(4,560)

            self.timer.start(20)

            self.btnControl.setText('Stop')

        else:

            self.timer.stop()

            self.cap.release()

            self.lblFaceDetect.setText('Waiting ...')
            self.lblFaceDetect.setStyleSheet("color: black;")

            self.btnControl.setText('Start')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())