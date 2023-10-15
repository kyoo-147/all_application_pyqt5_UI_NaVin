import sys
import os
import cv2
import numpy as np
import json
from PIL import Image, ImageFont, ImageDraw

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from urllib.request import urlretrieve
import requests

from keras.models import Model,load_model
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from yolo_detector import YOLO_detect
from yolo_multiple_output import YOLO, YOLO2

import time

yolo = YOLO()
yolo2 = YOLO2()
yolo_detect = YOLO_detect()

global link
link = []

class Ui_webcam(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_webcam, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()  # 初始化定時器
        self.cap = cv2.VideoCapture()  # 初始化攝像頭
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.label_type = str(0)
        self.label_class = str(0)
        self.all_link =[]

    def set_ui(self):
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.label_pic = QtWidgets.QLabel(self.centralwidget)
        self.label_pic.setGeometry(QtCore.QRect(600, 550, 300, 120))
        self.label_pic.setText("")
        pixmap = QtGui.QPixmap("figures/origin-logo.png")
        self.label_pic.setPixmap(pixmap.scaled(150, 150))
        self.label_pic.setObjectName("label_pic")

        self.__layout_main = QtWidgets.QHBoxLayout()  # 採用QHBoxLayout類，按照從左到右的順序來添加控件
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()  # QVBoxLayout類垂直地擺放小部件

        self.button_open_camera = QtWidgets.QPushButton(u'打開相機')
        self.button_close = QtWidgets.QPushButton(u'退出')
        self.button_open_camera.resize(70,50)
        self.button_close.resize(50,10)

        # move()方法是移動窗口在屏幕上的位置到x = 500，y = 500的位置上
        self.move(500, 500)

        # 信息顯示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)

        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.label_pic)
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.label_move)


        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)

        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'攝像頭')

    def slot_init(self):  # 建立通信連接
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'請檢測相機與電腦是否連接正確',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.button_open_camera.setText(u'關閉相機')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打開相機')

    def show_camera(self):
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (640, 480))
        show = cv2.flip(show, 1)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(show)
        r_image, output_boxes, output_classes, label_t = yolo.detect_image(image)
        for i in range(0, len(output_boxes)):
            box = output_boxes[i]
            image_detect2 = r_image.crop([box[1]+3, box[0]+3, box[3]-3, box[2]-3])
            pil_img = Image.fromarray(np.array(image_detect2))
            pil_img.save('image/0.jpg')
            v = 0
            output_scores2, output_classes2, bg = yolo2.detect_image(image_detect2, v)
            font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                                      size=np.floor(3e-2 * r_image.size[1] + 0.5).astype('int32'))
            thickness = (r_image.size[0] + r_image.size[1]) // 300
            if (output_scores2 != 0) & (output_classes[i] != 5):
                label = '{} {:.2f}'.format(output_classes2, output_scores2)
                draw = ImageDraw.Draw(r_image)
                label_size = draw.textsize(label, font)

                top, left, bottom, right = box
                top = max(0, np.floor(top + 0.5).astype('int32'))
                left = max(0, np.floor(left + 0.5).astype('int32'))
                bottom = min(r_image.size[1], np.floor(bottom + 0.5).astype('int32'))
                right = min(r_image.size[0], np.floor(right + 0.5).astype('int32'))
                print(label, (left, top), (right, bottom))
                if top - label_size[1] >= 0:
                    text_origin = np.array([left, top - 2 * label_size[1]])
                else:
                    text_origin = np.array([left, 2 * (top + 1)])
                draw.rectangle(
                    [tuple(text_origin), tuple(text_origin + label_size)],
                    fill=bg)
                draw.text(text_origin, label, fill=(0, 0, 0), font=font)
                del draw
                global label_t
                global label_color
                label = label.split(' ')
                label_color = label
                label_type = label_t.split(' ')

                self.label_class = label_color[0]
                self.label_type = label_type[0]

        result = np.asarray(r_image)
        showImage = QtGui.QImage(result, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))

        if len(self.label_class) != 1:
            if len(self.label_type) != 1:
                label_name={'backpack': '後背包',
                'cross_bag': '斜背包',
                'satchel_bag': '側背包',
                 'handbag': '手提包',
                'fanny_pack':'腰包'
                }.get(self.label_type, 'error')  # 'error'為預設返回值，可自設定

                color_name={'black':'黑色',
                            'red':'紅色',
                            'white':'白色',
                            'blue':'藍色',
                            'brown':'咖啡色',
                            'yellow':'黃色',
                            'green':'綠色',
                            'gray':'灰色',
                            'pink':'粉紅色',
                            'orange':'橘色',
                            'other':'',
                            'white':'白色',
                            'purple':'紫色'
                            }.get(self.label_class,'error')
              
                name = '{}{}'.format(color_name, label_name)
                print(name)

                crawler.productsearch(name)
                crawler.pchomeinfo(self)
                if self.cap.isOpened():
                    self.cap.release()
                if self.timer_camera.isActive():
                    self.timer_camera.stop()
                index = AE_sort.sort(self)
                link = crawler.link(self)

                urlLink1 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black>pick me</font> </a>".format(url=link[index[1]-1][0])
                btn.clicked.connect(lambda: l1.setText(urlLink1))
                l1.setOpenExternalLinks(True)
                req1 = requests.get(link[index[1]-1][1])
                photo1 = QPixmap()
                photo1.loadFromData(req1.content)
                btn.clicked.connect(lambda: ui1.setPixmap(photo1.scaled(200, 200)))

                urlLink2 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black>pick me</font> </a>".format(url=link[index[2]-1][0])
                btn.clicked.connect(lambda: l2.setText(urlLink2))
                l2.setOpenExternalLinks(True)
                req2 = requests.get(link[index[2]-1][1])
                photo2 = QPixmap()
                photo2.loadFromData(req2.content)
                btn.clicked.connect(lambda: ui2.setPixmap(photo2.scaled(200,200)))

                urlLink3 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black>pick me</font> </a>".format(url=link[index[3]-1][0])
                btn.clicked.connect(lambda: l3.setText(urlLink3))
                l3.setOpenExternalLinks(True)
                req3 = requests.get(link[index[3]-1][1])
                photo3 = QPixmap()
                photo3.loadFromData(req3.content)
                btn.clicked.connect(lambda: ui3.setPixmap(photo3.scaled(200,200)))

                urlLink4 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black>pick me</font> </a>".format(url=link[index[4]-1][0])
                btn.clicked.connect(lambda: l4.setText(urlLink4))
                l4.setOpenExternalLinks(True)
                req4 = requests.get(link[index[4]-1][1])
                photo4 = QPixmap()
                photo4.loadFromData(req4.content)
                btn.clicked.connect(lambda: ui4.setPixmap(photo4.scaled(200,200)))

                urlLink5 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black>pick me</font> </a>".format(url=link[index[5]-1][0])
                btn.clicked.connect(lambda: l5.setText(urlLink5))
                l5.setOpenExternalLinks(True)
                req5 = requests.get(link[index[5]-1][1])
                photo5 = QPixmap()
                photo5.loadFromData(req5.content)
                btn.clicked.connect(lambda: ui5.setPixmap(photo5.scaled(200,200)))

                urlLink6 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black>pick me</font> </a>".format(url=link[index[6]-1][0])
                btn.clicked.connect(lambda: l6.setText(urlLink6))
                l6.setOpenExternalLinks(True)
                req6 = requests.get(link[index[6]-1][1])
                photo6 = QPixmap()
                photo6.loadFromData(req6.content)
                btn.clicked.connect(lambda: ui6.setPixmap(photo6.scaled(200,200)))

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'關閉', u'是否關閉！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'確定')
        cancel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()

