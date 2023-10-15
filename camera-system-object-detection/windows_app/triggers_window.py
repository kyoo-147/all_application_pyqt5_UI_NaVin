import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from add_trigger_window import AddTriggerWindow
import layout
import triggers
import css

class TriggersWindow(QWidget):
    resetTriggerUI = pyqtSignal(triggers.Trigger)

    def __init__(self, mainWindow):
        super().__init__()
        self.resetTriggerUI.connect(resetTriggerStyle)
        self.mainWindow = mainWindow
        
        self.setGeometry(300, 200, 700, 440)
        self.setWindowTitle('Triggers')
        self.setWindowIcon(QIcon('./Assets/TriggersIcon.png'))

        layout.triggersWindowLayout(self)

        triggers.Trigger.triggersWindow = self
        
        for trigger in triggers.triggersList:
            layout.addTriggerOnViewList(self, trigger)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()
    
    def openDrawAreaWindow(self):
        self.drawAreaWindow = AddTriggerWindow(self)

def resetTriggerStyle(trigger):
    if trigger.widget is not None:
        trigger.widget.setStyleSheet(css.triggerStandard)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TriggersWindow()
    sys.exit(app.exec_())