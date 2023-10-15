import sys, os
import wx

from PyQt5.QtMultimedia import QSound
from playsound import playsound
import root.form.SecondForm as sec
from root.util.FaderStackWidget import *
from pathlib import Path


# App 관련 Class 생성
class AppForm(QtWidgets.QWidget):
    # 기본 스크린 사이즈
    root_path = Path(os.path.abspath('')).parent

    # m_process = multiprocessing.Process(target=playsound, args=['musics/space.mp3'])

    def playBackgroundSound(self):
        # playsound(str(self.root_path)+'/musics/space.mp3',False)
        pass


    def stopBackgroundSound(self):
        pass
        #empty


    # 클래스 중 가장 먼저 실행되는 함수
    def __init__(self):
        super().__init__()
        self.init_ui()

    # UI 초기화 함수 (기본 UI 설정)

    def init_ui(self):
        #set title

        self.setWindowTitle("Ai Application Demo")

        # if os.name == 'nt':
        #     self.setWindowIcon(QIcon('app_icon.png'))

        # set Defalut Screen Size
        #set Defalut Screen Size - 1. get Screen Size on each platform from wxPython
        # wxApp = wx.App(False)
        # sc_width, sc_height = wx.GetDisplaySize()
        # set Defalut Screen Size - 2. resize app screen size of your desktop screen size (About 1/4 size)


        # Quit action

        quit = QtWidgets.QAction("Quit", self)

        quit.triggered.connect(self.close)

        # set main btn
        self.vision_btn = QtWidgets.QPushButton('비전', self)
        self.qt_practice_btn = QtWidgets.QPushButton('QT 예제', self)

        # set btn font
        self.vision_btn.setFont(QFont('Arial',20))
        self.qt_practice_btn.setFont(QFont('Arial',20))

        self.vision_btn.setMaximumHeight(80)
        self.qt_practice_btn.setMaximumHeight(80)

        # set widget connect with signal
        self.vision_btn.clicked.connect(self.vision_btn_function)
        self.qt_practice_btn.clicked.connect(self.qt_practice_btn_function)

        self.vision_btn.installEventFilter(self)
        self.qt_practice_btn.installEventFilter(self)

        self.vision_btn.setStyleSheet('QPushButton::hover'
                                      '{'
                                      'background-color : #64b5f6'
                                      '}'
                                      )

        self.qt_practice_btn.setStyleSheet('QPushButton::hover'
                                      '{'
                                      'background-color : #64b5f6'
                                      '}'
                                      )

        #set text


        title_text = QtWidgets.QLabel('Vision Project with PyQt5')
        title_text.setStyleSheet('color : white')
        title_text.setFont(QFont('Arial',35))
        title_text.setAlignment(Qt.AlignCenter)

        copyright_text = QtWidgets.QLabel('Copylight : easyJin')
        copyright_text.setStyleSheet('color : white')
        copyright_text.setAlignment(Qt.AlignCenter)

        # set grid layout
        grid = QtWidgets.QGridLayout()


        self.setLayout(grid)
        grid.cellRect(5,3)

        grid.setRowStretch(0,1)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,1)
        grid.setRowStretch(3,1)
        grid.setRowStretch(4,1)

        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,1)
        grid.setColumnStretch(2,1)




        grid.addWidget(title_text,0,0,1,3)
        grid.addWidget(self.vision_btn,2,1,1,1)
        grid.addWidget(self.qt_practice_btn,3,1,1,1)
        grid.addWidget(copyright_text,4,0,1,3)

    def vision_btn_function(self):
        stack.setCurrentIndex(stack.currentIndex()+1)


    def qt_practice_btn_function(self):
        print('qt_practice_btn_function page')
        reply = QtWidgets.QMessageBox.question(self, 'Message', '준비중입니다 : (',
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

    # set background img

    def paintEvent(self, a0: QPaintEvent):
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pix = QPixmap(str(self.root_path)+"/imgs/ui/background-img.png")  # Change to the relative path of your own image
        painter.drawPixmap(self.rect(), pix)


    # app close event
    # def closeEvent(self, a0: QCloseEvent):
    #     self.stopBackgroundSound()

    def eventFilter(self, obj, event):

        if obj == self.qt_practice_btn and event.type() == QEvent.HoverEnter:
            self.onHovered()
        elif obj == self.vision_btn and event.type() == QEvent.HoverEnter:
            self.onHovered()

        return super(AppForm, self).eventFilter(obj, event)

    def onHovered(self):
        QSound.play(str(self.root_path)+'/musics/button_hover.wav')
#        playsound('musics/button_hover.wav')




# python main code(실행 메인 스크립트)
if __name__ == '__main__':

    sc_width = 1920
    sc_height = 1080
    sc_width = int(sc_width / 2)
    sc_height = int(sc_height / 2)

    # QApplication 함수 호출을 통해 app 생성 (모든 QT Application은 어플리케이션 객체를 생성해야한다. doc 참조.
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(AppForm.root_path)+'/imgs/app_icon.png'))

    # AppForm 인스턴스 생성 및 창 실행
    stack = StackedWidget()
    stack.resize(sc_width,sc_height)

    main_app_form = AppForm()
    second_form = sec.Second_Form()
    second_form.init_StackWidget(stack)

    stack.addWidget(main_app_form)
    stack.addWidget(second_form)
    main_app_form.playBackgroundSound()
    stack.show()

    # App 호출, pyqt4와의 호환성을 위해 sys.exit(app.exec_())로 쓰기도

    sys.exit(app.exec_())
