# Modified by Rajat Shrivastav
# o6th March 2021
# Traffic Surviellance System GUI using AI city Challenge
# *-

from PyQt5.QtGui import QImage, QPixmap,QPalette
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer,QDate,Qt,QUrl,QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import cv2
import numpy as np
import datetime
import os
import time


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.is_paused = False

    def run(self):
        # Play the video
        if self.is_paused:
            time.sleep(0)
        else:
            cap = cv2.VideoCapture('./Video2.mp4')
            while self._run_flag:
                ret, cv_img = cap.read()
                time.sleep(0.05)
                if ret:
                    self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
            cap.release()

    def pause(self):
        self._run_flag = False
        self.wait()

    def resume(self):
        self._run_flag = True


class Ui_OutputDialog(QMainWindow):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi('./opencv_vframe.ui', self)
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        self.stop_video.clicked.connect(self.thread.pause)
        self.play_video.clicked.connect(self.thread.resume)


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.imgLabel.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640,480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)



