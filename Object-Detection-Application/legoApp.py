


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import cv2
import numpy as np


# threshold
# ****************************
# probability threshold
thres = 0.45  # threshold to detect objects
# non maximum suppression probability threshold
nms_threshold = 0.5
# ****************************


# pathing
# **********************************************
# array to store class names
classNames = []
classFile = 'coco.names'
# this reads the coco names into an array instead of adding them all in manually, much easier and dynamic.
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# pathing
# tensorflow code which is  ai object detection software
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# a complete tensorflow model
weightsPath = 'frozen_inference_graph.pb'
# **********************************************


# object detection model
# **********************************************

# does the processing using openCV
# http://www.bim-times.com/opencv/4.3.0/javadoc/org/opencv/dnn/Model.html
net = cv2.dnn_DetectionModel(weightsPath, configPath)
# set input size for frame
net.setInputSize(320, 320)
# Set scalefactor value for frame.
net.setInputScale(1.0 / 127.5)
# Set mean value for frame.
net.setInputMean((125.5, 127.5, 127.5))
# Set flag swapRB for frame.
net.setInputSwapRB(True)


# **********************************************

global count

#create GUI
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 500)
        Form.setStyleSheet("background-color:rgb(245, 245, 245)")
        self.lblImage = QLabel(Form)
        #pixels from left,top,left,top(side:left,top,right,bottom)
        self.lblImage.setGeometry(QRect(1, 10, 581, 380))
        self.lblImage.setText("")
        self.lblImage.setPixmap(QPixmap("../Users/LeoMc/PycharmProjects/pyQt5Project/Queenslogo.jpg"))
        self.lblImage.setScaledContents(True)
        self.lblImage.setObjectName("lblImage")
        self.lblImage.setText("")
        self.lblImage.setPixmap(QPixmap("Queenslogo.jpg"))
        self.lblImage.setScaledContents(True)
        self.lblImage.setObjectName("lblImage")
        self.lblResult = QLabel(Form)
        fontResult = QFont()
        fontResult.setFamily("Calibri")
        fontResult.setPointSize(16)
        self.lblResult.setStyleSheet("color:rgb(30,31,31)")
        self.lblResult.setFont(fontResult)
        self.lblResult.setText("")
        self.lblResult.setScaledContents(True)
        self.lblResult.setObjectName("lblResult")
        self.lblResult.setGeometry(QRect(1, 430, 591, 41))
        self.lblKey = QLabel(Form)
        self.lblKey.setStyleSheet("color:rgb(30,31,31)")
        self.lblKey.setFont(fontResult)
        self.lblKey.setText("")
        self.lblKey.setScaledContents(True)
        self.lblKey.setObjectName("lblkey")
        self.lblKey.setGeometry(QRect(1, 390, 591, 41))
        self.btnStart = QPushButton(Form)
        self.btnStart.setGeometry(QRect(630, 70, 191, 81))
        self.btnStart = QPushButton(Form)
        self.btnStart.setGeometry(QRect(630, 70, 191, 81))
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.btnStart.setFont(font)
        self.btnStart.setStyleSheet("background-color:rgb(101, 185, 201);\n"
"color:rgb(30, 31, 31)")
        self.btnStart.clicked.connect(self.btnStart_Clicked)       
        self.btnStart.setObjectName("btnStart")
        self.btnStop = QPushButton(Form)
        self.btnStop.setGeometry(QRect(630, 230, 191, 81))
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.btnStop.setFont(font)
        self.btnStop.setStyleSheet("background-color:rgb(201, 60, 60);\n"
"color:rgb(32, 33, 33)\n"
"")
        self.btnStop.setObjectName("btnStop")
        self.btnStop.clicked.connect(self.btnStop_Clicked)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)
        self.FeedLabel = QLabel()
        
