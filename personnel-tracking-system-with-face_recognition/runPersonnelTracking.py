
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2

import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,qApp, 
                             QToolTip, QMessageBox, QLabel)
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

import winsound


import face_recognition

import numpy as np
import os

import datetime


import tensorflow
from tensorflow.keras.preprocessing.image import img_to_array
from face_recognition.face_recognition_cli import image_files_in_folder

import cvlib as cv

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import unittest

import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
    
class Tests(unittest.TestCase):
      def test(self):                                  #test method
          self.assertEqual(Work.face_encodings,Work.face_locations)
               
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.showFullScreen()
        
        
        #MainWindow.setStyleSheet("QWidget#centralwidget{background-color: rgb(85, 170, 127);}\n""")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # KAMERANIN YERLEŞTİĞİ ORTAM
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 100, 1020+240, 720))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label.setText("")
        self.label.setObjectName("label")
        #self.assertEqual(self.form.label.text(), "default")
        
        # START BUTTON
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1020+120+400-170+20, 120, 150, 60))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("font:20px;\n""border-radius:20px;\n""background-color: gray;\n""\n""")
        self.pushButton_2.setObjectName("pushButton_2")
        
        # Admin Panel
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1020+120+400+170+20, 120, 150, 60))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("font:20px;\n""border-radius:20px;\n""background-color: gray;\n""\n""")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.adminpanel)
        
        
        # EXİT
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1020+120+400+20, 120, 150, 60))
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("font:20px;\n""border-radius:20px;\n""background-color: gray;\n""\n""")
        self.pushButton_4.setObjectName("pushButton_4")
        
        # KİŞİ ÇIKTISI
        
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(1020+430, 240+120, 360, 360))
        #self.photo.setText("")
        #self.photo.setPixmap(QtGui.QPixmap("000010.jpg"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.photo.setStyleSheet("border :7px solid black;")
        
        # BAŞARILI GİRİŞ LABEL
        
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1020+430, 140, 360, 360))
        self.label_5.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";")
        self.label_5.setObjectName("label_5")
        
        # BAŞARILI GİRİŞ İSMİ LABEL
        
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1020+430, 580, 360, 360))
        self.label_6.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";")
        self.label_6.setObjectName("label_6")
        
        # GİRİŞ SAATİ İÇİN LABEL
        
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1020+430, 650, 360, 360))
        self.label_7.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";")
        self.label_7.setObjectName("label_7")
        
        
        # UST LABEL
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120+510, 40, 720,  640))
        self.label_2.setStyleSheet("font: 25pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")

        
        # ALT LABEL
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100,720+100, 1020+240, 180))
        self.label_3.setStyleSheet("background-color: gray;\n""font: 36pt \"MS Shell Dlg 2\";"
 
                        "color: dark;")
        self.label_3.setObjectName("label_3")
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        

        self.pushButton_2.clicked.connect(self.start_video)
        self.pushButton_4.clicked.connect(self.stop_video) 
        
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    
    def start_video(self):
        self.label.isEnabled()
        self.Work = Work()
        self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)

        
    def stop_video(self):
        self.Work = Work()
        self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)
        self.label.setDisabled(True)

        
        
    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))
        
    
    def adminpanel(self):                                             
        self.w = AdminPanel()
        self.w.show()
        self.hide()
        


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yüz Tanıma ile Personel Takip Sistemi"))
        self.pushButton_2.setText(_translate("MainWindow", "Başla"))
        self.pushButton_3.setText(_translate("MainWindow", "Yönetici Paneli"))
        self.pushButton_4.setText(_translate("MainWindow", "Durdur"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Yüz Tanıma için Sistemi Başlatınız.</p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Son Başarılı Giriş</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"></p></body></html>"))




    

class AdminPanel(QDialog):             
    def __init__(self):
        super().__init__()
        # setting window title
        self.setWindowTitle("Yönetici Paneli")
  
        # setting geometry to the window
        self.setGeometry(1020+400, 240, 400, 800)
  
        # creating a group box
        self.formGroupBox = QGroupBox("Yönetici Girişi Yapınız")
  
        # creating spin box to select age
        self.ageSpinBar = QSpinBox()
  
        # creating combo box to select degree
        self.degreeComboBox = QComboBox()
  
        # adding items to the combo box
        self.degreeComboBox.addItems(["BTech", "MTech", "PhD"])
  
        # creating a line edit
        self.nameLineEdit = QLineEdit()
  
        # calling the method that create the form
        self.createForm()
  
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
  
        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)
  
        # adding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)
  
        # creating a vertical layout
        mainLayout = QVBoxLayout()
  
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
  
        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)
  
        # setting lay out
        self.setLayout(mainLayout)
        
            # get info method called when form is accepted
    def getInfo(self):
      
        # printing the form information
        print("Person Name : {0}".format(self.nameLineEdit.text()))
        print("Degree : {0}".format(self.degreeComboBox.currentText()))
        print("Age : {0}".format(self.ageSpinBar.text()))
      
        # closing the window
        self.close()
      
    # creat form method
    def createForm(self):
      
        # creating a form layout
        layout = QFormLayout()
      
        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Name"), self.nameLineEdit)
      
        # for degree and adding combo box
        layout.addRow(QLabel("Degree"), self.degreeComboBox)
      
        # for age and adding spin box
        layout.addRow(QLabel("Age"), self.ageSpinBar)
      
        # setting layout
        self.formGroupBox.setLayout(layout)
        
        """
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                     'All Files (*.*)')
        if path != ('', ''):
            print(path[0])
        """

