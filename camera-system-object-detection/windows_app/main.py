import sys, os, cv2, time
from playsound import playsound
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QImage, QIcon, QCursor
from PyQt5.QtCore import Qt, pyqtSignal
from image_manager import ImageManager
from triggers_window import TriggersWindow
from area_painter import AreaPainter
from server import ServerConnection
from image_widget import ImageWidget
from detector import SSDDetector
from helpers.blob_size_tester import BlobSizeTester as dt
import layout, triggers, css

class GUI(QWidget):
    setImagePixmapSignal = pyqtSignal(ImageWidget, QPixmap)
    updateClientStatusSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.camImgs: list[ImageWidget] = []
        self.bVisualizarAreas = True
        self.triggersThread = triggers.initTriggers(self.updateTriggerState)
        self.detector = SSDDetector(triggers.updateTriggersAfterDetection)
        self.detector.start()
        self.imgManager = ImageManager(maxBufferSize=10)
        self.imgManager.onVideoEnd.append(self.detector.benchmark.printStatistics)
        self.imgManager.onUpdateFrame.append(self.detector.setFrame)
        self.initMainWindow()
        self.areaPainter = AreaPainter()
        self.updateClientStatusSignal.connect(self.updateClientStatus)
        self.server = ServerConnection(lambda status: self.updateClientStatusSignal.emit(status))
        self.server.start()
        self.focusedImage = None
        self.deactivateCheckBoxTimer = time.time()
        self.camImg1Pixmap = None

        self.initImgWidget()
        self.setImagePixmapSignal.connect(self.setImagePixmap)
        ImageManager.onUpdateFrame.append(self.updateFrame)

    def initMainWindow(self):
        self.setWindowTitle('Camera Surveillance System')
        self.setWindowIcon(QIcon('./assets/icon.png'))

        layout.initMainWindowLayout(self, triggers.Trigger)

    def initImgWidget(self):
        h, w = self.imgManager.frameResolution

        initialHeight = 280
        aspectRatio = float(w) / float(h)
        initialWidth = int(initialHeight * aspectRatio)
        self.initialCamImgShape = (initialWidth, initialHeight)
        self.focusedCamImgShape = (initialWidth * 2, initialHeight * 2)
        self.camImgShape = self.initialCamImgShape

        frame = cv2.imread("./assets/no_signal.jpg")

        self.focusOnImage(self.camImgs[0])
        
        width, height = self.initialCamImgShape
        bytesPerLine = 3 * width
        frameResized = cv2.resize(frame, self.initialCamImgShape)

        camImgQImage = QImage(frameResized.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        camImgPixmap = QPixmap(camImgQImage)
        self.camImgs[0].setPixmap(camImgPixmap)
        self.camImgs[1].setPixmap(camImgPixmap)

        self.camImgs[0].setMaximumSize(self.camImgShape[0], self.camImgShape[1])
        self.camImgs[1].setMaximumSize(self.camImgShape[0], self.camImgShape[1])

    def onCheckboxAjustarBlobSizeClick(self, value):
        self.imgManager.setShowPersonTester(value)
        self.detector.setOnlyDetectCroppedFrame(not value)
        self.personTesterSizeSlider.setVisible(value)
        self.lPersonSize.setVisible(value)

    def sliderPersonTesterSize(self, value):
        self.lPersonSize.setText(str(value))
        self.imgManager.setPersonTesterSize(value)

    def handleImageClick(self, imgToFocus):
        if self.focusedImage is None:
            self.focusOnImage(imgToFocus)
        else:
            self.unfocusImages()

    def focusOnImage(self, imgToFocus):
        self.camImgs[0].setMaximumSize(self.focusedCamImgShape[0], self.focusedCamImgShape[1])
        self.camImgs[1].setMaximumSize(self.focusedCamImgShape[0], self.focusedCamImgShape[1])
        self.camImgShape = self.focusedCamImgShape
        
        self.focusedImage = imgToFocus
        for img in self.camImgs:
            if img != self.focusedImage:
                img.hide()
    
    def unfocusImages(self):
        self.camImgs[0].setMaximumSize(self.initialCamImgShape[0], self.initialCamImgShape[1])
        self.camImgs[1].setMaximumSize(self.initialCamImgShape[0], self.initialCamImgShape[1])
        self.camImgShape = self.initialCamImgShape

        for img in self.camImgs:
            if img != self.focusedImage:
                img.show()
        self.focusedImage = None

    def updateFrame(self, frame):
        frameWithDetections = self.detector.drawDetections(frame)
        frame1 = cv2.resize(frameWithDetections, self.camImgShape)
           
        if self.checkboxViewTriggers.isChecked():
            frame1 = self.areaPainter.paintAreasMainImg(frame1)

        height, width, _ = frame1.shape
        bytesPerLine = 3 * width
        camImgQImage = QImage(frame1, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        camImg1Pixmap = QPixmap(camImgQImage)

        self.setImagePixmapSignal.emit(self.camImgs[0], camImg1Pixmap)

        if self.detector.resizeStartPoint is None:
            return

        croppedFrame = frameWithDetections[
            self.detector.resizeStartPoint[0]:self.detector.resizeEndPoint[0],
            self.detector.resizeStartPoint[1]:self.detector.resizeEndPoint[1]
        ]

        frame2 = cv2.resize(croppedFrame, self.camImgShape)
        height, width, _ = frame2.shape
        bytesPerLine = 3 * width
        camImgQImage = QImage(frame2, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        camImg2Pixmap = QPixmap(camImgQImage)
        
        self.setImagePixmapSignal.emit(self.camImgs[1], camImg2Pixmap)

    def setImagePixmap(self, img, pixmap):
        img.setPixmap(pixmap)

    def updateTriggerState(self, trigger: triggers.Trigger, state):
        if trigger.widget is not None:
            trigger.widget.setStyleSheet(css.triggerFired if state else css.triggerStandard)

        self.server.fireTrigger(trigger)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_2:
            self.server.sendNotification(triggers.triggersList[0])
        elif e.key() == Qt.Key_3:
            self.server.sendAlarm(triggers.triggersList[0])
        elif e.key() == Qt.Key_4:
            self.imgManager.togglePauseVideo()
        elif e.key() == Qt.Key_5:
            playsound('./sounds/mixkit-classic-short-alarm.wav')
        elif e.key() == Qt.Key_T:
            coordsGlobal = QCursor.pos()
            coordsLocal = self.camImgs[0].mapFromGlobal(coordsGlobal)
            coordsNormalized = (coordsLocal.x() / self.camImgs[0].frameGeometry().width(),
                                coordsLocal.y() / self.camImgs[0].frameGeometry().height())
            dt.addTesterToList(coordsNormalized)
        elif e.key() == Qt.Key_Q:
            self.close()

    def updateClientStatus(self, status):
        if status:
            self.lClientConnectedValue.setText('Connected')
            self.lClientConnectedValue.setStyleSheet(css.textGreen)
        else:
            self.lClientConnectedValue.setText('Disconnected')
            self.lClientConnectedValue.setStyleSheet(css.textRed)

    def openTriggersWindow(self):
        self.triggersWindow = TriggersWindow(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())