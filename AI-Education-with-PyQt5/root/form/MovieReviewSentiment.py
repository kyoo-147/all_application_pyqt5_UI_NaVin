from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from pathlib import Path
import os


import numpy as np
from tensorflow import keras
from googletrans import Translator
import json
from httpcore import ConnectError

class MovieReviewForm(QtWidgets.QWidget):

    root_path = Path(os.path.abspath('')).parent
    app_font = QFont('Arial',24)
    stack = None
    model = None
    word_index = None


    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.model_setup()



    def changed(self):
        print('changed')


    def setup_ui(self):
        self.setWindowTitle('Movie Review Sentiment')
        self.resize(800,600)

        self.title_label = QtWidgets.QLabel()
        self.title_label.setText('Movie Review Sentiment')
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(self.app_font)
        self.title_label.setStyleSheet('color : black')

        self.back_btn = QtWidgets.QPushButton()
        self.back_btn.setText('Back to Home')
        self.back_btn.setMaximumHeight(50)
        self.back_btn.clicked.connect(self.back_btn_function)

        self.input_text_box = QtWidgets.QLineEdit()
        self.input_text_box.setMaximumHeight(50)

        # self.input_text_box.
        self.input_text_box.setFont(QFont('Arial',15))
        self.input_text_box.setAlignment(QtCore.Qt.AlignCenter)

        self.input_text_box.setPlaceholderText('Please input the movie review')
        self.input_text_box.installEventFilter(self)

        self.result_text = QtWidgets.QLabel()
        self.result_text.setAlignment(QtCore.Qt.AlignCenter)
        self.result_text.setFont(self.app_font)
        self.result_text.setStyleSheet('color : black')


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
        self.grid_layout.addWidget(self.input_text_box, 3, 0, 1, 3)
        self.grid_layout.addWidget(self.result_text, 1, 0, 1, 3)
        self.grid_layout.addWidget(self.back_btn, 4, 1, 1, 1)

        # set focus widget
        # self.input_text_box.focusWidget()

    def paintEvent(self, a0: QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setOpacity(0.5)
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

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.input_text_box :
            if event.key() == QtCore.Qt.Key_Return and self.input_text_box.hasFocus():
                # text entered
                self.text_append(self.input_text_box.text())
                self.input_text_box.clear()

        return super().eventFilter(obj, event)

    def text_append(self, text):
        self.decode_review(text)


    def model_setup(self):

        with open(str(self.root_path) + '/models/imdb_word_index.json') as json_file:
            json_data = json.load(json_file)

        self.word_index = json_data
        self.word_index = {k: (v + 3) for k, v in self.word_index.items()}
        self.word_index["<PAD>"] = 0  # padding
        self.word_index["<START>"] = 1
        self.word_index["<UNK>"] = 2  # unknown
        self.word_index["<UNUSED>"] = 3
        self.model = keras.models.load_model(str(self.root_path)+'/models/fModel.h5')


    def decode_review(self,words):
        try:
            trans = Translator()
            result = trans.translate(words, dest='en')
            words = result.text
            words = words.replace('.', '')
            words = words.split(' ')
        except ConnectError as con_e:
            print(con_e)
            self.result_text.setStyleSheet('color : #ff7f00')
            self.result_text.setText("Please connecting the internet :(")
            return


        e_words = list()
        e_words.append(1)
        for word in words:
            tmp = self.word_index.get(word.lower())

            if tmp is not None and tmp >= 10000:
                e_words.append(3)
            elif tmp is None:
                e_words.append(2)
            else:
                e_words.append(tmp)

        while len(e_words) < 256:
            e_words.append(0)

        e_words = np.array(e_words)
        test_data_test = np.array([e_words, ])
        res = self.model.predict_classes(test_data_test)
        # print(res[0])
        # print(type( res[0][0]))

        if res[0][0] < 1:
            self.result_text.setStyleSheet('color : red')
            self.result_text.setText("negative review")

        else:
            self.result_text.setStyleSheet('color : blue')
            self.result_text.setText("positive review")