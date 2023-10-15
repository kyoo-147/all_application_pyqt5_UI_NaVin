from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class StackedWidget(QtWidgets.QStackedWidget):

    def __init__(self, parent=None):
        QtWidgets.QStackedWidget.__init__(self, parent)


    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QtWidgets.QStackedWidget.setCurrentIndex(self, index)


class FaderWidget(QtWidgets.QWidget):

    def __init__(self, old_widget, new_widget):
        QtWidgets.QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(200)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()