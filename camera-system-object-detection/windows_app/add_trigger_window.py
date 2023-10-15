import os
import cv2 as cv
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import triggers
import layout
import css
from image_manager import ImageManager
from area_painter import AreaPainter

class AddTriggerWindow(QWidget):
    setImageSignal = pyqtSignal(QPixmap)

    def __init__(self, triggersWindow):
        super().__init__()
        self.triggersWindow = triggersWindow
        self.setImageSignal.connect(lambda pixmap: self.camImg.setPixmap(pixmap))
        
        self.setWindowIcon(QIcon('./Assets/TriggersIcon.png'))
        self.bDrawing = False

        layout.addTriggerWindowLayout(self)

        h, w = ImageManager.frameResolution
        initialHeight = 500
        aspectRatio = float(w) / float(h)
        initialWidth = int(initialHeight * aspectRatio)
        self.camImgShape = (initialWidth, initialHeight)

        self.camImg.setMaximumSize(self.camImgShape[0], self.camImgShape[1])

        self.areaPainter = AreaPainter()

        ImageManager.onUpdateFrame.append(self.updateFrame)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()
        if e.key() == Qt.Key_Z:
            self.areaPainter.deleteLastArea()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.areaPainter.startArea(self.camImg)
            self.bDrawing = True

    def mouseMoveEvent(self, e):
        if self.bDrawing:
            self.areaPainter.updateArea()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.bDrawing = False
            self.areaPainter.saveArea()

    def closeEvent(self, e):
        ImageManager.onUpdateFrame.remove(self.updateFrame)

    def updateFrame(self, frame):
        frameResized = cv.resize(frame, self.camImgShape)
        self.areaPainter.paintAreasAddTrigger(frameResized)

        height, width, _ = frameResized.shape
        bytesPerLine = 3 * width
        qImg = QImage(frameResized, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        image = QPixmap(qImg)

        self.setImageSignal.emit(image)

    def saveTriggerAndQuit(self):
        try:
            float(self.inputMaxStayTime.text())
        except:
            print('Invalid stay time:', self.inputMaxStayTime.text())
            return

        if self.inputMaxStayTime.text() == '':
            print('Stay time is obligatory')
            return

        if len(self.areaPainter.areas) == 0:
            print("No areas were drawn")
            return

        if (self.areaPainter.areas[0][0][0] - self.areaPainter.areas[0][1][0] >= 0
            or self.areaPainter.areas[0][0][1] - self.areaPainter.areas[0][1][1] >= 0):
            print('Invalid area. Draw again.')
            return

        # Normaliza areas
        areaStartX = self.areaPainter.areas[0][0][0] / self.camImgShape[0]
        areaStartY = self.areaPainter.areas[0][0][1] / self.camImgShape[1]
        areaEndX = self.areaPainter.areas[0][1][0] / self.camImgShape[0]
        areaEndY = self.areaPainter.areas[0][1][1] / self.camImgShape[1]

        triggers.createTrigger(
            self.inputTriggerName.text(),
            self.inputTimeFrom.time().toString()[:-3],
            self.inputTimeTo.time().toString()[:-3],
            float(self.inputMaxStayTime.text()),
            self.inputAction.currentText(),
            areaStartX,
            areaStartY,
            areaEndX,
            areaEndY)

        self.triggersWindow.mainWindow.detector.updateDetectionArea()

        self.close()