#set text of UI
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnStart.setText(_translate("Form", "Start"))
        self.btnStop.setText(_translate("Form", "Stop"))
        self.lblResult.setText(_translate("Form", " " ))
        self.lblKey.setText(_translate("Form", " Waste Object Detector" ))
        

    # initialise thread which updates video frame and counter when start button is pressed
    def btnStart_Clicked(self):
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.ResultUpdate.connect(self.ResultUpdateSlot)
        self.Worker1.KeyUpdate.connect(self.KeyUpdateSlot)
        

    # stop video thread when stop button is pressed
    def btnStop_Clicked(self):  
        self.Worker1.stop()





        
    #update image frame
    def ImageUpdateSlot(self, Image):
        self.lblImage.setPixmap(QPixmap.fromImage(Image))

    # update result
    def ResultUpdateSlot(self,result):
        if(result == "stopped"):
           self.lblResult.setText("")
        else:
           self.lblResult.setText(result)

    # update key
    def KeyUpdateSlot(self,key):
        if(key == "stopped"):
           self.lblKey.setText("Waste Object Detector")
        else:
           self.lblKey.setText(key)


    

    
# create Qthread
class Worker1(QThread):
    #signals used for updating
    ImageUpdate = pyqtSignal(QImage)
    ResultUpdate = pyqtSignal(str)
    KeyUpdate = pyqtSignal(str)
    
    def run(self):
        #initialising here to stop bugs
        frameCount = 0
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                #count ojects per x number of frames
                frameCount +=1
                objectnames = []
                uniqueobjectscount = []
                classIds, confs, bbox = net.detect(frame, confThreshold=thres)

                # convert bbox to list
                bbox = list(bbox)
                # reshape array to 1 row and unknown columns
                confs = list(np.array(confs).reshape(1, -1)[0])
                # returns confs with values converted to floats
                confs = list(map(float, confs))
                # output              
                # Non Maximum Suppression to filter out boxes and select the best
                indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)

                for i in indices:
                    i = i[0]
                    box = bbox[i]
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    # https://stackoverflow.com/questions/23720875/how-to-draw-a-rectangle-around-a-region-of-interest-in-python
                    # code to build rectangle around a box (image, start_point, end_point, color, thickness)
                    cv2.rectangle(frame, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
                    cv2.putText(frame, classNames[classIds[i][0] - 1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
                    Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    #convert image to QImage format
                    ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                    #scale image
                    Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    # send signal to update
                    self.ImageUpdate.emit(Pic)
                    # convert array class ids to upper case  compare
                    #********************
                    #i want to create a table with two rows, 1st row is the unique objects detected and the second is the number of each specific object
                    #update every x frames in an attempt to take pressure of processor
                    self.KeyUpdate.emit("Key: [ Object , Count ]")
                    if (frameCount % 60 ==0):
                        for i in classIds:
                            #i for person classId would be 1, so -1 to get 0 and index 0 of classnames is 'person'
                            #get object name
                            name = (classNames[int(i)-1])
                            #add to objectnames list
                            objectnames.append(name)
                        #cycle through list
                        for i in objectnames:                     
                            #get count of said item and add to list for count
                            uniqueobjectscount.append(objectnames.count(i))

                        #merge lists into 2d list
                        objectvalues = [list(item) for item in zip(objectnames, uniqueobjectscount)]
                        
                        
                        #create list to store non duplicate list
                        objectvaluesNonDuplicate =[]
                        
                        #remove duplicates
                        [objectvaluesNonDuplicate.append(x) for x in objectvalues if x not in objectvaluesNonDuplicate]
        
                        #join list into a string with " " as seperator
                        #turn list into string
                        resultnames = " ".join(str(item) for item in objectvaluesNonDuplicate)
                        #update every x frames to make more readable
                        if (frameCount % 60 ==0):
                            self.ResultUpdate.emit(resultnames)
                        
                    # reset values every frame
                        
                        resultnames = ""
                        objectnames = []
                        uniqueobjectscount = []
                        #to refresh thread in an attempt to take pressure off processor
                        
                        
        # output result
        
        #after stop button has been pressed
        Capture.release()
        logo = QImage("Queenslogo.jpg")
        self.ResultUpdate.emit("stopped")
        self.ImageUpdate.emit(logo)
        self.KeyUpdate.emit("stopped")

    # End thread but not program
    def stop(self):
        self.ThreadActive = False
        



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
