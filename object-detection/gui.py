import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from detect import Detect
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QTimer, Qt
import cv2

class Gui(QWidget):
    def __init__(self):
        super().__init__()
        # Create a timer
        self._timer = QTimer()
        # Connect the timeout signal to the nextFrame slot
        self._timer.timeout.connect(self.nextFrameSlot)
        # Create a layout
        self._layout = QVBoxLayout()
        # Create a label
        self._label = QLabel()
        # Add the label to the layout
        self._layout.addWidget(self._label, alignment=Qt.AlignCenter)
        # Add open webcam button
        self.addButton(text="Open Webcam", slot=self.openWebcam)
        # Add stop webcam button
        self.addButton(text="Stop Webcam", slot=self.stopWebcam)
        self._cap = None
        # Set the layout to the application
        self.setLayout(self._layout)
        # Set the window title
        self.setWindowTitle("Vehicle speed estimation & Tracking")
        # Set the window size
        self.setFixedSize(800, 800)
        self._grid = None
        self.initializeNetwork()

    def addButton(self, text="Default", slot=None):
        button_layout = QHBoxLayout()
        btnCamera = QPushButton(text)
        btnCamera.clicked.connect(slot)
        button_layout.addWidget(btnCamera)
        self._layout.addLayout(button_layout)   

    def openWebcam(self):
        # Create a VideoCapture object
        self._cap = cv2.VideoCapture(0)
        # Set width and height
        self._cap.set(3, 640)
        self._cap.set(4, 480)
        if not self._cap.isOpened():
            msgBox = QMessageBox()
            msgBox.setText("Error opening webcam")
            msgBox.exec_()
            return
        # Start the timer
        self._timer.start(1000./24)

    def stopWebcam(self):
        # Stop the timer
        self._timer.stop()
        # Release the VideoCapture object
        self._cap.release()

    def convertNparrayToQPixmap(self, nparray):
        frame = cv2.cvtColor(nparray, cv2.COLOR_BGR2RGB)
        frame = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(frame)
        return pixmap

    def initializeNetwork(self):
        # Create Detect object
        self._detect = Detect()
        # Initialize model
        self._network = self._detect.initializeModel()

    def nextFrameSlot(self, frame=None):
        # Read the next frame
        ret, frame = self._cap.read()
        frame = self._detect.detect(network=self._network, frame=frame)
        # Convert the frame to a pyqt image
        pixmap = self.convertNparrayToQPixmap(frame)
        # Display the image
        self._label.setPixmap(pixmap)
    