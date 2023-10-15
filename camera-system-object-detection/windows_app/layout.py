from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QSlider
from PyQt5.QtWidgets import QWidget, QComboBox, QTimeEdit, QLineEdit, QScrollArea, QCheckBox, QLayout
from PyQt5.QtGui import QCursor, QIcon, QIntValidator
from PyQt5.QtCore import Qt
from image_widget import ImageWidget
import css
import typing
if typing.TYPE_CHECKING:
    from main import GUI
    from triggers import Trigger
    from add_trigger_window import AddTriggerWindow
    from triggers_window import TriggersWindow

def initMainWindowLayout(UI: "GUI", Triggers: "Trigger"):
    UI.setGeometry(50, 50, 1250, 660)
    UI.setObjectName('window')
    UI.setStyleSheet(css.windowStyle)

    # Button triggers
    btnTriggers = QPushButton("Triggers")
    btnTriggers.setStyleSheet(css.btnStyle)
    btnTriggers.setMaximumWidth(200)
    btnTriggers.clicked.connect(UI.openTriggersWindow)

    # CheckBox show triggers
    UI.checkboxViewTriggers = QCheckBox('Show Triggers')
    UI.checkboxViewTriggers.setStyleSheet(css.checkBoxStyle)
    
    # CheckBox adjust blob size
    checkboxBlobSize = QCheckBox('Adjust Blob Size')
    checkboxBlobSize.setStyleSheet(css.checkBoxStyle)
    checkboxBlobSize.clicked.connect(UI.onCheckboxAjustarBlobSizeClick)
    # UI.checkboxViewTriggers.setChecked(True)

    # CheckBox silence alarm
    Triggers.checkboxSilenceAlarms = QCheckBox('Silence Alarms')
    Triggers.checkboxSilenceAlarms.setStyleSheet(css.checkBoxStyle)
    Triggers.checkboxSilenceAlarms.setChecked(True)

    # Image
    UI.camImgs.append(ImageWidget(UI.handleImageClick))
    UI.camImgs[0].setStyleSheet(css.imageStyle)
    # UI.camImgs[0].setScaledContents(True)
    # UI.camImgs[0].setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    # UI.camImgs[0].setMinimumSize(800, 600)
    UI.camImgs.append(ImageWidget(UI.handleImageClick))
    UI.camImgs[1].setStyleSheet(css.imageStyle)
    # UI.camImgs[1].setMaximumWidth(100)

    # Labels
    lClientConnected = QLabel('Client: ')
    UI.lClientConnectedValue = QLabel('Disconnected')
    UI.lClientConnectedValue.setStyleSheet(css.textRed)
    lImg1BlobSize = QLabel('Blob Size Image 1:')
    lImg2BlobSize = QLabel('Blob Size Image 2:')
    lSettings = QLabel('Settings')

    # Slider
    UI.lPersonSize = QLabel(str(UI.imgManager.personTesterSize))
    UI.lPersonSize.hide()
    UI.personTesterSizeSlider = QSlider(Qt.Horizontal)
    UI.personTesterSizeSlider.setRange(2, 460)
    UI.personTesterSizeSlider.setValue(UI.imgManager.personTesterSize)
    UI.personTesterSizeSlider.valueChanged.connect(UI.sliderPersonTesterSize)
    UI.personTesterSizeSlider.setPageStep(50)
    UI.personTesterSizeSlider.setTickInterval(10)
    UI.personTesterSizeSlider.hide()

    # LineEdit
    UI.inputBlobSize = []
    for i in range(2):
        UI.inputBlobSize.append(QLineEdit())
        UI.inputBlobSize[i].setMaximumSize(45, 28)
        UI.inputBlobSize[i].setStyleSheet(css.blobSizeTextEdit)
        UI.inputBlobSize[i].setText(str(UI.detector.blobSizes[i]))
        UI.inputBlobSize[i].setValidator(
            QIntValidator(UI.detector.blobSizeRange[0], UI.detector.blobSizeRange[1]))
    UI.inputBlobSize[0].textChanged.connect(lambda value: UI.detector.setBlobSize(value, 0))
    UI.inputBlobSize[1].textChanged.connect(lambda value: UI.detector.setBlobSize(value, 1))

    # Layout organization
    vBoxMain = QVBoxLayout()
    vBoxMain.setSizeConstraint(QLayout.SetMinimumSize)
    hBoxTop = QHBoxLayout()
    hBoxTop.setAlignment(Qt.AlignTop)
    hBoxBottom = QHBoxLayout()
    vBoxImages = QVBoxLayout()
    vBoxImages.setAlignment(Qt.AlignCenter)
    vBoxSettings = QVBoxLayout()
    vBoxSettings.setSpacing(10)
    vBoxSettings.setAlignment(Qt.AlignTop)
    vBoxImages.addWidget(UI.camImgs[0])
    vBoxImages.addWidget(UI.camImgs[1])
    hBoxImg1BlobSize = QHBoxLayout()
    hBoxImg2BlobSize = QHBoxLayout()
    hBoxBlobSizeAjuste = QHBoxLayout()
    hBoxClientInfo = QHBoxLayout()
    hBoxTop.addWidget(btnTriggers)
    hBoxImg1BlobSize.addWidget(lImg1BlobSize)
    hBoxImg1BlobSize.addWidget(UI.inputBlobSize[0], alignment=Qt.AlignLeft)
    hBoxImg2BlobSize.addWidget(lImg2BlobSize)
    hBoxImg2BlobSize.addWidget(UI.inputBlobSize[1], alignment=Qt.AlignLeft)
    vBoxSettings.addWidget(lSettings, alignment=Qt.AlignTop | Qt.AlignCenter)
    vBoxSettings.addWidget(UI.checkboxViewTriggers)
    vBoxSettings.addWidget(checkboxBlobSize)
    vBoxSettings.addWidget(Triggers.checkboxSilenceAlarms)
    hBoxBlobSizeAjuste.addWidget(UI.personTesterSizeSlider)
    hBoxBlobSizeAjuste.addWidget(UI.lPersonSize)
    vBoxSettings.addLayout(hBoxBlobSizeAjuste)
    vBoxSettings.addLayout(hBoxImg1BlobSize)
    vBoxSettings.addLayout(hBoxImg2BlobSize)
    hBoxClientInfo.addWidget(lClientConnected)
    hBoxClientInfo.addWidget(UI.lClientConnectedValue)
    hBoxClientInfo.setAlignment(Qt.AlignRight)
    hBoxTop.addLayout(hBoxClientInfo)
    vBoxMain.addLayout(hBoxTop)
    vBoxMain.addLayout(hBoxBottom)
    vBoxMain.setStretchFactor(hBoxTop, 1)
    vBoxMain.setStretchFactor(hBoxBottom, 100)
    hBoxBottom.addLayout(vBoxImages)
    hBoxBottom.setStretchFactor(vBoxImages, 5)
    hBoxBottom.addLayout(vBoxSettings)
    hBoxBottom.setStretchFactor(vBoxSettings, 1)

    UI.setLayout(vBoxMain)
    UI.show()

