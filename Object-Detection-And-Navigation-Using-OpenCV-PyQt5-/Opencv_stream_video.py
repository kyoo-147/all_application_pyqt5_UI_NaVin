#######################################################################################################################
# Object-Detection-And-Navigation:
# Created On: 18-04-2021  Version V1.0
# Author: Aditya Shrivastava
# GitHub ID: AdityaShrivastava03
# Run command "pip install opencv"  to install opencv
# Run command "pip install pyqt5" to install pyqt5
# Application tested successfully on Web Cam and IP Cam.
########################################################################################################################
import cv2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
import sys, os
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from PyQt5.uic import loadUiType
import time


def resource_path(relative_path):
    base_path=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

FROM_CLASS,_ = loadUiType(resource_path("Opencv_stream_video.ui"))



class Main(QMainWindow, FROM_CLASS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowTitle("Display Video")
        global Area
        global DrawThreshold
        global ShowScale
        global North_X, North_Y
        global South_X, South_Y  
        global East_X, East_Y
        global West_X, West_Y
        Area = 5000
        DrawThreshold = False
        ShowScale = False
        North_X = 0 
        North_Y = 0
        South_X = 0 
        South_Y = 0  
        East_X = 0 
        East_Y = 0
        West_X = 0 
        West_Y = 0

        #1080p
        # self.disply_width = 1920
        # self.display_height = 1080

        #720p
        # self.disply_width = 1280
        # self.display_height = 720

        # #480p
        self.disply_width = 852
        self.display_height = 480

        #360p
        # self.disply_width = 480
        # self.display_height = 360

        # #240p
        # self.disply_width = 320
        # self.display_height = 240

        # #144p
        # self.disply_width = 176
        # self.display_height = 144

        # self.disply_width = 640
        # self.display_height = 480

        # create the label that holds the image
        # self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.pushButton_start.clicked.connect(self.Start)
        # Draw_lines toggle button 
        self.pushBotton_Draw_lines.toggle()
        self.pushBotton_Draw_lines.setCheckable(True)
        self.pushBotton_Draw_lines.clicked.connect(self.DrawThreshold_button_status)
        # ShowScale toggle button 
        self.pushBotton_ShowScale.toggle()
        self.pushBotton_ShowScale.setCheckable(True)
        self.pushBotton_ShowScale.clicked.connect(self.ShowScale_button_statue)

        self.pushButton_exit.clicked.connect(self.closeEvent)
        #emt signal from thread class
        self.pushButton_Apply.clicked.connect(self.Apply_settings)
        self.lineEdit_area.setText("5000")
        self.pushButton_set_area.clicked.connect(self.Set_area)
       
        self.pushButton_capture_ref.clicked.connect(self.Capture)

    def Set_area(self):
        global Area
        if not self.lineEdit_area.text() == '':
            Area = int(self.lineEdit_area.text())
        else:
            QMessageBox.about(self, 'Error', 'Fill Area')
        

    def Capture(self):
        self.thread = VideoThread()
        self.thread.Capture_ref_frame()

    def DrawThreshold_button_status(self):
        global DrawThreshold
        if self.pushBotton_Draw_lines.isChecked():
            DrawThreshold = True
            self.pushBotton_Draw_lines.setText('Threshold Disable')
        else:
            DrawThreshold = False
            self.pushBotton_Draw_lines.setText('Threshold Enable')
 
    def Apply_settings(self):
        global North_X, North_Y
        global South_X, South_Y 
        global East_X, East_Y
        global West_X, West_Y 
      
        if not (self.lineEdit_north_x.text() and self.lineEdit_north_y.text() and self.lineEdit_south_x.text() and self.lineEdit_south_y.text() and self.lineEdit_east_x.text() and self.lineEdit_east_y.text() and self.lineEdit_west_x.text() and self.lineEdit_west_y.text()) == "":
            North_X = self.lineEdit_north_x.text()
            North_Y = self.lineEdit_north_y.text()
            South_X = self.lineEdit_south_x.text()
            South_Y = self.lineEdit_south_y.text()
            East_X = self.lineEdit_east_x.text()
            East_Y = self.lineEdit_east_y.text()
            West_X = self.lineEdit_west_x.text()
            West_Y = self.lineEdit_west_y.text()
        else:
            QMessageBox.about(self, 'Error', 'Fill all details then apply')

    def ShowScale_button_statue(self):   
        global ShowScale
        if self.pushBotton_ShowScale.isChecked():
            ShowScale = True
            self.pushBotton_ShowScale.setText('Scale Disable')
        else:
            ShowScale = False
            self.pushBotton_ShowScale.setText('Scale Enable')

    def Start(self):
        try:
            # create the video capture thread
            self.thread = VideoThread()
            # connect its signal to the update_image slot
            self.thread.change_pixmap_signal.connect(self.update_image)
            # start the thread
            self.thread.start()
            # self.pushButton_start.clicked.connect(self.Start)
            
        except ConnectionError:
            self.stop()
            QMessageBox.about(self, 'Connection', 'Failed To Connect With Camera')
       
    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    #Updates the image_label with a new opencv image
    @pyqtSlot(np.ndarray)
    def update_image(self, frame1):
        qt_img = self.convert_cv_qt(frame1)
        self.image_label.setPixmap(qt_img)
        
    

    #Convert from an opencv image to QPixmap
    def convert_cv_qt(self, cv_img):
        
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
        # return QPixmap.fromImage(convert_to_Qt_format)

    
        
#####################################################################################
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    change_label_instruction = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        
        print('wait........')
        
        try:
            # For IP Cam cv2.VideoCapture('rtsp://ID:Password@IP Address/1')
            # self.cap = cv2.VideoCapture('rtsp://admin:@192.168.10.55/1')  
            # For Web Cam
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Cannot open camera")
                exit()
        except ConnectionError:
            self.stop()
            QMessageBox.about(self, 'Connection', 'Failed To Connect With Camera')


        self.Capture_ref_frame()
        
        # ret, self.frame0 = self.cap.read()
        # cv2.imwrite("Image_ref_01.jpg",self.frame0)
        # time.sleep(0.5)
        # self.frame2 = cv2.imread("Image_ref_01.jpg", cv2.IMREAD_COLOR) # frame2 capture image
        # self.Width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.Hight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


        print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))       # print frame width
        print(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))      # print frame hight

    def ShowScale(self):
        y = 0
        x = 0
        p = int(self.Width/10)
        q = int(self.Hight/10)
        
        for _ in range (10):
            # Print Scale 
            cv2.putText(self.frame1, str(x), (x, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 100), 2)
            cv2.line(self.frame1,(x,0), (x,50), (0,0,225), 2) # RED LINE 
            x = x+p
            # print(x)

        for _ in range (10):
            # Print Scale 
            cv2.putText(self.frame1, str(y), (0, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 100), 2)
            cv2.line(self.frame1,(0,y), (50,y), (0,0,225), 2) # RED LINE 
            y = y+q
            # print(y)
    # Take Reference frame without Any Object so we can compare the difference and find object
    def Capture_ref_frame(self):
        ret, self.frame0 = self.cap.read()
        cv2.imwrite("Image_ref_01.jpg",self.frame0)
        time.sleep(0.5)
        self.frame2 = cv2.imread("Image_ref_01.jpg", cv2.IMREAD_COLOR) # frame2 capture image
        self.Width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.Hight = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Capture")

    def DrawThreshold(self):
        global North_X, North_Y
        global South_X, South_Y  
        global East_X, East_Y
        global West_X, West_Y
    # North side liens
        cv2.line(self.frame1,(0,int(North_Y)+10), (int(North_X),int(North_Y)+10), (0,225,0), 2) # GREEN LINE  
        cv2.line(self.frame1,(0,int(North_Y)), (int(North_X), int(North_Y)), (0,0,225), 2) # RED LINE
        cv2.line(self.frame1,(0,int(North_Y)-10), (int(North_X),int(North_Y)-10), (0,225,0), 2) # GREEN LINE
    # South side liens 
        cv2.line(self.frame1,(0,int(South_Y)+10), (int(South_X),int(South_Y)+10), (0,225,0), 2) # GREEN LINE  
        cv2.line(self.frame1,(0,int(South_Y)), (int(South_X), int(South_Y)), (0,0,225), 2) # RED LINE
        cv2.line(self.frame1,(0,int(South_Y)-10), (int(South_X),int(South_Y)-10), (0,225,0), 2) # GREEN LINE
    # East side liens
        cv2.line(self.frame1,(int(East_X)+10,0), (int(East_X)+10,int(East_Y)), (0,225,0), 2) # GREEN LINE  
        cv2.line(self.frame1,(int(East_X),0), (int(East_X),int(East_Y)), (0,0,225), 2) # RED LINE
        cv2.line(self.frame1,(int(East_X)-10,0), (int(East_X)-10,int(East_Y)), (0,225,0), 2) # GREEN LINE 
    # West side liens
        cv2.line(self.frame1,(int(West_X)+10,0), (int(West_X)+10,int(West_Y)), (0,225,0), 2) # GREEN LINE  
        cv2.line(self.frame1,(int(West_X),0), (int(West_X),int(West_Y)), (0,0,225), 2) # RED LINE
        cv2.line(self.frame1,(int(West_X)-10,0), (int(West_X)-10,int(West_Y)), (0,225,0), 2) # GREEN LINE 
  

    def run(self):
        # capture from web cam
        global DrawThreshold
        global ShowScale
        global North_X, North_Y
        global South_X, South_Y  
        global East_X, East_Y
        global West_X, West_Y
        global Area 
        
        while self._run_flag:
            ret, self.frame1 = self.cap.read()
            frame_diff = cv2.absdiff(self.frame1, self.frame2)

            # convert foreground into GRAY
            frame_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)   

            # apply the threshold for increasing hite freground
            _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

            # assign frame2 to frame1 t continue the iteration untill all frame are read
            # frame1 = frame2
            #
            if DrawThreshold == True:
                self.DrawThreshold()
            if ShowScale == True:
                self.ShowScale()
        

        # extract the contours 
            image ,contours, hierarchy  = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
         # If error ValueError: too many values to unpack (expected 3) comment on above line and uncomment line below
            # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                # Ignore the small contours by finding area 
                # area = cv2.contourArea(c)
                # print(area)
                if cv2.contourArea(c) < Area:
                    continue
                x, y, w, h = cv2.boundingRect(c)
                # bound area for making rectangle
                # if x > 50 and x < 600 and y >100 and y < 400 :
                # # draw the bounding rectangle for all contours 
                cv2.rectangle(self.frame1, (x,y), (x+w, y+h), (255, 0 , 0), 3)
                xMid = int ((x+(x+w))/2)
                yMid = int ((y+(y+h))/2)

                xTop = int(x+w)
                yTop = int(y)
                xBot = int(x)
                yBot = int(y)
                rCent = int((y+(y+h))/2)
                lCent = int(rCent+x+w)

                # Top corners circules (Rght Left)
                cv2.circle(self.frame1, (xTop, yTop),5,(0,0,255),5)
                cv2.circle(self.frame1, (xTop, (yTop+h)),5,(0,0,255),5)

                # Bottom corners circules (Rght Left)
                cv2.circle(self.frame1, ((xTop-w), (yTop)),5,(0,0,255),5)
                cv2.circle(self.frame1, ((xTop-w), (yTop+h)),5,(0,0,255),5)

                if DrawThreshold == True:
                    # East circles B/W the lines 
                    if x < (int(East_X)-10): # and  yTop < 520: int(East_X)-10
                        cv2.putText(self.frame1, "MOVE FORWARD", (420, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    # cv2.putText(self.frame1, "MOVE FORWARD", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        
                    # West circles B/W the lines 
                    if (x+w) > (int(West_X)+10): # and xBot < 340:
                        cv2.putText(self.frame1, "MOVE BACK", (420, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        # cv2.putText(self.frame1, "Bottom On The Line", (x, y + (h+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    #                     GPIO.output(LeftPin, GPIO.HIGH)
    #                 else:
    #                     GPIO.output(LeftPin, GPIO.LOW)
                        
                    # North circles B/W the lines 
                    if y < (int(North_Y)-10) :
                        cv2.putText(self.frame1, "MOVE LEFT", (420, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        #cv2.putText(self.frame1, "Right On The Line", (x-240, rCent), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (230, 110, 30), 2)
                    
                    # South circles B/W the lines 
                    if (y+h) > (int(South_Y)+10) : #and (yTop+w) < 410:
                        cv2.putText(self.frame1, "MOVE RIGHT", (420, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        #cv2.putText(self.frame1, "Left On The Line", (x+150, rCent), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (230, 110, 30), 2)


                    # # Top and Bottom circles B/W the lines print capture
                    # if ((x > int(East_X) and ((x+w) < int(West_X))) and ((y < int(North_Y)) and ((y+h)> int(South_Y)))):
                    #     cv2.putText(self.frame1, "**** GOOD JOB ****", (350, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)

                
            
            # Display thresh resulting frame1 farm2 diff in gray
            # cv2.imshow('Foreground', frame_diff)   
            # Show orignal
            # cv2.imshow('Orignal', self.frame1)                   
            # Simply pressing X on the window won't work!
            if cv2.waitKey(1) & 0xFF == ord('q'):            # press q key to close window and brake wile loop
                # stop_thread = True 
                break
            if ret:
                self.change_pixmap_signal.emit(self.frame1)
        # shut down capture system
        self.cap.release()

    #Sets run flag to False and waits for thread to finish"""
    def stop(self):
        self._run_flag = False
        self.wait()

# MAIN
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()