class Ui_MainWindow(QWidget):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.url = url
        
        req = requests.get(self.url)
        photo = QPixmap()
        photo.loadFromData(req.content)

        self.label = QLabel()
        self.label.setPixmap(photo.scaled(200,200))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class crawler(object):
    def __init__(self, parent=None):
        super(crawler, self).__init__(parent)
        self.all_link = []
    def productsearch(main):
        global pchomesearch
        global itemname
        global shpsearch
        str(main)
        pchome = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='

        pchomesearch = pchome + main
        shp1 = 'https://shopee.tw/search/?keyword='
        shp2 = '&sortBy=sales'
        shpsearch = shp1 + main + shp2
        print("Pchome24H購物:")
        print(pchomesearch)

    def pchomeinfo(self):
        global pchomesearch
        res = requests.get(pchomesearch)
        ress = res.text
        jd = json.loads(ress)
        pcitems = []
        pcprices = []
        pcurls = []
        picurls = []
        pcmainurl = 'http://24h.pchome.com.tw/prod/'
        picmainurl = 'https://b.ecimg.tw/'
        f = open('link.txt', 'w')
        for n in range(1, 11):
            try:
                for item in jd['prods']:
                    pcitems.append(item['name'])
                    pcprices.append(item['price'])
                    url = pcmainurl + item['Id']
                    pcurls.append(url)
                    picurl = picmainurl + item['picB']
                    picurls.append(picurl)
                pcitems0 = pcitems[n]
                pcprices0 = pcprices[n] # price
                pcurls0 = pcurls[n]     # URL
                picurls0 = picurls[n]   # bag_image
            except:
                pcitems0 = '唤哦,查無相關資料'
                pcprices0 = '噢哦,查無相關資料'
                pcurls0 = '噢哦,查無相關資料'
                picurls = '噢哦,查無相關資料'
            print(pcurls0)
            f.write(pcurls0+'\n')
            f.write(picurls0+'\n')

            if self.all_link == []:
                self.all_link = [[pcurls0]]
                self.all_link.append([picurls0])
            else:
                self.all_link.append([pcurls0])
                self.all_link.append([picurls0])

            local = os.path.join('image\\%s.jpg' % n)
            urlretrieve(picurls0, local)
        self.all_link = np.array(self.all_link).reshape(10, 2)
    def link(self):
        return self.all_link