class Work(QThread):
    
    Imageupd = pyqtSignal(QImage)
    
    face_locations = []
    face_encodings = []
    

        
    def run(self):
        self.hilo_corriendo = True
        video_capture = cv2.VideoCapture(0)
        

        model = tensorflow.keras.models.load_model('masknet.h5')

        classes = ['mask','nonmask']

        #i = 0

        known_face_encodings = []
        known_face_names = []
        train_dir = "person_images"

        def person_image_search(train_dir,known_face_encodings,known_face_names):
            for class_dir in os.listdir(train_dir):
                    if not os.path.isdir(os.path.join(train_dir, class_dir)):
                        continue
            
                    for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
                        image = face_recognition.load_image_file(img_path)
                        image_face_encoding = face_recognition.face_encodings(image)[0]
                        known_face_encodings.append(image_face_encoding)
                        
                        files = open(img_path[:-4]+"_info.txt","r",encoding="utf-8")
                        files_read = files.read()
                        known_face_names.append(files_read)

               
        person_image_search(train_dir,known_face_encodings,known_face_names)


        # Initialize some variables
        face_locations = []
        face_encodings = []
        
        
        class Tests(unittest.TestCase):
            def test(self):                                  #test method
               self.assertEqual(face_loactions,face_encoding)
        
        
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            
            
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            title = 0
            #label = ""

            status2, frame2 = video_capture.read()
            face, confidence = cv.detect_face(frame2)
            
            for idx, f in enumerate(face):
              
                (startX, startY) = f[0], f[1]
                (endX, endY) = f[2], f[3]
                
                #cv2.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
                #face_crop_title = np.copy(frame[startY:endY,startX:endX])
                face_crop = np.copy(frame[startY:endY,startX:endX])
                if (face_crop.shape[0]) < 10 or (face_crop.shape[1]) < 10:
                    continue
                face_crop = cv2.resize(face_crop, (128,128))
                face_crop = face_crop.astype("float") / 255.0
                face_crop = img_to_array(face_crop)
                face_crop = np.expand_dims(face_crop, axis=0)

                conf = model.predict(face_crop)[0]
                idx = np.argmax(conf)
    
                title = conf[idx]
                
                
            if title==0:
                output = "Lütfen Kameraya Yaklaşınız."
                #cv2.putText(frame, output, (450,700),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,255,0), 2)
                _translate = QtCore.QCoreApplication.translate
                ui.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">"+output+"</p></body></html>"))
                #f = open("kayit.txt", "a")
                #f.write(output+"\n")
                face_names = []
            
            elif process_this_frame == True and title<0.95:
                output = "Lütfen Maskenizi Takınız."
                #cv2.putText(frame, output, (450,700),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,0,255), 2)
                _translate = QtCore.QCoreApplication.translate
                ui.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">"+output+"</p></body></html>"))
                #f = open("kayit.txt", "a")
                #f.write(output+"\n")
                face_names = []

            # Only process every other frame of video to save time
            elif process_this_frame == True and title>0.95:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Bilinmeyen Kisi"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        ui.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">"+name+" Giriş Yapabilirsin.</p></body></html>"))
                    face_names.append(name)


            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
                if(name != "Bilinmeyen Kisi"):
                    ui.photo.setPixmap(QtGui.QPixmap("person_images/"+name+"/"+name+".jpg"))
                    

                    ui.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">"+name+"</p></body></html>"))
                    print(name)
                    an = datetime.datetime.now()
                    tarih = datetime.datetime.strftime(an, '%c')
                    ui.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">"+tarih+"</p></body></html>"))
                    winsound.Beep(1000, 100) 
                    f = open("kayit.txt", "a")
                    f.write(name+"\n")
                    
                

            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = Image
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
                pic = convertir_QT.scaled(1020+120, 720, Qt.KeepAspectRatio)
                self.Imageupd.emit(pic)
            
            
            # Display the resulting image
            #cv2.imshow('Pilot Uygulama', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        """
        cap = cv2.VideoCapture(0)
        while self.hilo_corriendo:
            ret, frame = cap.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(Image, 1)
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
                pic = convertir_QT.scaled(320, 240, Qt.KeepAspectRatio)
                self.Imageupd.emit(pic)
        """
        
                 
                           
    def stop(self):
        self.hilo_corriendo = False
        self.quit()

if __name__ == "__main__":
    import sys
    unittest.main()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