def triggersWindowLayout(UI: "TriggersWindow"):
    UI.setObjectName('window')
    UI.setStyleSheet(css.windowStyle)

    # Buttons
    btnAdd = QPushButton("Add Trigger")
    btnAdd.clicked.connect(UI.openDrawAreaWindow)
    btnAdd.setMinimumWidth(150)
    btnAdd.setStyleSheet(css.btnStyle)
    btnBack = QPushButton("Back")
    btnBack.clicked.connect(UI.close)
    btnBack.setStyleSheet(css.btnStyle)

    # Labels
    lTriggersList = QLabel("Triggers List")
    scrollArea = QScrollArea()
    triggersList = QWidget()

    # Layout organization
    vBoxMain = QVBoxLayout()
    UI.vBoxTriggers = QVBoxLayout()

    scrollArea.setStyleSheet(css.scrollAreaStyle)
    scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scrollArea.setWidgetResizable(True)

    vBoxMain.addWidget(btnAdd, alignment=Qt.AlignLeft)
    vBoxMain.addWidget(lTriggersList, alignment=Qt.AlignHCenter)
    vBoxMain.addWidget(scrollArea)
    vBoxMain.addWidget(btnBack, alignment=Qt.AlignRight)

    triggersList.setLayout(UI.vBoxTriggers)
    scrollArea.setWidget(triggersList)
    UI.setLayout(vBoxMain)
    UI.show()

