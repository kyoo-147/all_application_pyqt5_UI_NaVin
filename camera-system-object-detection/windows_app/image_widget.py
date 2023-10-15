from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QMouseEvent, QResizeEvent
from PyQt5.QtCore import pyqtSignal

class ImageWidget(QLabel):
    def __init__(self, onClicked):
        super().__init__()

        self.onClicked = onClicked

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.onClicked(self)
        return super().mousePressEvent(e)
    
    # def resizeEvent(self, e: QResizeEvent) -> None:
    #     pixmap = self.pixmap()
    #     if pixmap is not None:
    #         self.setPixmap(pixmap.scaled(e.size().width(), e.size().height(), Qt.KeepAspectRatio))
    #     return super().resizeEvent(e)