# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MAINPAGE_UIiFnbok.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2extn.RoundProgressBar import roundProgressBar
from PySide2extn.SpiralProgressBar import spiralProgressBar

import assets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(868, 718)
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Header_frame = QFrame(self.centralwidget)
        self.Header_frame.setObjectName(u"Header_frame")
        self.Header_frame.setStyleSheet(u"#Header_frame{\n"
"border:3px solid #22a7f2;\n"
"border-radius:10px;\n"
"padding: 0 8px; \n"
"margin:12px;\n"
"}")
        self.Header_frame.setFrameShape(QFrame.NoFrame)
        self.Header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.Header_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Header_left_frame = QFrame(self.Header_frame)
        self.Header_left_frame.setObjectName(u"Header_left_frame")
        font1 = QFont()
        font1.setFamily(u"Arial Rounded MT Bold")
        font1.setPointSize(20)
        font1.setUnderline(True)
        self.Header_left_frame.setFont(font1)
        self.Header_left_frame.setFrameShape(QFrame.StyledPanel)
        self.Header_left_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.Header_left_frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.menu = QPushButton(self.Header_left_frame)
        self.menu.setObjectName(u"menu")
        font2 = QFont()
        font2.setFamily(u"Arial Rounded MT Bold")
        font2.setPointSize(20)
        font2.setBold(False)
        font2.setWeight(50)
        self.menu.setFont(font2)
        self.menu.setStyleSheet(u"*{\n"
"border:none\n"
"}")
        icon = QIcon()
        icon.addFile(u":/black/icons/black/align-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.menu.setIcon(icon)
        self.menu.setIconSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.menu, 0, Qt.AlignLeft)


        self.horizontalLayout.addWidget(self.Header_left_frame)

        self.Header_center_frame = QFrame(self.Header_frame)
        self.Header_center_frame.setObjectName(u"Header_center_frame")
        self.Header_center_frame.setFrameShape(QFrame.StyledPanel)
        self.Header_center_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.Header_center_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.Header_center_frame)
        self.label_2.setObjectName(u"label_2")
        font3 = QFont()
        font3.setFamily(u"Arial Rounded MT Bold")
        font3.setPointSize(20)
        font3.setBold(False)
        font3.setUnderline(True)
        font3.setWeight(50)
        self.label_2.setFont(font3)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)


        self.horizontalLayout.addWidget(self.Header_center_frame)

        self.Header_right_frame = QFrame(self.Header_frame)
        self.Header_right_frame.setObjectName(u"Header_right_frame")
        self.Header_right_frame.setMinimumSize(QSize(0, 0))
        self.Header_right_frame.setStyleSheet(u"*{\n"
"border:none;\n"
"}")
        self.Header_right_frame.setFrameShape(QFrame.StyledPanel)
        self.Header_right_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.Header_right_frame)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Minimize_window_button = QPushButton(self.Header_right_frame)
        self.Minimize_window_button.setObjectName(u"Minimize_window_button")
        self.Minimize_window_button.setMinimumSize(QSize(30, 30))
        icon1 = QIcon()
        icon1.addFile(u":/menu/icons/menu/minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Minimize_window_button.setIcon(icon1)
        self.Minimize_window_button.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.Minimize_window_button)

        self.Restore_window_button = QPushButton(self.Header_right_frame)
        self.Restore_window_button.setObjectName(u"Restore_window_button")
        self.Restore_window_button.setMinimumSize(QSize(30, 30))
        icon2 = QIcon()
        icon2.addFile(u":/black/icons/black/maximize-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Restore_window_button.setIcon(icon2)
        self.Restore_window_button.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.Restore_window_button)

        self.Close_window_button = QPushButton(self.Header_right_frame)
        self.Close_window_button.setObjectName(u"Close_window_button")
        self.Close_window_button.setMinimumSize(QSize(30, 30))
        icon3 = QIcon()
        icon3.addFile(u":/menu/icons/menu/close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Close_window_button.setIcon(icon3)
        self.Close_window_button.setIconSize(QSize(16, 16))

        self.horizontalLayout_2.addWidget(self.Close_window_button)


        self.horizontalLayout.addWidget(self.Header_right_frame, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.Header_frame)

        self.Main_body_frame = QFrame(self.centralwidget)
        self.Main_body_frame.setObjectName(u"Main_body_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Main_body_frame.sizePolicy().hasHeightForWidth())
        self.Main_body_frame.setSizePolicy(sizePolicy)
        self.Main_body_frame.setFrameShape(QFrame.StyledPanel)
        self.Main_body_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.Main_body_frame)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.Left_menu_cont_frame = QFrame(self.Main_body_frame)
        self.Left_menu_cont_frame.setObjectName(u"Left_menu_cont_frame")
        self.Left_menu_cont_frame.setMinimumSize(QSize(110, 0))
        self.Left_menu_cont_frame.setMaximumSize(QSize(65, 16777215))
        self.Left_menu_cont_frame.setFrameShape(QFrame.StyledPanel)
        self.Left_menu_cont_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.Left_menu_cont_frame)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.menu_frame = QFrame(self.Left_menu_cont_frame)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setMinimumSize(QSize(200, 0))
        self.menu_frame.setStyleSheet(u"#menu_frame{\n"
"background-color:rgba(68, 138, 255,80%);\n"
"border-radius:7px;\n"
"padding: 0 8px;\n"
"margin:1px;\n"
"}\n"
"#CPU_btn,#Disk_btn,#GPU_btn,#RAM_btn,#System_info,#Wifi_btn,#act_btn,#battery_btn,#sensor_btn,#all_btn{\n"
"background-color:rgba(79, 91, 98,80%);\n"
"border:1.5px solid black;\n"
"padding: 0 8px;\n"
"margin:1px;\n"
"\n"
"}")
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.menu_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.all_btn = QPushButton(self.menu_frame)
        self.all_btn.setObjectName(u"all_btn")
        self.all_btn.setMinimumSize(QSize(0, 36))
        icon4 = QIcon()
        icon4.addFile(u":/black/icons/black/codesandbox.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.all_btn.setIcon(icon4)
        self.all_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.all_btn, 0, 0, 1, 1)

        self.CPU_btn = QPushButton(self.menu_frame)
        self.CPU_btn.setObjectName(u"CPU_btn")
        icon5 = QIcon()
        icon5.addFile(u":/black/icons/black/cpu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CPU_btn.setIcon(icon5)
        self.CPU_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.CPU_btn, 1, 0, 1, 1)

        self.label_3 = QLabel(self.menu_frame)
        self.label_3.setObjectName(u"label_3")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        font4.setWeight(75)
        self.label_3.setFont(font4)

        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)

        self.RAM_btn = QPushButton(self.menu_frame)
        self.RAM_btn.setObjectName(u"RAM_btn")
        icon6 = QIcon()
        icon6.addFile(u":/menu/icons/menu/ram.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.RAM_btn.setIcon(icon6)
        self.RAM_btn.setIconSize(QSize(40, 40))

        self.gridLayout.addWidget(self.RAM_btn, 2, 0, 1, 1)

        self.label_4 = QLabel(self.menu_frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font4)

        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)

        self.Disk_btn = QPushButton(self.menu_frame)
        self.Disk_btn.setObjectName(u"Disk_btn")
        icon7 = QIcon()
        icon7.addFile(u":/menu/icons/menu/disk.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Disk_btn.setIcon(icon7)
        self.Disk_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.Disk_btn, 3, 0, 1, 1)

        self.label_5 = QLabel(self.menu_frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font4)

        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)

        self.Wifi_btn = QPushButton(self.menu_frame)
        self.Wifi_btn.setObjectName(u"Wifi_btn")
        icon8 = QIcon()
        icon8.addFile(u":/black/icons/black/wifi.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Wifi_btn.setIcon(icon8)
        self.Wifi_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.Wifi_btn, 4, 0, 1, 1)

        self.label_6 = QLabel(self.menu_frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font4)

        self.gridLayout.addWidget(self.label_6, 4, 1, 1, 1)

        self.GPU_btn = QPushButton(self.menu_frame)
        self.GPU_btn.setObjectName(u"GPU_btn")
        icon9 = QIcon()
        icon9.addFile(u":/menu/icons/menu/gpu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.GPU_btn.setIcon(icon9)
        self.GPU_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.GPU_btn, 5, 0, 1, 1)

        self.label_7 = QLabel(self.menu_frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font4)

        self.gridLayout.addWidget(self.label_7, 5, 1, 1, 1)

        self.System_info = QPushButton(self.menu_frame)
        self.System_info.setObjectName(u"System_info")
        icon10 = QIcon()
        icon10.addFile(u":/black/icons/black/monitor.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.System_info.setIcon(icon10)
        self.System_info.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.System_info, 6, 0, 1, 1)

        self.label_8 = QLabel(self.menu_frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font4)

        self.gridLayout.addWidget(self.label_8, 6, 1, 1, 1)

        self.act_btn = QPushButton(self.menu_frame)
        self.act_btn.setObjectName(u"act_btn")
        self.act_btn.setMaximumSize(QSize(16777215, 16777215))
        icon11 = QIcon()
        icon11.addFile(u":/black/icons/black/activity.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.act_btn.setIcon(icon11)
        self.act_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.act_btn, 7, 0, 1, 1)

        self.label_9 = QLabel(self.menu_frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font4)

        self.gridLayout.addWidget(self.label_9, 7, 1, 1, 1)

        self.sensor_btn = QPushButton(self.menu_frame)
        self.sensor_btn.setObjectName(u"sensor_btn")
        icon12 = QIcon()
        icon12.addFile(u":/black/icons/black/thermometer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.sensor_btn.setIcon(icon12)
        self.sensor_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.sensor_btn, 8, 0, 1, 1)

        self.label_10 = QLabel(self.menu_frame)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font4)

        self.gridLayout.addWidget(self.label_10, 8, 1, 1, 1)

        self.battery_btn = QPushButton(self.menu_frame)
        self.battery_btn.setObjectName(u"battery_btn")
        icon13 = QIcon()
        icon13.addFile(u":/black/icons/black/battery-charging.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.battery_btn.setIcon(icon13)
        self.battery_btn.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.battery_btn, 9, 0, 1, 1)

        self.label_27 = QLabel(self.menu_frame)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font4)

        self.gridLayout.addWidget(self.label_27, 9, 1, 1, 1)


        self.verticalLayout_10.addWidget(self.menu_frame)


        self.horizontalLayout_8.addWidget(self.Left_menu_cont_frame)

        self.right_frame = QFrame(self.Main_body_frame)
        self.right_frame.setObjectName(u"right_frame")
        self.right_frame.setStyleSheet(u"#label_71,#label_70,#label_50,#label_52,#label_69,#label_37,#label_49,#label_51,#label_28{\n"
"border:3px solid #22a7f2;\n"
"border-radius:5px;\n"
"padding: 0 1px; \n"
"margin:4px\n"
"}\n"
"#cpu_percentage,#ram_percentage,#battery_usage{\n"
"border:7px solid #22a7f2;\n"
"border-radius:60px;\n"
"width:400px;\n"
"height:400px;\n"
"padding: 0 1px; \n"
"margin:4px\n"
"}\n"
"#all_battery,#all_cpu,#all_gpu,#all_net,#all_ram,#label_38,#label_43,#label_42,#label_33,#label_57{border:3px solid #22a7f2;\n"
"border-radius:5px;\n"
"padding: 0 1px; \n"
"margin:4px}")
        self.right_frame.setFrameShape(QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.right_frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stackedWidget = QStackedWidget(self.right_frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        font5 = QFont()
        font5.setPointSize(14)
        self.stackedWidget.setFont(font5)
        self.stackedWidget.setStyleSheet(u"#stackedWidget{\n"
"border:3px solid #22a7f2;\n"
"border-radius:10px;\n"
"padding: 0 8px; \n"
"}\n"
"")
        self.cpu_and_bat = QWidget()
        self.cpu_and_bat.setObjectName(u"cpu_and_bat")
        self.verticalLayout_3 = QVBoxLayout(self.cpu_and_bat)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_71 = QLabel(self.cpu_and_bat)
        self.label_71.setObjectName(u"label_71")
        self.label_71.setMinimumSize(QSize(0, 40))
        font6 = QFont()
        font6.setPointSize(18)
        font6.setBold(True)
        font6.setUnderline(True)
        font6.setWeight(75)
        self.label_71.setFont(font6)

        self.verticalLayout_3.addWidget(self.label_71)

        self.cpu_info_frame = QFrame(self.cpu_and_bat)
        self.cpu_info_frame.setObjectName(u"cpu_info_frame")
        self.cpu_info_frame.setFrameShape(QFrame.StyledPanel)
        self.cpu_info_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.cpu_info_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cpu_per = QLabel(self.cpu_info_frame)
        self.cpu_per.setObjectName(u"cpu_per")
        sizePolicy.setHeightForWidth(self.cpu_per.sizePolicy().hasHeightForWidth())
        self.cpu_per.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setFamily(u"Arial Rounded MT Bold")
        font7.setPointSize(14)
        self.cpu_per.setFont(font7)

        self.gridLayout_2.addWidget(self.cpu_per, 1, 1, 1, 1)

        self.label_11 = QLabel(self.cpu_info_frame)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setFont(font7)

        self.gridLayout_2.addWidget(self.label_11, 2, 0, 1, 1)

        self.label_14 = QLabel(self.cpu_info_frame)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setFont(font7)

        self.gridLayout_2.addWidget(self.label_14, 0, 0, 1, 1)

        self.cpu_count = QLabel(self.cpu_info_frame)
        self.cpu_count.setObjectName(u"cpu_count")
        sizePolicy.setHeightForWidth(self.cpu_count.sizePolicy().hasHeightForWidth())
        self.cpu_count.setSizePolicy(sizePolicy)
        self.cpu_count.setFont(font7)

        self.gridLayout_2.addWidget(self.cpu_count, 0, 1, 1, 1)

        self.label_13 = QLabel(self.cpu_info_frame)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setFont(font7)

        self.gridLayout_2.addWidget(self.label_13, 1, 0, 1, 1)

        self.cpu_main_core = QLabel(self.cpu_info_frame)
        self.cpu_main_core.setObjectName(u"cpu_main_core")
        sizePolicy.setHeightForWidth(self.cpu_main_core.sizePolicy().hasHeightForWidth())
        self.cpu_main_core.setSizePolicy(sizePolicy)
        self.cpu_main_core.setFont(font7)

        self.gridLayout_2.addWidget(self.cpu_main_core, 2, 1, 1, 1)

        self.cpu_percentage = roundProgressBar(self.cpu_info_frame)
        self.cpu_percentage.setObjectName(u"cpu_percentage")
        self.cpu_percentage.setMinimumSize(QSize(300, 300))
        font8 = QFont()
        font8.setPointSize(17)
        self.cpu_percentage.setFont(font8)

        self.gridLayout_2.addWidget(self.cpu_percentage, 1, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.cpu_info_frame)

        self.stackedWidget.addWidget(self.cpu_and_bat)
        self.memory = QWidget()
        self.memory.setObjectName(u"memory")
        self.verticalLayout_4 = QVBoxLayout(self.memory)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_70 = QLabel(self.memory)
        self.label_70.setObjectName(u"label_70")
        self.label_70.setMinimumSize(QSize(0, 40))
        self.label_70.setFont(font6)

        self.verticalLayout_4.addWidget(self.label_70, 0, Qt.AlignTop)

        self.ram_info = QFrame(self.memory)
        self.ram_info.setObjectName(u"ram_info")
        sizePolicy.setHeightForWidth(self.ram_info.sizePolicy().hasHeightForWidth())
        self.ram_info.setSizePolicy(sizePolicy)
        self.ram_info.setFrameShape(QFrame.StyledPanel)
        self.ram_info.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.ram_info)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.free_ram = QLabel(self.ram_info)
        self.free_ram.setObjectName(u"free_ram")
        self.free_ram.setFont(font7)

        self.gridLayout_3.addWidget(self.free_ram, 3, 1, 1, 1)

        self.total_ram = QLabel(self.ram_info)
        self.total_ram.setObjectName(u"total_ram")
        self.total_ram.setFont(font7)

        self.gridLayout_3.addWidget(self.total_ram, 0, 1, 1, 1)

        self.label_21 = QLabel(self.ram_info)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font7)

        self.gridLayout_3.addWidget(self.label_21, 4, 0, 1, 1)

        self.ram_usage = QLabel(self.ram_info)
        self.ram_usage.setObjectName(u"ram_usage")
        self.ram_usage.setFont(font7)

        self.gridLayout_3.addWidget(self.ram_usage, 4, 1, 1, 1)

        self.label_17 = QLabel(self.ram_info)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font7)

        self.gridLayout_3.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_20 = QLabel(self.ram_info)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font7)

        self.gridLayout_3.addWidget(self.label_20, 3, 0, 1, 1)

        self.used_ram = QLabel(self.ram_info)
        self.used_ram.setObjectName(u"used_ram")
        self.used_ram.setFont(font7)

        self.gridLayout_3.addWidget(self.used_ram, 2, 1, 1, 1)

        self.label_18 = QLabel(self.ram_info)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font7)

        self.gridLayout_3.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_19 = QLabel(self.ram_info)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font7)

        self.gridLayout_3.addWidget(self.label_19, 2, 0, 1, 1)

        self.available_ram = QLabel(self.ram_info)
        self.available_ram.setObjectName(u"available_ram")
        self.available_ram.setFont(font7)

        self.gridLayout_3.addWidget(self.available_ram, 1, 1, 1, 1)

        self.ram_percentage = spiralProgressBar(self.ram_info)
        self.ram_percentage.setObjectName(u"ram_percentage")
        self.ram_percentage.setMinimumSize(QSize(300, 300))

        self.gridLayout_3.addWidget(self.ram_percentage, 1, 2, 2, 1)


        self.verticalLayout_4.addWidget(self.ram_info)

        self.stackedWidget.addWidget(self.memory)
        self.rom = QWidget()
        self.rom.setObjectName(u"rom")
        self.verticalLayout_7 = QVBoxLayout(self.rom)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_50 = QLabel(self.rom)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(0, 40))
        font9 = QFont()
        font9.setFamily(u"Arial Rounded MT Bold")
        font9.setPointSize(18)
        font9.setUnderline(True)
        self.label_50.setFont(font9)

        self.verticalLayout_7.addWidget(self.label_50)

        self.store_table = QTableWidget(self.rom)
        if (self.store_table.columnCount() < 9):
            self.store_table.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.store_table.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.store_table.setObjectName(u"store_table")
        self.store_table.setFont(font7)

        self.verticalLayout_7.addWidget(self.store_table)

        self.stackedWidget.addWidget(self.rom)
        self.network = QWidget()
        self.network.setObjectName(u"network")
        self.horizontalLayout_13 = QHBoxLayout(self.network)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.frame_8 = QFrame(self.network)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.frame_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_55 = QLabel(self.frame_8)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFont(font7)

        self.gridLayout_8.addWidget(self.label_55, 3, 0, 1, 1)

        self.upspeed = QLabel(self.frame_8)
        self.upspeed.setObjectName(u"upspeed")
        self.upspeed.setFont(font7)

        self.gridLayout_8.addWidget(self.upspeed, 1, 1, 1, 1)

        self.label_54 = QLabel(self.frame_8)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setFont(font7)

        self.gridLayout_8.addWidget(self.label_54, 2, 0, 1, 1)

        self.totalspeed = QLabel(self.frame_8)
        self.totalspeed.setObjectName(u"totalspeed")
        self.totalspeed.setFont(font7)

        self.gridLayout_8.addWidget(self.totalspeed, 3, 1, 1, 1)

        self.label_52 = QLabel(self.frame_8)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setMinimumSize(QSize(0, 40))
        font10 = QFont()
        font10.setFamily(u"Arial Black")
        font10.setPointSize(16)
        font10.setBold(True)
        font10.setUnderline(True)
        font10.setWeight(75)
        self.label_52.setFont(font10)

        self.gridLayout_8.addWidget(self.label_52, 0, 0, 1, 1, Qt.AlignTop)

        self.label_53 = QLabel(self.frame_8)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFont(font7)

        self.gridLayout_8.addWidget(self.label_53, 1, 0, 1, 1)

        self.downloadspeed = QLabel(self.frame_8)
        self.downloadspeed.setObjectName(u"downloadspeed")
        self.downloadspeed.setFont(font7)

        self.gridLayout_8.addWidget(self.downloadspeed, 2, 1, 1, 1)

        self.label_15 = QLabel(self.frame_8)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font7)

        self.gridLayout_8.addWidget(self.label_15, 4, 0, 1, 1)

        self.ping = QLabel(self.frame_8)
        self.ping.setObjectName(u"ping")
        self.ping.setFont(font7)

        self.gridLayout_8.addWidget(self.ping, 4, 1, 1, 1)

        self.refresh_btn = QPushButton(self.frame_8)
        self.refresh_btn.setObjectName(u"refresh_btn")
        font11 = QFont()
        font11.setFamily(u"Arial")
        font11.setPointSize(12)
        font11.setBold(True)
        font11.setWeight(75)
        self.refresh_btn.setFont(font11)
        icon14 = QIcon()
        icon14.addFile(u":/black/icons/black/refresh-cw.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.refresh_btn.setIcon(icon14)

        self.gridLayout_8.addWidget(self.refresh_btn, 0, 1, 1, 1, Qt.AlignRight)


        self.horizontalLayout_13.addWidget(self.frame_8)

        self.stackedWidget.addWidget(self.network)
        self.gpu = QWidget()
        self.gpu.setObjectName(u"gpu")
        self.verticalLayout_9 = QVBoxLayout(self.gpu)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_69 = QLabel(self.gpu)
        self.label_69.setObjectName(u"label_69")
        self.label_69.setMinimumSize(QSize(0, 40))
        font12 = QFont()
        font12.setFamily(u"Bahnschrift SemiBold SemiConden")
        font12.setPointSize(22)
        font12.setBold(True)
        font12.setUnderline(True)
        font12.setWeight(75)
        self.label_69.setFont(font12)

        self.verticalLayout_9.addWidget(self.label_69, 0, Qt.AlignTop)

        self.frame_9 = QFrame(self.gpu)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.frame_9)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.totalmemory = QLabel(self.frame_9)
        self.totalmemory.setObjectName(u"totalmemory")
        font13 = QFont()
        font13.setFamily(u"Arial Rounded MT Bold")
        font13.setPointSize(14)
        font13.setBold(False)
        font13.setWeight(50)
        self.totalmemory.setFont(font13)

        self.gridLayout_9.addWidget(self.totalmemory, 0, 1, 1, 1)

        self.freememory = QLabel(self.frame_9)
        self.freememory.setObjectName(u"freememory")
        self.freememory.setFont(font13)

        self.gridLayout_9.addWidget(self.freememory, 2, 1, 1, 1)

        self.label_62 = QLabel(self.frame_9)
        self.label_62.setObjectName(u"label_62")
        self.label_62.setFont(font13)

        self.gridLayout_9.addWidget(self.label_62, 3, 0, 1, 1)

        self.label_60 = QLabel(self.frame_9)
        self.label_60.setObjectName(u"label_60")
        self.label_60.setFont(font13)

        self.gridLayout_9.addWidget(self.label_60, 1, 0, 1, 1)

        self.temperature = QLabel(self.frame_9)
        self.temperature.setObjectName(u"temperature")
        self.temperature.setFont(font13)

        self.gridLayout_9.addWidget(self.temperature, 4, 1, 1, 1)

        self.label_59 = QLabel(self.frame_9)
        self.label_59.setObjectName(u"label_59")
        self.label_59.setFont(font13)

        self.gridLayout_9.addWidget(self.label_59, 0, 0, 1, 1)

        self.usedmemory = QLabel(self.frame_9)
        self.usedmemory.setObjectName(u"usedmemory")
        self.usedmemory.setFont(font13)

        self.gridLayout_9.addWidget(self.usedmemory, 1, 1, 1, 1)

        self.label_67 = QLabel(self.frame_9)
        self.label_67.setObjectName(u"label_67")
        self.label_67.setFont(font13)

        self.gridLayout_9.addWidget(self.label_67, 4, 0, 1, 1)

        self.label_61 = QLabel(self.frame_9)
        self.label_61.setObjectName(u"label_61")
        self.label_61.setFont(font13)

        self.gridLayout_9.addWidget(self.label_61, 2, 0, 1, 1)

        self.loadd = QLabel(self.frame_9)
        self.loadd.setObjectName(u"loadd")
        self.loadd.setFont(font13)

        self.gridLayout_9.addWidget(self.loadd, 3, 1, 1, 1)

        self.gpu_per = roundProgressBar(self.frame_9)
        self.gpu_per.setObjectName(u"gpu_per")
        self.gpu_per.setMinimumSize(QSize(300, 300))

        self.gridLayout_9.addWidget(self.gpu_per, 1, 2, 1, 1)


        self.verticalLayout_9.addWidget(self.frame_9)

        self.stackedWidget.addWidget(self.gpu)
        self.system_info = QWidget()
        self.system_info.setObjectName(u"system_info")
        self.gridLayout_7 = QGridLayout(self.system_info)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame_3 = QFrame(self.system_info)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.system_platform = QLabel(self.frame_3)
        self.system_platform.setObjectName(u"system_platform")
        self.system_platform.setFont(font7)

        self.gridLayout_5.addWidget(self.system_platform, 2, 1, 1, 1)

        self.system_system = QLabel(self.frame_3)
        self.system_system.setObjectName(u"system_system")
        self.system_system.setFont(font7)

        self.gridLayout_5.addWidget(self.system_system, 1, 0, 1, 1)

        self.label_45 = QLabel(self.frame_3)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font7)

        self.gridLayout_5.addWidget(self.label_45, 8, 0, 1, 1)

        self.label_39 = QLabel(self.frame_3)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font7)

        self.gridLayout_5.addWidget(self.label_39, 2, 0, 1, 1)

        self.system_processor = QLabel(self.frame_3)
        self.system_processor.setObjectName(u"system_processor")
        self.system_processor.setFont(font7)

        self.gridLayout_5.addWidget(self.system_processor, 7, 1, 1, 1)

        self.label_40 = QLabel(self.frame_3)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font7)

        self.gridLayout_5.addWidget(self.label_40, 3, 0, 1, 1)

        self.system_version = QLabel(self.frame_3)
        self.system_version.setObjectName(u"system_version")
        self.system_version.setFont(font7)

        self.gridLayout_5.addWidget(self.system_version, 3, 1, 1, 1)

        self.label_41 = QLabel(self.frame_3)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setFont(font7)

        self.gridLayout_5.addWidget(self.label_41, 4, 0, 1, 1)

        self.label_46 = QLabel(self.frame_3)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font7)

        self.gridLayout_5.addWidget(self.label_46, 7, 0, 1, 1)

        self.system_date = QLabel(self.frame_3)
        self.system_date.setObjectName(u"system_date")
        self.system_date.setFont(font7)

        self.gridLayout_5.addWidget(self.system_date, 4, 1, 1, 1)

        self.system_time = QLabel(self.frame_3)
        self.system_time.setObjectName(u"system_time")
        self.system_time.setFont(font7)

        self.gridLayout_5.addWidget(self.system_time, 8, 1, 1, 1)

        self.label_37 = QLabel(self.frame_3)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setMinimumSize(QSize(0, 40))
        self.label_37.setFont(font6)

        self.gridLayout_5.addWidget(self.label_37, 0, 0, 1, 1)

        self.label_12 = QLabel(self.frame_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font7)

        self.gridLayout_5.addWidget(self.label_12, 5, 0, 1, 1)

        self.system_machine = QLabel(self.frame_3)
        self.system_machine.setObjectName(u"system_machine")
        self.system_machine.setFont(font7)

        self.gridLayout_5.addWidget(self.system_machine, 5, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_3, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.system_info)
        self.activity = QWidget()
        self.activity.setObjectName(u"activity")
        self.verticalLayout_2 = QVBoxLayout(self.activity)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_4 = QFrame(self.activity)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_49 = QLabel(self.frame_4)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(0, 40))
        font14 = QFont()
        font14.setFamily(u"Arial Rounded MT Bold")
        font14.setPointSize(18)
        font14.setBold(False)
        font14.setUnderline(True)
        font14.setWeight(50)
        font14.setStrikeOut(False)
        self.label_49.setFont(font14)

        self.horizontalLayout_10.addWidget(self.label_49)

        self.frame_7 = QFrame(self.frame_4)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(300, 0))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.activity_search = QLineEdit(self.frame_7)
        self.activity_search.setObjectName(u"activity_search")

        self.horizontalLayout_9.addWidget(self.activity_search)

        self.search = QPushButton(self.frame_7)
        self.search.setObjectName(u"search")
        self.search.setMinimumSize(QSize(30, 30))
        icon15 = QIcon()
        icon15.addFile(u":/black/icons/black/search.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.search.setIcon(icon15)

        self.horizontalLayout_9.addWidget(self.search)


        self.horizontalLayout_10.addWidget(self.frame_7, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.frame_4, 0, Qt.AlignTop)

        self.frame_5 = QFrame(self.activity)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.act_table = QTableWidget(self.frame_5)
        if (self.act_table.columnCount() < 8):
            self.act_table.setColumnCount(8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(6, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.act_table.setHorizontalHeaderItem(7, __qtablewidgetitem16)
        self.act_table.setObjectName(u"act_table")
        self.act_table.setFont(font7)

        self.verticalLayout_6.addWidget(self.act_table)


        self.verticalLayout_2.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.activity)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.pushButton_7 = QPushButton(self.frame_6)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setFont(font7)

        self.horizontalLayout_12.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.frame_6)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setFont(font7)

        self.horizontalLayout_12.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.frame_6)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setFont(font7)

        self.horizontalLayout_12.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.frame_6)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setFont(font7)

        self.horizontalLayout_12.addWidget(self.pushButton_10)


        self.verticalLayout_2.addWidget(self.frame_6, 0, Qt.AlignBottom)

        self.stackedWidget.addWidget(self.activity)
        self.sensor = QWidget()
        self.sensor.setObjectName(u"sensor")
        self.verticalLayout_8 = QVBoxLayout(self.sensor)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_51 = QLabel(self.sensor)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(0, 40))
        self.label_51.setFont(font6)

        self.verticalLayout_8.addWidget(self.label_51)

        self.sensor_table = QTableWidget(self.sensor)
        if (self.sensor_table.columnCount() < 6):
            self.sensor_table.setColumnCount(6)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.sensor_table.setHorizontalHeaderItem(0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.sensor_table.setHorizontalHeaderItem(1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.sensor_table.setHorizontalHeaderItem(2, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.sensor_table.setHorizontalHeaderItem(3, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.sensor_table.setHorizontalHeaderItem(4, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.sensor_table.setHorizontalHeaderItem(5, __qtablewidgetitem22)
        self.sensor_table.setObjectName(u"sensor_table")
        self.sensor_table.setFont(font7)

        self.verticalLayout_8.addWidget(self.sensor_table)

        self.stackedWidget.addWidget(self.sensor)
        self.battery = QWidget()
        self.battery.setObjectName(u"battery")
        self.gridLayout_10 = QGridLayout(self.battery)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.frame_2 = QFrame(self.battery)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QSize(0, 400))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.battery_time_left = QLabel(self.frame_2)
        self.battery_time_left.setObjectName(u"battery_time_left")
        self.battery_time_left.setFont(font7)

        self.gridLayout_4.addWidget(self.battery_time_left, 2, 1, 1, 1)

        self.battery_status = QLabel(self.frame_2)
        self.battery_status.setObjectName(u"battery_status")
        self.battery_status.setFont(font7)

        self.gridLayout_4.addWidget(self.battery_status, 0, 1, 1, 1)

        self.battery_charge = QLabel(self.frame_2)
        self.battery_charge.setObjectName(u"battery_charge")
        self.battery_charge.setFont(font7)

        self.gridLayout_4.addWidget(self.battery_charge, 1, 1, 1, 1)

        self.label_29 = QLabel(self.frame_2)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font7)

        self.gridLayout_4.addWidget(self.label_29, 0, 0, 1, 1)

        self.label_32 = QLabel(self.frame_2)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font7)

        self.gridLayout_4.addWidget(self.label_32, 3, 0, 1, 1)

        self.label_30 = QLabel(self.frame_2)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font7)

        self.gridLayout_4.addWidget(self.label_30, 1, 0, 1, 1)

        self.battery_plugged = QLabel(self.frame_2)
        self.battery_plugged.setObjectName(u"battery_plugged")
        self.battery_plugged.setFont(font7)

        self.gridLayout_4.addWidget(self.battery_plugged, 3, 1, 1, 1)

        self.label_31 = QLabel(self.frame_2)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font7)

        self.gridLayout_4.addWidget(self.label_31, 2, 0, 1, 1)


        self.gridLayout_10.addWidget(self.frame_2, 1, 0, 1, 1, Qt.AlignTop)

        self.battery_usage = roundProgressBar(self.battery)
        self.battery_usage.setObjectName(u"battery_usage")
        self.battery_usage.setMinimumSize(QSize(300, 300))
        self.battery_usage.setMaximumSize(QSize(400, 400))

        self.gridLayout_10.addWidget(self.battery_usage, 1, 1, 1, 1)

        self.label_28 = QLabel(self.battery)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setMinimumSize(QSize(0, 40))
        self.label_28.setFont(font6)

        self.gridLayout_10.addWidget(self.label_28, 0, 0, 1, 2)

        self.stackedWidget.addWidget(self.battery)
        self.all = QWidget()
        self.all.setObjectName(u"all")
        self.gridLayout_11 = QGridLayout(self.all)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.all_ram = QFrame(self.all)
        self.all_ram.setObjectName(u"all_ram")
        self.all_ram.setMinimumSize(QSize(400, 0))
        self.all_ram.setFrameShape(QFrame.StyledPanel)
        self.all_ram.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.all_ram)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_43 = QLabel(self.all_ram)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_14.addWidget(self.label_43, 0, 0, 1, 1)

        self.widget_3 = spiralProgressBar(self.all_ram)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(150, 150))

        self.gridLayout_14.addWidget(self.widget_3, 0, 1, 5, 1)

        self.label_44 = QLabel(self.all_ram)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_14.addWidget(self.label_44, 1, 0, 1, 1)

        self.label_47 = QLabel(self.all_ram)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_14.addWidget(self.label_47, 2, 0, 1, 1)

        self.label_48 = QLabel(self.all_ram)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_14.addWidget(self.label_48, 3, 0, 1, 1)

        self.label_56 = QLabel(self.all_ram)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_14.addWidget(self.label_56, 4, 0, 1, 1)


        self.gridLayout_11.addWidget(self.all_ram, 1, 0, 1, 2)

        self.all_battery = QFrame(self.all)
        self.all_battery.setObjectName(u"all_battery")
        self.all_battery.setMinimumSize(QSize(280, 0))
        self.all_battery.setFrameShape(QFrame.StyledPanel)
        self.all_battery.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.all_battery)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_57 = QLabel(self.all_battery)
        self.label_57.setObjectName(u"label_57")

        self.gridLayout_15.addWidget(self.label_57, 0, 0, 1, 1)

        self.widget_4 = roundProgressBar(self.all_battery)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(150, 150))

        self.gridLayout_15.addWidget(self.widget_4, 0, 1, 4, 1)

        self.label_58 = QLabel(self.all_battery)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_15.addWidget(self.label_58, 1, 0, 1, 1)

        self.label_63 = QLabel(self.all_battery)
        self.label_63.setObjectName(u"label_63")

        self.gridLayout_15.addWidget(self.label_63, 2, 0, 1, 1)

        self.label_64 = QLabel(self.all_battery)
        self.label_64.setObjectName(u"label_64")

        self.gridLayout_15.addWidget(self.label_64, 3, 0, 1, 1)


        self.gridLayout_11.addWidget(self.all_battery, 1, 2, 1, 2)

        self.all_net = QFrame(self.all)
        self.all_net.setObjectName(u"all_net")
        self.all_net.setMinimumSize(QSize(150, 0))
        self.all_net.setFrameShape(QFrame.StyledPanel)
        self.all_net.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.all_net)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_33 = QLabel(self.all_net)
        self.label_33.setObjectName(u"label_33")

        self.verticalLayout_5.addWidget(self.label_33)

        self.label_34 = QLabel(self.all_net)
        self.label_34.setObjectName(u"label_34")

        self.verticalLayout_5.addWidget(self.label_34)

        self.label_35 = QLabel(self.all_net)
        self.label_35.setObjectName(u"label_35")

        self.verticalLayout_5.addWidget(self.label_35)

        self.label_36 = QLabel(self.all_net)
        self.label_36.setObjectName(u"label_36")

        self.verticalLayout_5.addWidget(self.label_36)


        self.gridLayout_11.addWidget(self.all_net, 0, 3, 1, 1)

        self.all_cpu = QFrame(self.all)
        self.all_cpu.setObjectName(u"all_cpu")
        self.all_cpu.setMinimumSize(QSize(265, 0))
        self.all_cpu.setFrameShape(QFrame.StyledPanel)
        self.all_cpu.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.all_cpu)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_23 = QLabel(self.all_cpu)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_12.addWidget(self.label_23, 3, 0, 1, 1)

        self.label_16 = QLabel(self.all_cpu)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_12.addWidget(self.label_16, 1, 0, 1, 1)

        self.label_22 = QLabel(self.all_cpu)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_12.addWidget(self.label_22, 2, 0, 1, 1)

        self.label_38 = QLabel(self.all_cpu)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_12.addWidget(self.label_38, 0, 0, 1, 1)

        self.widget = roundProgressBar(self.all_cpu)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(150, 150))

        self.gridLayout_12.addWidget(self.widget, 0, 1, 4, 1)


        self.gridLayout_11.addWidget(self.all_cpu, 0, 0, 1, 1)

        self.all_gpu = QFrame(self.all)
        self.all_gpu.setObjectName(u"all_gpu")
        self.all_gpu.setMinimumSize(QSize(250, 0))
        self.all_gpu.setFrameShape(QFrame.StyledPanel)
        self.all_gpu.setFrameShadow(QFrame.Raised)
        self.gridLayout_13 = QGridLayout(self.all_gpu)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_26 = QLabel(self.all_gpu)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_13.addWidget(self.label_26, 3, 0, 1, 1)

        self.label_25 = QLabel(self.all_gpu)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_13.addWidget(self.label_25, 2, 0, 1, 1)

        self.label_24 = QLabel(self.all_gpu)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_13.addWidget(self.label_24, 1, 0, 1, 1)

        self.label_42 = QLabel(self.all_gpu)
        self.label_42.setObjectName(u"label_42")

        self.gridLayout_13.addWidget(self.label_42, 0, 0, 1, 1)

        self.widget_2 = roundProgressBar(self.all_gpu)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(150, 150))

        self.gridLayout_13.addWidget(self.widget_2, 0, 1, 4, 1)


        self.gridLayout_11.addWidget(self.all_gpu, 0, 1, 1, 2)

        self.stackedWidget.addWidget(self.all)

        self.gridLayout_6.addWidget(self.stackedWidget, 0, 1, 1, 1)


        self.horizontalLayout_8.addWidget(self.right_frame)


        self.verticalLayout.addWidget(self.Main_body_frame)

        self.Footer_frame = QFrame(self.centralwidget)
        self.Footer_frame.setObjectName(u"Footer_frame")
        self.Footer_frame.setStyleSheet(u"#Footer_frame{\n"
"border:3px solid #22a7f2;\n"
"border-radius:10px;\n"
"padding: 0 8px; \n"
"margin:10px\n"
"}")
        self.Footer_frame.setFrameShape(QFrame.NoFrame)
        self.Footer_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.Footer_frame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.footer_left_frame = QFrame(self.Footer_frame)
        self.footer_left_frame.setObjectName(u"footer_left_frame")
        font15 = QFont()
        font15.setPointSize(18)
        font15.setUnderline(True)
        self.footer_left_frame.setFont(font15)
        self.footer_left_frame.setFrameShape(QFrame.StyledPanel)
        self.footer_left_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.footer_left_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.footer_left_frame)
        self.label.setObjectName(u"label")
        font16 = QFont()
        font16.setFamily(u"Bahnschrift")
        font16.setPointSize(11)
        font16.setUnderline(False)
        self.label.setFont(font16)

        self.horizontalLayout_5.addWidget(self.label)


        self.horizontalLayout_7.addWidget(self.footer_left_frame)

        self.footer_right_frame = QFrame(self.Footer_frame)
        self.footer_right_frame.setObjectName(u"footer_right_frame")
        self.footer_right_frame.setFrameShape(QFrame.StyledPanel)
        self.footer_right_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.footer_right_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_2 = QPushButton(self.footer_right_frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        font17 = QFont()
        font17.setFamily(u"Arial Rounded MT Bold")
        font17.setPointSize(12)
        self.pushButton_2.setFont(font17)

        self.horizontalLayout_6.addWidget(self.pushButton_2, 0, Qt.AlignRight)

        self.size_grip = QFrame(self.footer_right_frame)
        self.size_grip.setObjectName(u"size_grip")
        self.size_grip.setMaximumSize(QSize(30, 30))
        self.size_grip.setFrameShape(QFrame.StyledPanel)
        self.size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.size_grip)


        self.horizontalLayout_7.addWidget(self.footer_right_frame)


        self.verticalLayout.addWidget(self.Footer_frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(9)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menu.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Heat Sink", None))
        self.Minimize_window_button.setText("")
        self.Restore_window_button.setText("")
        self.Close_window_button.setText("")
        self.all_btn.setText("")
        self.CPU_btn.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.RAM_btn.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"RAM", None))
        self.Disk_btn.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Disk Usage", None))
        self.Wifi_btn.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Network", None))
        self.GPU_btn.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"GPU", None))
        self.System_info.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"System info", None))
        self.act_btn.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Activity", None))
        self.sensor_btn.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Sensor", None))
        self.battery_btn.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Battery", None))
        self.label_71.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.cpu_per.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"CPU Main Core", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"CPU count", None))
        self.cpu_count.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"CPU Percent", None))
        self.cpu_main_core.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_70.setText(QCoreApplication.translate("MainWindow", u"RAM", None))
        self.free_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.total_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"RAM Usage", None))
        self.ram_usage.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Total Ram", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Free RAM", None))
        self.used_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Available RAM", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Used RAM", None))
        self.available_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"DISC PARTITION", None))
        ___qtablewidgetitem = self.store_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Device", None));
        ___qtablewidgetitem1 = self.store_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Mount Point", None));
        ___qtablewidgetitem2 = self.store_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"OPTS", None));
        ___qtablewidgetitem3 = self.store_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Max File", None));
        ___qtablewidgetitem4 = self.store_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Max Path", None));
        ___qtablewidgetitem5 = self.store_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Total Storage", None));
        ___qtablewidgetitem6 = self.store_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Free Storage", None));
        ___qtablewidgetitem7 = self.store_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Used Storage", None));
        ___qtablewidgetitem8 = self.store_table.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Percent", None));
        self.label_55.setText(QCoreApplication.translate("MainWindow", u" Total Speed", None))
        self.upspeed.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"Download Speed", None))
        self.totalspeed.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"NETWORK", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Upload Speed", None))
        self.downloadspeed.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Ping", None))
        self.ping.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.refresh_btn.setText(QCoreApplication.translate("MainWindow", u"refresh", None))
        self.label_69.setText(QCoreApplication.translate("MainWindow", u"GPU", None))
        self.totalmemory.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.freememory.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_62.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.label_60.setText(QCoreApplication.translate("MainWindow", u"Used Memory ", None))
        self.temperature.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_59.setText(QCoreApplication.translate("MainWindow", u"Total Memory", None))
        self.usedmemory.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_67.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.label_61.setText(QCoreApplication.translate("MainWindow", u"Free Memory", None))
        self.loadd.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_platform.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_system.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"System Time", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Platform", None))
        self.system_processor.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.system_version.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"System Date", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Processor", None))
        self.system_date.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_time.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"System Information", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Machine", None))
        self.system_machine.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.activity_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Procssses", None))
        self.search.setText("")
        ___qtablewidgetitem9 = self.act_table.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Process ID", None));
        ___qtablewidgetitem10 = self.act_table.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Process Name", None));
        ___qtablewidgetitem11 = self.act_table.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Process Status", None));
        ___qtablewidgetitem12 = self.act_table.horizontalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Started", None));
        ___qtablewidgetitem13 = self.act_table.horizontalHeaderItem(4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Suspend", None));
        ___qtablewidgetitem14 = self.act_table.horizontalHeaderItem(5)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Terminate", None));
        ___qtablewidgetitem15 = self.act_table.horizontalHeaderItem(6)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Resume", None));
        ___qtablewidgetitem16 = self.act_table.horizontalHeaderItem(7)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Kill", None));
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Suspend", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Terminate", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Kill", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"SENSOR", None))
        ___qtablewidgetitem17 = self.sensor_table.horizontalHeaderItem(0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Sensor", None));
        ___qtablewidgetitem18 = self.sensor_table.horizontalHeaderItem(1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Label", None));
        ___qtablewidgetitem19 = self.sensor_table.horizontalHeaderItem(2)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Current", None));
        ___qtablewidgetitem20 = self.sensor_table.horizontalHeaderItem(3)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"High", None));
        ___qtablewidgetitem21 = self.sensor_table.horizontalHeaderItem(4)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Critical", None));
        self.battery_time_left.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.battery_status.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.battery_charge.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Plugged in", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Charge", None))
        self.battery_plugged.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Time Left", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Battery Information", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"RAM", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"BATTERY", None))
        self.label_58.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_63.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_64.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"NETWORK", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"GPU", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Version 1.0 | Copyright HeatSink by Team ZOX", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"?", None))
    # retranslateUi