def addTriggerWindowLayout(UI: "AddTriggerWindow"):
    UI.setObjectName('window')
    UI.setStyleSheet(css.windowStyle)
    UI.setGeometry(100, 100, 1150, 440)
    UI.setWindowTitle('Add Trigger')

    # Buttons
    btnConfirm = QPushButton("Confirm")
    btnConfirm.setMaximumWidth(150)
    btnConfirm.clicked.connect(UI.saveTriggerAndQuit)
    btnConfirm.setStyleSheet(css.btnStyle)

    # Labels
    UI.camImg = QLabel()
    lDrawArea = QLabel("Draw detection area")
    lDrawArea.setMaximumHeight(20)
    lTriggerName = QLabel("Name")
    lTriggerName.setMaximumHeight(20)
    lDetectionTime = QLabel("Active Time")
    lDetectionTime.setMaximumHeight(20)
    lMaxStayTime = QLabel("Maximum Stay Time")
    lMaxStayTime.setMaximumHeight(20)
    lSeconds = QLabel("sec")
    lSeconds.setMaximumHeight(20)
    lSeconds.setMinimumWidth(20)
    lAction = QLabel("Action")
    lAction.setMaximumHeight(20)
    lUntil = QLabel("to")
    lUntil.setMaximumHeight(20)
    lUntil.setMaximumWidth(40)

    # Input widgets
    UI.inputTriggerName = QLineEdit()
    UI.inputTriggerName.setStyleSheet(css.textBlack)
    UI.inputAction = QComboBox()
    UI.inputAction.addItem('Alarm')
    UI.inputAction.addItem('Notification')
    UI.inputAction.setStyleSheet(css.textBlack)
    UI.inputTimeFrom = QTimeEdit()
    UI.inputTimeFrom.setStyleSheet(css.textBlack)
    UI.inputTimeTo = QTimeEdit()
    UI.inputTimeTo.setStyleSheet(css.textBlack)
    UI.inputMaxStayTime = QLineEdit()
    UI.inputMaxStayTime.setStyleSheet(css.textBlack)

    # Layout organization
    vBoxMain = QVBoxLayout()
    hBoxMain = QHBoxLayout()
    vBoxRight = QVBoxLayout()
    hBoxTime = QHBoxLayout()
    hBoxMaxStayTime = QHBoxLayout()
    vBoxMain.addWidget(lDrawArea)
    vBoxMain.addLayout(hBoxMain)
    hBoxMain.addWidget(UI.camImg, alignment=Qt.AlignLeft)
    hBoxMain.addLayout(vBoxRight)
    vBoxRight.addWidget(lTriggerName)
    vBoxRight.addWidget(UI.inputTriggerName)
    vBoxRight.addWidget(lDetectionTime)
    vBoxRight.addLayout(hBoxTime)
    hBoxTime.addWidget(UI.inputTimeFrom)
    hBoxTime.addWidget(lUntil)
    hBoxTime.addWidget(UI.inputTimeTo)
    vBoxRight.addWidget(lMaxStayTime)
    vBoxRight.addLayout(hBoxMaxStayTime)
    hBoxMaxStayTime.addWidget(UI.inputMaxStayTime)
    hBoxMaxStayTime.addWidget(lSeconds)
    vBoxRight.addWidget(lAction)
    vBoxRight.addWidget(UI.inputAction)
    vBoxRight.addWidget(btnConfirm, alignment=Qt.AlignBottom | Qt.AlignCenter)

    UI.setLayout(vBoxMain)
    UI.show()

def addTriggerOnViewList(UI: "TriggersWindow", trigger: "Trigger"):
    trigger.widget = triggerBackground = QWidget()
    triggerBackground.setObjectName('triggerBackground')
    
    # Button delete
    btnDelete = QPushButton()
    btnDelete.setIcon(QIcon('./Assets/delete_white.png'))
    btnDelete.clicked.connect(trigger.remove)
    btnDelete.setCursor(QCursor(Qt.PointingHandCursor))
    btnDelete.setStyleSheet(css.btnTriggerStyle)
    
    # Button reset
    btnReset = QPushButton('Reset')
    btnReset.clicked.connect(trigger.reset)
    btnReset.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    btnReset.setStyleSheet(css.btnTriggerStyle)

    # Trigger style
    if trigger.fired:
        triggerBackground.setStyleSheet(css.triggerFired)
    else:
        triggerBackground.setStyleSheet(css.triggerStandard)

    # Labels
    lTriggerName = QLabel(trigger.name if trigger.name != '' else 'Trigger ' + str(trigger.id))
    lTriggerName.setStyleSheet(css.title)
    lAction = QLabel("Action: " + trigger.action)
    lMaxStayTime = QLabel("Maximum Stay Time: " + str(trigger.maxStayTime))
    lActiveTime = QLabel("Active Time:")
    lActiveTimeValues = QLabel(trigger.initialTime + ' to ' + trigger.finalTime)
    lStayedTime = QLabel('Stayed Time:')
    trigger.lStayedTime = QLabel(str(round(trigger.stayedTime, 3)))

    # Layout organization
    vBoxMain = QVBoxLayout(triggerBackground) # QVBoxLayout with QWidget as parent to style the layout
    hBoxInfo = QHBoxLayout()
    hBoxTop = QHBoxLayout()
    vBoxLeft = QVBoxLayout()
    vBoxStayTime = QVBoxLayout()
    hBoxStayedTime = QHBoxLayout()
    hBoxDetectionTime = QHBoxLayout()
    vBoxBtnReset = QVBoxLayout()
    UI.vBoxTriggers.addWidget(triggerBackground)
    hBoxTop.addWidget(lTriggerName, alignment=Qt.AlignTop)
    hBoxTop.addWidget(btnDelete, alignment=Qt.AlignRight)
    hBoxInfo.setAlignment(Qt.AlignTop)
    vBoxLeft.addWidget(lAction, alignment=Qt.AlignTop)
    vBoxStayTime.addWidget(lMaxStayTime, alignment=Qt.AlignRight)
    vBoxStayTime.addLayout(hBoxStayedTime)
    vBoxStayTime.setAlignment(Qt.AlignRight)
    hBoxStayedTime.addWidget(lStayedTime)
    hBoxStayedTime.addWidget(trigger.lStayedTime)
    hBoxDetectionTime.addWidget(lActiveTime)
    hBoxDetectionTime.addWidget(lActiveTimeValues)
    vBoxBtnReset.addWidget(btnReset, alignment=Qt.AlignBottom)
    vBoxLeft.addLayout(hBoxDetectionTime)
    vBoxMain.addLayout(hBoxTop)
    vBoxMain.addLayout(hBoxInfo)
    hBoxInfo.addLayout(vBoxLeft)
    hBoxInfo.addLayout(vBoxStayTime)
    hBoxInfo.addLayout(vBoxBtnReset)