class AE_sort():
    def cosine_similarity(ratings):
        sim = ratings.dot(ratings.T)
        if not isinstance(sim, np.ndarray):
            sim = sim.toarray()
        norms = np.array([np.sqrt(np.diagonal(sim))])
        return (sim / norms / norms.T)
    def sort(self):
        imgDB_size = 11
        imagepath = 'image/'
        img_path = os.listdir(imagepath)
        for p in img_path:
            fullpath = os.path.join(imagepath, p)
            img = Image.open(fullpath)
            r_image, boxes, classes, scores, time = yolo_detect.detect_image(img)
            if len(scores) > 0:
                max_score = np.argmax(scores)
                image_detect2 = r_image.crop(
                    [boxes[max_score][1], boxes[max_score][0], boxes[max_score][3], boxes[max_score][2]])
                image_detect2.save(imagepath + p)
        X = []       
        for im in range(imgDB_size):
            img_path = imagepath+str(im) + '.jpg'
            print(img_path)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (32,32), interpolation=cv2.INTER_CUBIC)
            img = img.reshape(32 * 32 * 3)                   
            X.append(img)
        X = np.array(X)
        X = X/255.0

        model = load_model('model_data/encoder_model_deep.h5')
        X_ae = model.predict(X)
        X_ae = np.array(X_ae)
        features = X_ae.reshape(imgDB_size, 256)           

        sim = AE_sort.cosine_similarity(features)
        index1 = np.argsort(-sim[0])
        fea = []
        for i in range(imgDB_size):
            fe = np.round(sum(abs(features[i]-features[0])), 2)
            find = list(np.where(fea == fe))
            flag = 0
            for j in fea:
                if j == fe:
                    flag = 1
            if flag == 0:
                fea.append(fe)
            else:
                fea.append(1000000)
                #fea.append(fe)
        index = np.argsort(fea)
        return index


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    webcam=Ui_webcam()

    url1='https://b.ecimg.tw//items/DCAGMVA9009Q76N/000001_1565577423.jpg'
    url2='https://b.ecimg.tw//items/DICMHYA9009T0V1/000001_1550291342.jpg'
    url3='https://b.ecimg.tw//items/DGBX19A9008BED8/000001_1501754321.jpg'
    url4='https://b.ecimg.tw//items/DIBA89A9009RVZ1/000001_1558489835.jpg'
    url5='https://b.ecimg.tw//items/DGCN0VA9009CAIU/000001_1534927659.jpg'
    url6='https://b.ecimg.tw//items/DCAGMV1900A6GNN/000001_1564571586.jpg'

    photo = QPixmap()
    label = QLabel()
    label.setPixmap(photo.scaled(200, 200))

    photo2 = QPixmap()
    label2 = QLabel()
    label2.setPixmap(photo2.scaled(200, 200))

    photo3 = QPixmap()
    label3 = QLabel()
    label3.setPixmap(photo3.scaled(200, 200))

    photo4 = QPixmap()
    label4 = QLabel()
    label4.setPixmap(photo4.scaled(200, 200))

    photo5 = QPixmap()
    label5 = QLabel()
    label5.setPixmap(photo5.scaled(200, 200))

    photo6 = QPixmap()
    label6 = QLabel()
    label6.setPixmap(photo6.scaled(200, 200))

    ui1 = label
    ui2 = label2
    ui3 = label3
    ui4 = label4
    ui5 = label5
    ui6 = label6

    urlLink1 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black> </font> </a>".format(url=url1)
    l1 = QtWidgets.QLabel()
    l1.setText(urlLink1)

    urlLink2 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black> </font> </a>".format(url=url2)
    l2 = QtWidgets.QLabel()
    l2.setText(urlLink2)
    
    urlLink3 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black> </font> </a>".format(url=url3)
    l3 = QtWidgets.QLabel()
    l3.setText(urlLink3)

    urlLink4 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black> </font> </a>".format(url=url4)
    l4 = QtWidgets.QLabel()
    l4.setText(urlLink4)

    urlLink5 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black> </font> </a>".format(url=url5)
    l5 = QtWidgets.QLabel()
    l5.setText(urlLink5)

    urlLink6 = " <a href=\"{url}\"> <font face=Tw Cen MT Condensed size=2 color=black> </font> </a>".format(url=url6)
    l6 = QtWidgets.QLabel()
    l6.setText(urlLink6)

    sub_layout1 = QtWidgets.QVBoxLayout()
    sub_layout1.addWidget(ui1)
    sub_layout1.addWidget(l1)
    sub_layout1.addWidget(ui2)
    sub_layout1.addWidget(l2)

    sub_layout2 = QtWidgets.QVBoxLayout()
    sub_layout2.addWidget(ui3)
    sub_layout2.addWidget(l3)
    sub_layout2.addWidget(ui4)
    sub_layout2.addWidget(l4)

    sub_layout3 = QtWidgets.QVBoxLayout()
    sub_layout3.addWidget(ui5)
    sub_layout3.addWidget(l5)
    sub_layout3.addWidget(ui6)
    sub_layout3.addWidget(l6)

    btn = QPushButton('顯示結果')

    main_layout = QtWidgets.QHBoxLayout()

    main_layout.addWidget(webcam)
    main_layout.addWidget(btn)
    main_layout.addLayout(sub_layout1)
    main_layout.addLayout(sub_layout2)
    main_layout.addLayout(sub_layout3)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(main_layout)

    main_window = QtWidgets.QMainWindow()

    main_window.setCentralWidget(layout_widget)
    # 設置背景顏色
    palette1 = QPalette()
    palette1.setBrush(main_window.backgroundRole(), QBrush(QPixmap('figures/background.jpg')))
    main_window.setPalette(palette1)

    main_window.show()
    app.exec_()
