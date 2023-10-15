from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from pathlib import Path
import os

class DummyForm(QtWidgets.QWidget):

    root_path = Path(os.path.abspath('')).parent
    app_font = QFont('Arial',24)
    stack = None

    def __init__(self):
        super().__init__()
        self.setup_ui()


    def setup_ui(self):
        self.setWindowTitle('Dummy Review Sentiment')
        self.resize(800,600)

        self.title_label = QtWidgets.QLabel()
        self.title_label.setText('Dummy Review Sentiment')
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(self.app_font)
        self.title_label.setStyleSheet('color : white')

        self.back_btn = QtWidgets.QPushButton()
        self.back_btn.setText('Back to Home')
        self.back_btn.setMaximumHeight(50)
        self.back_btn.clicked.connect(self.back_btn_function)

        self.grid_layout = QtWidgets.QGridLayout()
        # 그리드 레이아웃 크기 지정
        # self.grid_layout.cellRect(5,3)
        # 그리드 레이아웃 각 행열의 사이즈 계수 1로 고정 ,, 0이 아니라 1부터 시작 주의
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)

        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setRowStretch(4, 1)

        self.setLayout(self.grid_layout)

        # 3,4 파라미터는 행은 1개먹고, 열은 2개먹고
        self.grid_layout.addWidget(self.title_label, 0, 0, 1, 3)

        self.grid_layout.addWidget(self.back_btn, 4, 1, 1, 1)

    def paintEvent(self, a0: QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.7)
        painter.drawRect(self.rect())


        pix = QtGui.QPixmap()  # Change to the relative path of your own image
        img_path = str(self.root_path) + '/imgs/ui/background-img.png'
        pix.load(img_path)

        painter.drawPixmap(self.rect(), pix)

    def init_StackWidget(self, para):
        self.stack = para

    def back_btn_function(self):
        self.stack.removeWidget(self)
        # setCurrentIndex 안해도 removeWidget 하면 넘어감.. self.stack.setCurrentIndex(self.stack.currentIndex())