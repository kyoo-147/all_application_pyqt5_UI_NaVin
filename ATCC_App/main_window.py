# Modified by Rajat Shrivastav
# o6th March 2021
# Traffic Surviellance System GUI using AI city Challenge
# *-
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QDate, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox,QMainWindow,QDialog
import resource
# from model import Model
from output_window import Ui_OutputDialog


class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("./mainwindow.ui", self)
        self.runButton.clicked.connect(self.runSlot)

    @pyqtSlot()
    def runSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        ui.hide()  # hide the main window
        self.outputWindow_()

    def outputWindow_(self):
        """
        Created new window for visual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
