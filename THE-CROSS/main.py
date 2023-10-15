'''
THE-CROSS : A Smart Traffic Control System for the protection of
the socially disadvantaged and rapid transport of emergency vehicles.

Copyright (C) 2021 THE-CROSS authors
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
'''
import argparse
import sys
import threading
import time
import cv2

import Camera
import FileManager

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton
from PyQt5 import QtGui

import ImageUtils
from ImageUtils import cvImgToQtImg, draw_area, isAnyObjectInRect
from Camera import VideoThread, CameraSetup
from SirenDetector import SirenDetector

# ====================== [ GUI CONFIG ] =========================

CAMERA_W = 400
CAMERA_H = 300

IMAGE_PATH = "Images/"

TIMER_FONT = 'Arial'
CONFIRM_BUTTON_FONT = 'Arial'

Option_INC_TIME_NORMAL_LABEL_TEXT = "Time to increase for ORDINARY PEOPLE (natural number)(seconds) : "
Option_INC_TIME_SPECIAL_LABEL_TEXT = "Time to increase for THE SOCIALLY DISADVANTAGED (natural number)(seconds) : "
Option_TIME_CROSSWALK_GREEN_LABEL_TEXT = "Basic pedestrian signal time (natural number)(seconds) : "
Option_TIME_CARLANE_GREEN_LABEL_TEXT = "Basic vehicle signal time (natural number)(seconds) : "
Option_TIME_CHAGNE_TERM_LABEL_TEXT = "Yellow traffic light time (natural number)(seconds) : "

BUTTON_CHANGE_CROSSWALK_TIME_TEXT = "Change to pedestrian signal"
BUTTON_CHANGE_CARLINE_TIME_TEXT = "Change to a vehicle signal"
BUTTON_SETTING_LEFT_CAM_CROSSWALK_TEXT = "LEFT CAM CROSSWALK area setting"
BUTTON_SETTING_RIGHT_CAM_CROSSWALK_TEXT = "RIGHT CAM CROSSWALK area setting"
BUTTON_SETTING_LEFT_CAM_CARLINE_TEXT = "LEFT CAM CARLINE area setting"
BUTTON_SETTING_RIGHT_CAM_CARLINE_TEXT = "RIGHT CAM CARLINE area setting"

BUTTON_SETTING_SAVE = "SAVE"

WHEELCHAIR_CLASS = 0
BABY_CARRIAGE_CLASS = 1
CANE_CLASS = 2
AMBULANCE_CLASS = 3

WHEELCHAIR_LABEL = 'WHEELCHAIR'
BABY_CARRIAGE_LABEL = 'BABY_CARRIAGE'
CANE__LABEL = 'CANE'
AMBULANCE_LABEL = 'AMBULANCE'

ClassNum_List = [WHEELCHAIR_CLASS, BABY_CARRIAGE_CLASS, CANE_CLASS, AMBULANCE_CLASS]
ClassLabel_List = [WHEELCHAIR_LABEL, BABY_CARRIAGE_LABEL, CANE__LABEL, AMBULANCE_LABEL]


# ===============================================================


