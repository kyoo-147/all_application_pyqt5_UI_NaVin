import sys
#from detect import Detect
from gui import Gui
import cv2
from PyQt5.QtWidgets import QApplication

def main():
    """
    Main function
    """
    app = QApplication(sys.argv)
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()