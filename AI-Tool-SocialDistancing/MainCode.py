# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:25:54 2020

@author: SHUKLA
"""
from PyQt5.QtWidgets import QApplication, QFileDialog,QMainWindow
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, Qt,QCoreApplication
from PyQt5.QtGui import QPixmap,QImage

import numpy as np
import cv2

import qimage2ndarray
from UI_Maincode import Ui_MainWindow
from  code_logic import yolo
#import psutil

class ProcessingThread(QThread):
    UpdateSignal = pyqtSignal(QImage,QImage,int,int,int,int)
    
    def __init__(self,media_path):
        QThread.__init__(self)
        self.flag = False
        self.media_path = media_path
       
    def run(self):
        cap = cv2.VideoCapture(self.media_path)
        self.flag = True
        while self.flag:
            ret, image = cap.read()
            if ret:
                frame,frm,total_p, low_risk_p, high_risk_p, safe_p=yolo(image)
                qtimg = qimage2ndarray.array2qimage(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
                sqtimg = qimage2ndarray.array2qimage(cv2.cvtColor(frm,cv2.COLOR_BGR2RGB))
                self.UpdateSignal.emit(qtimg,sqtimg,total_p, low_risk_p, high_risk_p, safe_p)   
        cap.release()
        
    def stop(self):
        self.flag = False



class MainCode(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        
        
        self.actionVideo.triggered.connect(self.OpenFileFormatVideo)
        self.actionImage.triggered.connect(self.OpenFileFormatImage)
        self.actionCam_Feed.triggered.connect(self.OpenFileFormatWebcam)
        self.pushButton_img.clicked.connect(self.OpenFileFormatImage)
        self.pushButton_vid.clicked.connect(self.OpenFileFormatVideo)
        self.pushButton_Link.clicked.connect(self.OpenFileFormatWebcam)
        
    
    def releaseFrame(self):
        self.thread.stop()
        self.thread.terminate # try intechanginh posritions
          
    def ThreadFunc(self,media_path):
        self.thread = ProcessingThread(media_path)
        self.pushButton_start.clicked.connect(self.thread.start)
        self.thread.UpdateSignal.connect(self.img_Qpixmap)
        self.pushButton_stop.clicked.connect(self.releaseFrame)
        
    @pyqtSlot(QImage,QImage,int,int,int,int)     
    def img_Qpixmap(self,qtimg,sqtimg,total_p, low_risk_p, high_risk_p, safe_p):
        pixmap_Frm = QPixmap.fromImage(qtimg)
        #print(pixmap_Frm.size())
        pixmap_Scld = pixmap_Frm.scaled(1070, 615, Qt.KeepAspectRatio) if pixmap_Frm.width()>1065 and pixmap_Frm.height()>615 else pixmap_Frm
        #pixmap_Scld = pixmap_Frm.scaled(1070, 615, Qt.KeepAspectRatio)
        self.label_3_MediaFrame.setPixmap(pixmap_Scld)
        self.Total_lcdNumber_2.setProperty("intValue", total_p)
        self.safe_lcdNumber_4.setProperty("intValue", safe_p)
        self.Low_lcdNumber_3.setProperty("intValue", low_risk_p)
        self.High_lcdNumber.setProperty("intValue", high_risk_p)
        if type(sqtimg) == QImage :
            spixmap_Frm = QPixmap.fromImage(sqtimg)
            pixmap_small = spixmap_Frm.scaled(251, 251, Qt.KeepAspectRatio)
            self.label_2_StreetView.setPixmap(pixmap_small)
         
    def OpenFileFormatImage(self):
        filename = QFileDialog.getOpenFileName(None, "Select Image File", "", "Images (*.png *.xpm *.jpg)")#,options=QFileDialog.DontUseNativeDialog
        path = filename[0]
        image = cv2.imread(path)
        image = cv2.resize(image,(640,800),interpolation = cv2.INTER_AREA ) if image.shape[0]>1350 and image.shape[1]>700 else image
        frame,_,total_p, low_risk_p, high_risk_p, safe_p=yolo(image)
        qtimg = qimage2ndarray.array2qimage(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        self.img_Qpixmap(qtimg,_,total_p, low_risk_p, high_risk_p, safe_p)
        
    def OpenFileFormatVideo(self):
        filename = QFileDialog.getOpenFileName(None, "Select Image File", "", "Video (*.mp4 *.avi *.flv)")#,options=QFileDialog.DontUseNativeDialog
        path = filename[0]
        self.ThreadFunc(path)
        
    def OpenFileFormatWebcam(self):
        path = 0
        self.ThreadFunc(path)
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    #app.setStyle('Fusion')
    Form = MainCode()
    Form.show()
    sys.exit(app.exec_())
        