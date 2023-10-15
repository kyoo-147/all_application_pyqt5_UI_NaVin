import sys
import cv2
import numpy as np
import torch
import random
import torch.backends.cudnn as cudnn

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.torch_utils import select_device
from utils.plots import plot_one_box
from detect import parse_opt

from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timerVideo = QtCore.QTimer()

        # Load GUI from file .ui and set python icon
        #loadUi('nhap.ui',self)
        loadUi('GUI.ui',self)
        self.setWindowIcon(QtGui.QIcon("python-icon.png"))
      
        # Set default picture for PyQt5
        self.initDefaultPicture()

        # recommended command-line parsing module in the Python standard library
        self.opt = parse_opt()
        print(self.opt)

        weights, imgsz = self.opt.weights, self.opt.imgsz
        
        # Device selection, determines the speed of the process
        self.device = select_device(self.opt.device)
        # half precision only supported on CUDA
        self.half = self.device.type != 'cpu'
        
        # set True to speed up constant image size inference
        cudnn.benchmark = True

        # Load model
        self.model = attempt_load(
            weights, map_location=self.device)  # load FP32 model
        stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(imgsz, s=stride)  # check img_size
        if self.half:
            self.model.half()  # to FP16

        # Get names for objects
        self.names = self.model.module.names if hasattr(
            self.model, 'module') else self.model.names

        # Get colors for objects
        self.colors = [[random.randint(0, 255)
                        for _ in range(3)] for _ in self.names]

        # actions menu
        self.actionExit.triggered.connect(self.questionExit)
        self.actionAbout_QT.triggered.connect(self.aboutQt)
        self.actionAuthor.triggered.connect(self.aboutAuthor)

        # buttons menu
        self.pushButton_Image.clicked.connect(self.objectsDetection)

    @pyqtSlot()
    def initDefaultPicture(self):
        picture = QtGui.QPixmap('github.png')
        self.label.setScaledContents(True)
        self.label.setPixmap(picture)

    # This function is called for opening the image and 
    def buttonOpenImage(self):
        print('\nOpening a image!\nPlease choose one!\n')

        # Open the folder for choosing the image
        imageName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Image", "", "All Files(*);;*.jpg;;*.png")
        if not imageName:
            return
        return imageName

    def objectsDetection(self):
        image = cv2.imread(self.buttonOpenImage())
        showImage = image
        with torch.no_grad():
            image = letterbox(image, new_shape=self.opt.imgsz)[0]
            # Convert
            # BGR to RGB, to 3x416x416
            image = image[:, :, ::-1].transpose(2, 0, 1)
            # Return a contiguous array (ndim >= 1) in memory
            image = np.ascontiguousarray(image)
            image = torch.from_numpy(image).to(self.device)
            image = image.half() if self.half else image.float()  # uint8 to fp16/32
            
            # Tranfer 0 - 255 to 0.0 - 1.0
            image /= 255.0
            if image.ndimension() == 3:
                image = image.unsqueeze(0)
            # Inference
            prediction = self.model(image, augment=self.opt.augment)[0]
            # Apply Non max suppression to optimize the bounding box 
            prediction = non_max_suppression(prediction, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes,
                                       agnostic=self.opt.agnostic_nms)
            print(prediction, '\n')

            # Process objects detection in image
            for i, det in enumerate(prediction):
                if det is not None and len(det):
                    # This is for rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(
                        image.shape[2:], det[:, :4], showImage.shape).round()

                    # Write results of objects to command line and file .txt
                    print("Name and exact scale of detected object:" )
                    for *xyxy, conf, cls in reversed(det):
                        label = '%s %.2f' % (self.names[int(cls)], conf)
                        name_list = []

                        name_list.append(self.names[int(cls)])
                        print("  ", label)
                        plot_one_box(xyxy, showImage, label=label,
                                     color=self.colors[int(cls)], line_thickness=2)        

        # Received results
        cv2.imwrite('result_Image.jpg', showImage)
        self.result = cv2.cvtColor(showImage, cv2.COLOR_BGR2BGRA)
        self.result = cv2.resize(
            self.result, (640, 480), interpolation=cv2.INTER_AREA)
        self.QtImg = QtGui.QImage(
            self.result.data, self.result.shape[1], self.result.shape[0], QtGui.QImage.Format_RGB32)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))
        self.textBrowser.setText(label)

    # This function to describe QT
    def aboutQt(self):
        QMessageBox.about(self, "About Qt - Qt Designer",
            "Qt is a cross-platform framework written in C++ language, used to develop projects, software for desktop, or mobile."
            "PyQt is a library that allows you to use Qt GUI, a very famous framework of C++. PyQt has many versions but the most recent and most supported is PyQt5.\n")
    
    # Describe author
    def aboutAuthor(self):
        QMessageBox.about(self, "About Author", "Instructor: Коцубинский В. П.\nExecutor: Tran Huu Thai\n\n"
                                                    "Contact me: \n"
                                                    "Number Phone - 89138032486\n"
                                                    "Email - Thaitran130399.tusur@gmail.com")

    # Exit
    def questionExit(self):
        message = QMessageBox.question(self, "Exit", "Do you want to exit? Please sure that you saved all your data!", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            print("Closing Application")
            self.close()

if __name__ == '__main__':
    application = QApplication(sys.argv)
    windows = Ui_MainWindow()
    windows.show()
    try:
        sys.exit(application.exec())
    except:
        print("Exitting...")