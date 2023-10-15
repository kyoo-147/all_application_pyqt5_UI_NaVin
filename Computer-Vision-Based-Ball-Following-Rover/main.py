from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np

dist = lambda x1,y1,x2,y2:((x1-x2)**2 + (y1-y2)**2)
x = 0
y = 0

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.prevCircle = None

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, frame = cap.read()
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurFrame = cv2.GaussianBlur(grayFrame, (25,25), 0)
            circle = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 0.8, 80, param1=80, param2=25, minRadius=60, maxRadius=120)
            
            # Draw Coordinates System
            x = int(cap.get(3))
            y = int(cap.get(4))
            mid_x = int(x/2)
            mid_y = int(y/2)
            frame = cv2.line(frame, (mid_x, 0), (mid_x, y), (0, 255, 0), 2)
            frame = cv2.line(frame, (0, mid_y), (x, mid_y), (0, 255, 0), 2)
            frame = cv2.rectangle(frame, (mid_x-100, mid_y-100), (mid_x+100, mid_y+100), (0, 0, 255), 2)

            if circle is None:
                cv2.putText(frame,"Searching!!!",(mid_x,mid_y-100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                #Send Arduino signal to turn the BOT 360 (To Search) 

            if circle is not None:
                circle = np.uint16(np.around(circle))
                chosen = None
                for i in circle[0,:]:
                    if chosen is None : chosen = i
                    if self.prevCircle is not None:
                        if dist(i[0],i[1],chosen[0],chosen[1]) < dist(i[0],i[1],self.prevCircle[0],self.prevCircle[1]):
                            chosen = i
                cv2.circle(frame, (chosen[0], chosen[1]), 1,(0, 100, 100), 3)
                cv2.circle(frame, (chosen[0], chosen[1]), chosen[2],(255, 0, 255), 3)  #Center Coordinates (chosen[0],chosen[1])


                # Navigation Measurements 
                c_x = chosen[0]        # Circle X
                c_y = chosen[1]        # Circle Y
                r_start_x =  mid_x-100 # Rectangular Start X
                r_end_x   =  mid_x+100 # Rectangular End X
                r_start_y =  mid_y-100 # Rectangular Start Y
                r_end_y   =  mid_y+100 # Rectangular End y            

                # Navigation Algorithm 
                if r_start_x<c_x<r_end_x and r_start_y<c_y<r_end_y:
                    cv2.putText(frame,"DETECTED!!!",(mid_x,mid_y-100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    # If Distance(Using ultrasonic) is less than the threshold, Send Arduino to stop motor and blink green LED
                elif c_x>r_start_x:
                    cv2.putText(frame," GO LEFT!!!",(mid_x,mid_y-100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    #Send Arduino to move left
                elif c_x<r_start_x:
                    cv2.putText(frame,"GO RIGHT!!!",(mid_x,mid_y-100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    #Send Arduino to move right
                self.prevCircle = chosen 

            if ret:
                self.change_pixmap_signal.emit(frame)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ball Following Rover Using OpenCV")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        #self.image_label.resize(self.disply_width, self.display_height)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())