from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import *
from pathlib import Path
import os
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import time
from PyQt5.QtCore import QBuffer
import io
import asyncio
import threading
from playsound import playsound

class MaskDetectorForm(QtWidgets.QWidget):

    root_path = Path(os.path.abspath('')).parent
    app_font = QFont('Arial',24)
    stack = None
    available_cameras = QCameraInfo.availableCameras()
    shield = False

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.model = tensorflow.keras.models.load_model(str(self.root_path)+'/models/mask_model.h5')
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)
        # Load the model

        # 쓰레드 인스턴스 생성
        self.th = TestThread(self)
        # 쓰레드 이벤트 연결
        self.th.threadEvent.connect(self.threadEventHandler)

        self.threadStart()


    def setup_ui(self):
        self.setWindowTitle('Dummy Review Sentiment')
        self.resize(800,600)
        self.scaledImage = None
        self.title_label = QtWidgets.QLabel()
        self.title_label.setText('Dummy Review Sentiment')
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(self.app_font)
        self.title_label.setStyleSheet('color : white')

        self.back_btn = QtWidgets.QPushButton()
        self.back_btn.setText('Back to Home')
        self.back_btn.setMaximumHeight(50)
        self.back_btn.clicked.connect(self.back_btn_function)

        self.grid_layout = QtWidgets.QGridLayout()
        # 그리드 레이아웃 크기 지정
        # self.grid_layout.cellRect(5,3)
        # 그리드 레이아웃 각 행열의 사이즈 계수 1로 고정 ,, 0이 아니라 1부터 시작 주의
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)

        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setRowStretch(4, 1)

        self.setLayout(self.grid_layout)

        # 3,4 파라미터는 행은 1개먹고, 열은 2개먹고
        self.grid_layout.addWidget(self.title_label, 0, 0, 1, 3)

        self.grid_layout.addWidget(self.back_btn, 4, 1, 1, 1)

        # path to save
        self.save_path = ""

        # creating a QCameraViewfinder object

        self.viewfinder = QCameraViewfinder()

        # showing this viewfinder
        self.viewfinder.show()

        # making it central widget of main window

        #layout
        # self.setCentralWidget(self.viewfinder)
        self.grid_layout.addWidget(self.viewfinder, 1, 0, 3, 3)

        # Set the default camera.
        self.select_camera(0)

        # creating a photo action to take photo
        click_action = QtWidgets.QAction("Click photo", self)

        # adding status tip to the photo action
        click_action.setStatusTip("This will capture picture")

        # adding tool tip
        click_action.setToolTip("Capture picture")

        # adding action to it
        # calling take_photo method
        click_action.triggered.connect(self.click_photo)

        # similarly creating action for changing save folder
        change_folder_action = QtWidgets.QAction("Change save location",
                                       self)

        # adding status tip
        change_folder_action.setStatusTip("Change folder where picture will be saved saved.")

        # adding tool tip to it
        change_folder_action.setToolTip("Change save location")

        # setting calling method to the change folder action
        # when triggered signal is emitted
        change_folder_action.triggered.connect(self.change_folder)


        # creating a combo box for selecting camera
        camera_selector = QtWidgets.QComboBox()

        # adding status tip to it
        camera_selector.setStatusTip("Choose camera to take pictures")

        # adding tool tip to it
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)

        # adding items to the combo box
        camera_selector.addItems([camera.description()
                                  for camera in self.available_cameras])

        # adding action to the combo box
        # calling the select camera method
        camera_selector.currentIndexChanged.connect(self.select_camera)


        # method to select camera

    def select_camera(self, i):
            # getting the selected camera
        self.camera = QCamera(self.available_cameras[i])

            # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)

            # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureStillImage)

            # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))

            # start the camera
        self.camera.start()

            # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)

            # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error,
                                              msg: self.alert(msg))

            # when image captured showing message
        # self.capture.imageCaptured.connect(lambda d,
        #                                               i: self.status.showMessage("Image captured : "
        #                                                                          + str(self.save_seq)))
        self.capture.imageCaptured.connect(self.processCapturedImage)
            # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()

            # inital save sequence
        self.save_seq = 0

        # method to take photo

    def processCapturedImage(self, requestId, img):
        # Q_UNUSED(requestId);
        self.scaledImage = img
        print("cap")



    def click_photo(self):
            # time stamp

        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")

            # capture the image and save it on the save path
        self.capture.capture(os.path.join(self.save_path,
                                              "%s-%04d-%s.jpg" % (
                                                  self.current_camera_name,
                                                  self.save_seq,
                                                  timestamp
                                              )))

            # increment the sequence
        self.save_seq += 1

        # change folder method
    def change_folder(self):
            # open the dialog to select path
        path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                    "Picture Location", "")

            # if path is selected
        if path:
                # update the path
            self.save_path = path

                # update the sequence
            self.save_seq = 0


    def alert(self, msg):
            # error message
        error = QtWidgets.QErrorMessage(self)

        # setting text to the error message
        error.showMessage(msg)


    def paintEvent(self, a0: QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.7)
        painter.drawRect(self.rect())


        pix = QtGui.QPixmap()  # Change to the relative path of your own image
        img_path = str(self.root_path) + '/imgs/ui/background-img.png'
        pix.load(img_path)

        painter.drawPixmap(self.rect(), pix)

    def init_StackWidget(self, para):
        self.stack = para

    def back_btn_function(self):
        self.stack.removeWidget(self)
        # setCurrentIndex 안해도 removeWidget 하면 넘어감.. self.stack.setCurrentIndex(self.stack.currentIndex())

    def mask_model(self):
        self.capture.capture()
        try:
            if self.scaledImage == None:
                return
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            self.scaledImage.save(buffer, "jpg")
            image = Image.open(io.BytesIO(buffer.data()))
#            buffer.close()
        except TypeError:
#            print("q_img error")
#            buffer.close()
            return

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        # str(self.root_path) + '/imgs/xx.png'
        #         image = Image.open('test_photo.jpg')

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # # display the resized image
        # image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = self.model.predict(data)
        print(prediction)
        if prediction[0][0] > 0.9 and self.shield == False:
            # playsound(str(self.root_path) + '/musics/alert.mp3', False)
            shield = True
            self.title_label.setText("통과입니다.")
            self.title_label.setStyleSheet("color : #0000FF")
        else :
            self.title_label.setText("마스크를 착용해주세요.")
            self.title_label.setStyleSheet("color : #00FF00")


#


    @pyqtSlot()
    def threadStart(self):
        if not self.th.isRun:
            print('메인 : 쓰레드 시작')
            self.th.isRun = True
            self.th.start()

    @pyqtSlot()
    def threadStop(self):
        if self.th.isRun:
            print('메인 : 쓰레드 정지')
            self.th.isRun = False

    # 쓰레드 이벤트 핸들러
    # 장식자에 파라미터 자료형을 명시
    @pyqtSlot(int)
    def threadEventHandler(self, n):
#        print('호출 : threadEvent(self,' + str(n) + ')')
        self.mask_model()

class TestThread(QtCore.QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.n = 0
        self.main = parent
        self.isRun = False

    def run(self):
        while self.isRun:
#            print('쓰레드 : ' + str(self.n))

            # 'threadEvent' 이벤트 발생
            # 파라미터 전달 가능(객체도 가능)
            self.threadEvent.emit(self.n)

            self.n += 1
            self.msleep(1500)