class Main(QWidget):
    """This class is actually a central class for using client programs.
    All functions work around this class.
    """

    def __init__(self):
        """A function to initialize the Main class
        This function declares all variables and classes required to run a client program.
        """

        super().__init__()

        self.Emergency_Ambulance = False
        self.Emergency_Person = False
        self.Emergency_DisablePerson = False

        self.SirenDetector = SirenDetector()
        self.isPreparingCamera = False
        self.config = FileManager.configManager()

        self.isTimerRun = False
        self.timerThread = threading.Thread(target=self.TimerMethod)
        self.changeTerm = self.config.getConfig()['CHANGE_TERM']
        self.timeStack = 0
        self.carlaneTime = self.config.getConfig()['CARLANE_TIME']
        self.crosswalkTime = self.config.getConfig()['CROSSWALK_TIME']
        self.timeIncNormal = self.config.getConfig()['INCREASE_TIME_NORMAL']
        self.timeIncSpecial = self.config.getConfig()['INCREASE_TIME_SPECIAL']
        self.isCrosswalkTime = False
        self.isCarlaneTime = False

        self.Left_Camera_Carlane_Button = QPushButton()
        self.Right_Camera_Carlane_Button = QPushButton()
        self.Option_TIME_CHANGE_TERM_Input = QLineEdit()
        self.Option_TIME_CARLANE_GREEN_Input = QLineEdit()
        self.Option_TIME_CROSSWALK_GREEN_Input = QLineEdit()
        self.Right_Camera_Crosswalk_Button = QPushButton()
        self.Left_Camera_Crosswalk_Button = QPushButton()
        self.Change_CarTime_Button = QPushButton()
        self.Change_CrosswalkTime_Button = QPushButton()
        self.Option_INC_TIME_SPECIAL_Input = QLineEdit()
        self.ConfirmButton = QPushButton()
        self.TimerLabel = QLabel()
        self.Option_INC_TIME_NORMAL_Input = QLineEdit()

        self.setWindowTitle(":: The CROSS :: Smart Traffic Control System")

        self.CAMERA_PREPARING_IMG_L = cvImgToQtImg(cv2.imread(IMAGE_PATH + "camera_preparing.png"), CAMERA_W)
        self.CAMERA_PREPARING_IMG_R = cvImgToQtImg(cv2.imread(IMAGE_PATH + "camera_preparing.png"), CAMERA_W)

        self.CAMERA_NO_SIGNAL_IMG_L = cvImgToQtImg(cv2.imread(IMAGE_PATH + "camera_no_signal.png"), CAMERA_W)
        self.CAMERA_NO_SIGNAL_IMG_R = cvImgToQtImg(cv2.imread(IMAGE_PATH + "camera_no_signal.png"), CAMERA_W)

        self.CROSSWALK_GREEN_ON_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "crosswalk_green_on.png"))
        self.CROSSWALK_GREEN_OFF_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "crosswalk_green_off.png"))
        self.CROSSWALK_RED_ON_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "crosswalk_red_on.png"))
        self.CROSSWALK_RED_OFF_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "crosswalk_red_off.png"))

        self.GREEN_ON_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "green_on.png"))
        self.GREEN_OFF_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "green_off.png"))
        self.RED_ON_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "red_on.png"))
        self.RED_OFF_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "red_off.png"))
        self.YELLOW_ON_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "yellow_on.png"))
        self.YELLOW_OFF_IMG = cvImgToQtImg(cv2.imread(IMAGE_PATH + "yellow_off.png"))

        self.CarLane_Green = QLabel()
        self.CarLane_Green.setPixmap(self.GREEN_OFF_IMG.pixmap())
        self.CarLane_Yellow = QLabel()
        self.CarLane_Yellow.setPixmap(self.YELLOW_OFF_IMG.pixmap())
        self.CarLane_Red = QLabel()
        self.CarLane_Red.setPixmap(self.RED_OFF_IMG.pixmap())
        self.Crosswalk_Green = QLabel()
        self.Crosswalk_Green.setPixmap(self.CROSSWALK_GREEN_OFF_IMG.pixmap())
        self.Crosswalk_Red = QLabel()
        self.Crosswalk_Red.setPixmap(self.CROSSWALK_RED_OFF_IMG.pixmap())

        self.CameraRight = QLabel()
        self.CameraRight.setPixmap(self.CAMERA_NO_SIGNAL_IMG_R.pixmap())
        self.CameraLeft = QLabel()
        self.CameraLeft.setPixmap(self.CAMERA_NO_SIGNAL_IMG_L.pixmap())
        self.initUI()

    def initUI(self):
        """This function is for GUI activation. It is also a function that actually starts the program.
        """
        UpPanel = QHBoxLayout()
        DownPanel = QHBoxLayout()

        CameraPanel = QHBoxLayout()

        SignalPanel = QVBoxLayout()
        CrosswalkPanel = QHBoxLayout()
        CarLanePanel = QHBoxLayout()

        OptionPanel = QHBoxLayout()
        OptionList = QVBoxLayout()
        ControlPanel = QVBoxLayout()

        CameraPanel.addWidget(self.CameraLeft)
        CameraPanel.addWidget(self.CameraRight)

        CrosswalkPanel.addWidget(self.Crosswalk_Red)
        CrosswalkPanel.addWidget(self.Crosswalk_Green)

        self.TimerLabel.setFont(QFont(TIMER_FONT, 60))
        self.TimerLabel.setText("0")
        CrosswalkPanel.addStretch(1)
        CrosswalkPanel.addWidget(self.TimerLabel)
        CrosswalkPanel.addStretch(1)

        CarLanePanel.addWidget(self.CarLane_Red)
        CarLanePanel.addWidget(self.CarLane_Yellow)
        CarLanePanel.addWidget(self.CarLane_Green)

        SignalPanel.addLayout(CrosswalkPanel)
        SignalPanel.addLayout(CarLanePanel)

        UpPanel.addLayout(CameraPanel, 6)
        UpPanel.addLayout(SignalPanel, 4)

        # =======================================================
        # ==================== OPTION PANEL =====================
        # =======================================================

        Option_INC_TIME_NORMAL = QHBoxLayout()
        Option_INC_TIME_NORMAL_LABEL = QLabel()
        Option_INC_TIME_NORMAL_LABEL.setText(Option_INC_TIME_NORMAL_LABEL_TEXT)
        self.Option_INC_TIME_NORMAL_Input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.Option_INC_TIME_NORMAL_Input.setText(str(self.config.getConfig()['INCREASE_TIME_NORMAL']))
        Option_INC_TIME_NORMAL.addWidget(Option_INC_TIME_NORMAL_LABEL)
        Option_INC_TIME_NORMAL.addWidget(self.Option_INC_TIME_NORMAL_Input)
        OptionList.addLayout(Option_INC_TIME_NORMAL)

        Option_INC_TIME_SPECIAL = QHBoxLayout()
        Option_INC_TIME_SPECIAL_LABEL = QLabel()
        Option_INC_TIME_SPECIAL_LABEL.setText(Option_INC_TIME_SPECIAL_LABEL_TEXT)
        self.Option_INC_TIME_SPECIAL_Input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.Option_INC_TIME_SPECIAL_Input.setText(str(self.config.getConfig()['INCREASE_TIME_SPECIAL']))
        Option_INC_TIME_SPECIAL.addWidget(Option_INC_TIME_SPECIAL_LABEL)
        Option_INC_TIME_SPECIAL.addWidget(self.Option_INC_TIME_SPECIAL_Input)
        OptionList.addLayout(Option_INC_TIME_SPECIAL)

        Option_TIME_CROSSWALK_GREEN = QHBoxLayout()
        Option_TIME_CROSSWALK_GREEN_LABEL = QLabel()
        Option_TIME_CROSSWALK_GREEN_LABEL.setText(Option_TIME_CROSSWALK_GREEN_LABEL_TEXT)
        self.Option_TIME_CROSSWALK_GREEN_Input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.Option_TIME_CROSSWALK_GREEN_Input.setText(str(self.config.getConfig()['CROSSWALK_TIME']))
        Option_TIME_CROSSWALK_GREEN.addWidget(Option_TIME_CROSSWALK_GREEN_LABEL)
        Option_TIME_CROSSWALK_GREEN.addWidget(self.Option_TIME_CROSSWALK_GREEN_Input)
        OptionList.addLayout(Option_TIME_CROSSWALK_GREEN)

        Option_TIME_CARLANE_GREEN = QHBoxLayout()
        Option_TIME_CARLANE_GREEN_LABEL = QLabel()
        Option_TIME_CARLANE_GREEN_LABEL.setText(Option_TIME_CARLANE_GREEN_LABEL_TEXT)
        self.Option_TIME_CARLANE_GREEN_Input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.Option_TIME_CARLANE_GREEN_Input.setText(str(self.config.getConfig()['CARLANE_TIME']))
        Option_TIME_CARLANE_GREEN.addWidget(Option_TIME_CARLANE_GREEN_LABEL)
        Option_TIME_CARLANE_GREEN.addWidget(self.Option_TIME_CARLANE_GREEN_Input)
        OptionList.addLayout(Option_TIME_CARLANE_GREEN)

        Option_TIME_CHAGNE_TERM = QHBoxLayout()
        Option_TIME_CHAGNE_TERM_LABEL = QLabel()
        Option_TIME_CHAGNE_TERM_LABEL.setText(Option_TIME_CHAGNE_TERM_LABEL_TEXT)
        self.Option_TIME_CHANGE_TERM_Input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.Option_TIME_CHANGE_TERM_Input.setText(str(self.config.getConfig()['CHANGE_TERM']))
        Option_TIME_CHAGNE_TERM.addWidget(Option_TIME_CHAGNE_TERM_LABEL)
        Option_TIME_CHAGNE_TERM.addWidget(self.Option_TIME_CHANGE_TERM_Input)
        OptionList.addLayout(Option_TIME_CHAGNE_TERM)

        # OptionList Attach To OptionPanel
        OptionPanel.addLayout(OptionList, 8)

        # =======================================================
        # ==================== CONTROL PANEL ====================
        # =======================================================

        self.Change_CrosswalkTime_Button.setText(BUTTON_CHANGE_CROSSWALK_TIME_TEXT)
        self.Change_CarTime_Button.setText(BUTTON_CHANGE_CARLINE_TIME_TEXT)

        self.Change_CrosswalkTime_Button.clicked.connect(self.Change_CrosswalkTime_Button_Event)
        self.Change_CarTime_Button.clicked.connect(self.Change_CarTime_Button_Event)

        self.Left_Camera_Crosswalk_Button.setText(BUTTON_SETTING_LEFT_CAM_CROSSWALK_TEXT)
        self.Right_Camera_Crosswalk_Button.setText(BUTTON_SETTING_RIGHT_CAM_CROSSWALK_TEXT)

        self.Left_Camera_Crosswalk_Button.clicked.connect(self.Left_Camera_Crosswalk_Button_Event)
        self.Right_Camera_Crosswalk_Button.clicked.connect(self.Right_Camera_Crosswalk_Button_Event)

        self.Left_Camera_Carlane_Button.setText(BUTTON_SETTING_LEFT_CAM_CARLINE_TEXT)
        self.Right_Camera_Carlane_Button.setText(BUTTON_SETTING_RIGHT_CAM_CARLINE_TEXT)

        self.Left_Camera_Carlane_Button.clicked.connect(self.Left_Camera_Carlane_Button_Event)
        self.Right_Camera_Carlane_Button.clicked.connect(self.Right_Camera_Carlane_Button_Event)

        Control_Crosswalk_Panel = QHBoxLayout()
        Control_Crosswalk_Panel.addWidget(self.Change_CarTime_Button)
        Control_Crosswalk_Panel.addWidget(self.Change_CrosswalkTime_Button)

        Control_Camera_Crosswalk_Panel = QHBoxLayout()
        Control_Camera_Crosswalk_Panel.addWidget(self.Left_Camera_Crosswalk_Button)
        Control_Camera_Crosswalk_Panel.addWidget(self.Right_Camera_Crosswalk_Button)

        Control_Camera_Carlane_Panel = QHBoxLayout()
        Control_Camera_Carlane_Panel.addWidget(self.Left_Camera_Carlane_Button)
        Control_Camera_Carlane_Panel.addWidget(self.Right_Camera_Carlane_Button)

        ControlPanel.addLayout(Control_Crosswalk_Panel)
        ControlPanel.addLayout(Control_Camera_Crosswalk_Panel)
        ControlPanel.addLayout(Control_Camera_Carlane_Panel)

        # =======================================================
        # ==================== CONFIRM BUTTON ===================
        # =======================================================

        self.ConfirmButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ConfirmButton.setText(BUTTON_SETTING_SAVE)
        self.ConfirmButton.setFont(QFont(CONFIRM_BUTTON_FONT, 20))
        self.ConfirmButton.clicked.connect(self.confirmButtonClicked)
        OptionPanel.addWidget(self.ConfirmButton, 2)

        DownPanel.addLayout(OptionPanel, 63)
        DownPanel.addLayout(ControlPanel, 37)

        allPanel = QVBoxLayout()
        allPanel.addLayout(UpPanel)
        allPanel.addLayout(DownPanel)

        self.setLayout(allPanel)
        self.setFixedSize(self.sizeHint())

        # Set Up Camera
        self.preparingCamera()
        self.thread = VideoThread(self.config.getConfig()['LEFT_CAMERA_NUMBER'],
                                  self.config.getConfig()['RIGHT_CAMERA_NUMBER'])
        self.thread.change_pixmap_signal.connect(self.processing)
        self.thread.start()
        self.isPreparingCamera = False

        # Set Up Timer
        self.start_Timer()

        # Set Up Siren Detector
        self.startSirenDetector()

        # Set Up GUI
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        """This function is an event function that occurs when the exit button is clicked in the GUI,
        allowing the client program to end safely.
        """
        self.stop_Timer()
        self.stopSirenDetector()
        self.thread.close()
        time.sleep(3)
        self.close()

    # imgLeft & imgRight must be cvImage
    def processing(self, imgLeft, imgRight, left_pos, right_pos, custom_left_pos, custom_right_pos):
        """This function is a function that receives an image from a camera, receives an object detection result,
        and determines whether to adjust the signal or not.

        :param 3D-ndarray imgLeft: 3D ndarray type variable, which has left image data.
        :param 3D-ndarray imgRight: 3D ndarray type variable, which has right image data.

        :param 2D-list left_pos: A list of coordinates of the detected person in left image.
        .. Note:: left_pos must have the form of [[xmin, ymax, xmax, ymin], [..], ..]

        :param 2D-list right_pos: A list of coordinates of the detected person in right image.
        .. Note:: right_pos must have the form of [[xmin, ymax, xmax, ymin], [..], ..]

        :param 3D-list custom_left_pos: A list of coordinates of the detected objects in left image.
        .. Note:: custom_left_pos must have the form of [ [ [xmin, ymax, xmax, ymin], [..], .. ], [..], .. ]

        :param 3D-list custom_right_pos: A list of coordinates of the detected objects in right image.
        .. Note:: custom_right_pos must have the form of [ [ [xmin, ymax, xmax, ymin], [..], .. ], [..], .. ]
        """

        if self.isPreparingCamera is True:
            return

        # Flags
        isPersonExist = False
        isDisablePersonExist = False
        isAmbulanceExist = False
        isSiren = self.SirenDetector.isSiren()

        # Unpacking Positions of Objects Detected on Left Camera
        wheelchair_pos_left = custom_left_pos[WHEELCHAIR_CLASS]
        baby_carriage_pos_left = custom_left_pos[BABY_CARRIAGE_CLASS]
        cane_pos_left = custom_left_pos[CANE_CLASS]
        ambulance_pos_left = custom_left_pos[AMBULANCE_CLASS]

        # Unpacking Positions of Objects Detected on Right Camera
        wheelchair_pos_right = custom_right_pos[WHEELCHAIR_CLASS]
        baby_carriage_pos_right = custom_right_pos[BABY_CARRIAGE_CLASS]
        cane_pos_right = custom_right_pos[CANE_CLASS]
        ambulance_pos_right = custom_right_pos[AMBULANCE_CLASS]

        # Draw Person Detection Box on Left-Camera image
        if len(left_pos) != 0:
            imgLeft = ImageUtils.draw_detection_boxes(imgLeft, left_pos, 'PERSON')

        if len(right_pos) != 0:
            imgRight = ImageUtils.draw_detection_boxes(imgRight, right_pos, 'PERSON')

        # Draw Custom Detection Box on Left-Camera image
        for classNum in ClassNum_List:
            if len(custom_left_pos[classNum]) == 0:
                continue
            imgLeft = ImageUtils.draw_detection_boxes(
                imgLeft, custom_left_pos[classNum], ClassLabel_List[classNum])

        # Draw Custom Detection Box on Right-Camera image
        for classNum in ClassNum_List:
            if len(custom_right_pos[classNum]) == 0:
                continue
            imgRight = ImageUtils.draw_detection_boxes(
                imgRight, custom_right_pos[classNum], ClassLabel_List[classNum])

        if len(imgLeft) == 0:
            imgLeft = self.CAMERA_NO_SIGNAL_IMG_L
        else:
            CrossArea = self.config.getConfig()['LEFT_CAMERA_CROSSWALK_POS']
            CarLaneArea = self.config.getConfig()['LEFT_CAMERA_CARLANE_POS']

            if isPersonExist is False and isAnyObjectInRect(CrossArea, left_pos):
                isPersonExist = True

            if isDisablePersonExist is False:
                if isAnyObjectInRect(CrossArea, cane_pos_left) or isAnyObjectInRect(CrossArea,
                                                                                    wheelchair_pos_left) or \
                        isAnyObjectInRect(CrossArea, baby_carriage_pos_left):
                    isDisablePersonExist = True

            if isAmbulanceExist is False:
                if isAnyObjectInRect(CarLaneArea, ambulance_pos_left):
                    isAmbulanceExist = True

            imgLeft = draw_area(imgLeft, CrossArea)
            imgLeft = draw_area(imgLeft, CarLaneArea, (255, 0, 0), (255, 0, 0))
            imgLeft = cvImgToQtImg(imgLeft, CAMERA_W)

        self.CameraLeft.setPixmap(imgLeft.pixmap())

        if len(imgRight) == 0:
            imgRight = self.CAMERA_NO_SIGNAL_IMG_R
        else:
            CrossArea = self.config.getConfig()['RIGHT_CAMERA_CROSSWALK_POS']
            CarLaneArea = self.config.getConfig()['RIGHT_CAMERA_CARLANE_POS']

            if isPersonExist is False and isAnyObjectInRect(CrossArea, right_pos):
                isPersonExist = True

            if isDisablePersonExist is False:
                if isAnyObjectInRect(CrossArea, cane_pos_right) or isAnyObjectInRect(CrossArea,
                                                                                     wheelchair_pos_right) or \
                        isAnyObjectInRect(CrossArea, baby_carriage_pos_right):
                    isDisablePersonExist = True

            if isAmbulanceExist is False:
                if isAnyObjectInRect(CarLaneArea, ambulance_pos_right):
                    isAmbulanceExist = True

            imgRight = draw_area(imgRight, CrossArea)
            imgRight = draw_area(imgRight, CarLaneArea, (255, 0, 0), (255, 0, 0))
            imgRight = cvImgToQtImg(imgRight, CAMERA_W)

        self.CameraRight.setPixmap(imgRight.pixmap())

        if self.timeStack <= self.changeTerm:
            if self.isCrosswalkTime is False and self.isCarlaneTime is True:
                if isSiren is True and isAmbulanceExist is True:
                    self.Emergency_Ambulance = True
                else:
                    self.Emergency_Ambulance = False

            elif self.isCrosswalkTime is True and self.isCarlaneTime is False:
                if isDisablePersonExist is True:
                    self.Emergency_DisablePerson = True
                elif isPersonExist is True:
                    self.Emergency_Person = True

    # ============== CONTROL PANEL SIGH CONTROL ================

    def crosswalk_TurnRed_On(self):
        """This function turns on the pedestrian red signal in the GUI.
        """
        self.Crosswalk_Red.setPixmap(self.CROSSWALK_RED_ON_IMG.pixmap())

    def crosswalk_TurnRed_Off(self):
        """This function turns off the pedestrian red signal in the GUI.
        """
        self.Crosswalk_Red.setPixmap(self.CROSSWALK_RED_OFF_IMG.pixmap())

    def crosswalk_TurnGreen_On(self):
        """This function turns on the pedestrian green signal in the GUI.
        """
        self.Crosswalk_Green.setPixmap(self.CROSSWALK_GREEN_ON_IMG.pixmap())

    def crosswalk_TurnGreen_Off(self):
        """This function turns off the pedestrian green signal in the GUI.
        """
        self.Crosswalk_Green.setPixmap(self.CROSSWALK_GREEN_OFF_IMG.pixmap())

    def carlane_TurnRed_On(self):
        """This function turns on the GUI's vehicle red signal.
        """
        self.CarLane_Red.setPixmap(self.RED_ON_IMG.pixmap())

    def carlane_TurnRed_Off(self):
        """This function turns off the GUI's vehicle red signal.
        """
        self.CarLane_Red.setPixmap(self.RED_OFF_IMG.pixmap())

    def carlane_TurnGreen_On(self):
        """This function turns on the GUI's vehicle green signal.
        """
        self.CarLane_Green.setPixmap(self.GREEN_ON_IMG.pixmap())

    def carlane_TurnGreen_Off(self):
        """This function turns off the GUI's vehicle green signal.
        """
        self.CarLane_Green.setPixmap(self.GREEN_OFF_IMG.pixmap())

    def carlane_TurnYellow_On(self):
        """This function turns on the GUI's vehicle yellow signal.
        """
        self.CarLane_Yellow.setPixmap(self.YELLOW_ON_IMG.pixmap())

    def carlane_TurnYellow_Off(self):
        """This function turns of the GUI's vehicle yellow signal.
        """
        self.CarLane_Yellow.setPixmap(self.YELLOW_OFF_IMG.pixmap())

    # ================ CONTROL PANEL CAMERA Setting ==================

    def preparingCamera(self):
        """This function stops the output of two real-time images displayed on the GUI,
        allowing the user to adjust the camera.
        """
        self.isPreparingCamera = True
        self.CameraLeft.setPixmap(self.CAMERA_PREPARING_IMG_L.pixmap())
        self.CameraRight.setPixmap(self.CAMERA_PREPARING_IMG_R.pixmap())

    def stopCamera(self):
        """This function stops VideoThread instance from delivering real-time images to MainClass,
        stops real-time images output on the GUI,
        and actually stops the camera.
        """
        if self.thread.isRun() is True:
            self.thread.stop()
            self.preparingCamera()

    def refreshCamera(self):
        """This function is a function that brings back the camera's set value,
        resets the camera, and allows the camera to work again.
        """
        self.stopCamera()
        self.preparingCamera()
        self.thread.setCameraNumber(self.config.getConfig()['LEFT_CAMERA_NUMBER'],
                                    self.config.getConfig()['RIGHT_CAMERA_NUMBER'])
        self.thread.start()
        self.isPreparingCamera = False

    # ================= CONTROL PANEL BUTTON EVENTS =====================

    def confirmButtonClicked(self):
        """This function is a function called to store the program settings that the user has changed on the GUI.
        This function allows the user's changed program setting value to be stored in the config.json file on the GUI,
        so that the user's changed program setting value on the GUI
        can be applied directly to the currently operating program.

        .. Note:: It may take up to one cycle of traffic light before the program setting value changed by the user is applied on the GUI. This varies depending on the current traffic light signal status.

        """

        # GET TEXTBOX VALUES
        try:
            INCREASE_TIME_NORMAL = int(self.Option_INC_TIME_NORMAL_Input.text())
            INCREASE_TIME_SPECIAL = int(self.Option_INC_TIME_SPECIAL_Input.text())
            CROSSWALK_TIME = int(self.Option_TIME_CROSSWALK_GREEN_Input.text())
            CARLANE_TIME = int(self.Option_TIME_CARLANE_GREEN_Input.text())
            CHANGE_TERM = int(self.Option_TIME_CHANGE_TERM_Input.text())
        except ValueError as e:
            return

        # SAVE AT JSON
        self.config.setConfig('INCREASE_TIME_NORMAL', INCREASE_TIME_NORMAL)
        self.config.setConfig('INCREASE_TIME_SPECIAL', INCREASE_TIME_SPECIAL)
        self.config.setConfig('CROSSWALK_TIME', CROSSWALK_TIME)
        self.config.setConfig('CARLANE_TIME', CARLANE_TIME)
        self.config.setConfig('CHANGE_TERM', CHANGE_TERM)

        self.crosswalkTime = self.config.getConfig()['CROSSWALK_TIME']
        self.carlaneTime = self.config.getConfig()['CARLANE_TIME']
        self.changeTerm = self.config.getConfig()['CHANGE_TERM']
        self.timeIncNormal = self.config.getConfig()['INCREASE_TIME_NORMAL']
        self.timeIncSpecial = self.config.getConfig()['INCREASE_TIME_SPECIAL']

    def Change_CrosswalkTime_Button_Event(self):
        """It is a function that is called when the user clicks the Change to pedestrian signal button on the GUI.
        """
        if self.isCarlaneTime is True and self.isCrosswalkTime is False:
            self.timeStack = self.changeTerm
        elif self.isCarlaneTime is False and self.isCrosswalkTime is True:
            self.timeStack = self.crosswalkTime

    def Change_CarTime_Button_Event(self):
        """This is a function that is called when the user clicks
        the Change to Vehicle Driving Signal button on the GUI.
        """
        self.startCarlane()

    def Left_Camera_Crosswalk_Button_Event(self):
        """This is an event function that is called when the user clicks
        the reset left camera crosswalk area button on the GUI.
        """
        self.stopCamera()
        self.stop_Timer()
        setup = CameraSetup(self.config.getConfig()['LEFT_CAMERA_NUMBER'])
        result = setup.runSetup()
        self.config.setConfig('LEFT_CAMERA_CROSSWALK_POS', result)
        self.refreshCamera()
        self.start_Timer()

    def Right_Camera_Crosswalk_Button_Event(self):
        """This is an event function that is called when the user clicks
        the reset right camera crosswalk area button on the GUI.
        """
        self.stopCamera()
        self.stop_Timer()
        setup = CameraSetup(self.config.getConfig()['RIGHT_CAMERA_NUMBER'])
        result = setup.runSetup()
        self.config.setConfig('RIGHT_CAMERA_CROSSWALK_POS', result)
        self.refreshCamera()
        self.start_Timer()

    def Left_Camera_Carlane_Button_Event(self):
        """This is an event function that is called when the user clicks
        the reset left camera vehicle zone button on the GUI.
        """
        self.stopCamera()
        self.stop_Timer()
        setup = CameraSetup(self.config.getConfig()['LEFT_CAMERA_NUMBER'])
        result = setup.runSetup()
        self.config.setConfig('LEFT_CAMERA_CARLANE_POS', result)
        self.refreshCamera()
        self.start_Timer()

    def Right_Camera_Carlane_Button_Event(self):
        """This is an event function that is called when the user clicks
        the reset right camera vehicle zone button on the GUI.
        """
        self.stopCamera()
        self.stop_Timer()
        setup = CameraSetup(self.config.getConfig()['RIGHT_CAMERA_NUMBER'])
        result = setup.runSetup()
        self.config.setConfig('RIGHT_CAMERA_CARLANE_POS', result)
        self.refreshCamera()
        self.start_Timer()

    # ============================= TIMER ===============================

    def TimerMethod(self):
        """This function manages the actual traffic light time and outputs signals according to emergencies.
        """
        while self.isTimerRun:
            # Initialize
            if self.isCarlaneTime is False and self.isCrosswalkTime is False:
                self.startCarlane()

            # Emergency handling part.
            if self.Emergency_Ambulance or self.Emergency_Person or self.Emergency_DisablePerson:

                self.timeStack -= 1
                self.changeTimer(self.timeStack)
                time.sleep(1)

                if self.Emergency_Ambulance is True:
                    if self.timeStack <= self.changeTerm and self.isCrosswalkTime is False and self.isCarlaneTime:
                        self.timeStack = self.changeTerm

                elif self.timeStack <= 0:
                    if self.Emergency_DisablePerson:
                        self.timeStack = self.timeIncSpecial
                    elif self.Emergency_Person:
                        self.timeStack = self.timeIncNormal

                    self.crosswalk_TurnRed_On()
                    self.crosswalk_TurnGreen_Off()
                    for i in range(0, self.timeStack):
                        self.timeStack -= 1
                        self.changeTimer(self.timeStack)
                        time.sleep(1)

                if self.timeStack <= 0:
                    if self.isCrosswalkTime is False and self.isCarlaneTime is True:
                        self.startCrosswalk()

                    elif self.isCrosswalkTime is True and self.isCarlaneTime is False:
                        self.startCarlane()

                    self.Emergency_DisablePerson = False
                    self.Emergency_Person = False

                continue

            # if timer == 0
            if self.timeStack <= 0:
                self.carlane_TurnYellow_Off()
                # When the driving signal is over,
                if self.isCarlaneTime is True and self.isCrosswalkTime is False:
                    self.startCrosswalk()

                # When the pedestrian signal time is over
                elif self.isCarlaneTime is False and self.isCrosswalkTime is True:
                    self.startCarlane()

            # If the signal time is equal to or less than the yellow signal time,
            # the current signal is output as the yellow signal.
            if 0 < self.timeStack <= self.changeTerm and \
                    self.isCrosswalkTime is False and self.isCarlaneTime is True:
                self.carlane_TurnRed_Off()
                self.carlane_TurnYellow_On()
                self.carlane_TurnGreen_Off()

            # Timer reduction and time output to GUI.
            self.timeStack -= 1
            self.changeTimer(self.timeStack)
            time.sleep(1)

        # Close Traffic Signal Timer
        self.isCrosswalkTime = False
        self.isCarlaneTime = False

        self.carlane_TurnRed_Off()
        self.carlane_TurnYellow_Off()
        self.carlane_TurnGreen_Off()

        self.crosswalk_TurnRed_Off()
        self.crosswalk_TurnGreen_Off()

    def startCrosswalk(self):
        """This function actually changes the signal to the vehicle driving time and reflects it in the GUI.
        """
        self.carlane_TurnRed_On()
        self.carlane_TurnGreen_Off()

        self.crosswalk_TurnGreen_On()
        self.crosswalk_TurnRed_Off()

        self.timeStack = self.crosswalkTime
        self.isCarlaneTime = False
        self.isCrosswalkTime = True

    def startCarlane(self):
        """This function actually changes the signal to pedestrian time and reflects it in the GUI.
        """
        self.carlane_TurnRed_Off()
        self.carlane_TurnGreen_On()

        self.crosswalk_TurnGreen_Off()
        self.crosswalk_TurnRed_On()

        self.timeStack = self.carlaneTime
        self.isCarlaneTime = True
        self.isCrosswalkTime = False

    def stop_Timer(self):
        """This function is a function that stops the traffic light timer process.
        """
        self.isTimerRun = False
        self.TimerLabel.setText('X')

    def start_Timer(self):
        """This function is a function that starts the traffic light timer process.
        """
        if self.timerThread.is_alive() is True:
            return
        self.timerThread = threading.Thread(target=self.TimerMethod)
        self.isTimerRun = True
        self.timerThread.start()

    def changeTimer(self, num):
        """This function is a function that changes the traffic light time displayed on the GUI.
        """
        self.TimerLabel.setText(str(num + 1))

    # ====================  SIREN DETECTOR  ======================
    def startSirenDetector(self):
        """This function is a function that activates the SirenDetector
        to detect the siren sound of an emergency vehicle.
        """
        self.stopSirenDetector()
        self.SirenDetector.start()

    def stopSirenDetector(self):
        """This function is a function that stops the SirenDetector to detect the siren sound of an emergency vehicle.
        """
        if self.SirenDetector.isRun is True:
            self.SirenDetector.stop()


def start(IP, PORT):
    """This function is called from Client.py to run a client program.
    """

    Camera.DETECTOR_SERVER_IP = IP
    Camera.DETECTOR_SERVER_PORT = PORT

    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    app = QApplication(sys.argv)
    window = Main()
    app.exec_()
