from PyQt5 import QtCore, QtGui, QtWidgets
import Reso

from datetime import datetime
import sys



# Initializing Login UI Window

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1532, 768)
        MainWindow.setStyleSheet("font: 12pt \"Droid Sans Fallback\";\n"
"border-color: rgb(5, 255, 255);\n"
"background-color: rgb(0, 0, 0);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(800, 30, 401, 91))
        self.label.setStyleSheet("gridline-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85, 170, 255);\n"
"\n"
"font: 40pt \"Ravie\";")


        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(680, 20, 111, 111))
        self.frame_2.setStyleSheet("image: url(:/newPrefix/logo.png);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(610, 190, 751, 431))
        self.frame_3.setStyleSheet("border-color: rgb(85, 255, 255);\n"
"background-color: rgb(61, 185, 185);")


        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(70, 130, 191, 241))
        self.label_5.setStyleSheet("image: url(:/newPrefix/chat.jpg);")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.frame = QtWidgets.QFrame(self.frame_3)
        self.frame.setGeometry(QtCore.QRect(260, 60, 431, 361))
        self.frame.setStyleSheet("border-color: rgb(85, 255, 255);\n"
"border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(85, 255, 255, 170), stop:1 rgba(255, 255, 255, 255));\n"
"")


        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(10)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(250, 290, 181, 41))
        self.pushButton.setStyleSheet("background-color: rgb(32, 139, 239);\n"
"color: rgb(0, 255, 255);")


        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.InsertData)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(50, 80, 101, 31))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(50, 120, 171, 23))
        self.textEdit.setStyleSheet("\n" "color: rgb(255, 121, 26);"
"background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:1, stop:0.536842 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")


        self.textEdit.setObjectName("textEdit")
        self.textEdit.setAcceptRichText(False)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(50, 170, 111, 21))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame)
        self.textEdit_2.setGeometry(QtCore.QRect(50, 200, 171, 23))
        self.textEdit_2.setStyleSheet("\n" "color: rgb(255, 121, 26);"
"background-color: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:1, stop:0.536842 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")


        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setAcceptRichText(False)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(320, 20, 91, 71))
        self.label_4.setStyleSheet("gridline-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));\n"
"font: 23pt \"Comic Sans MS\";\n"
"color: rgb(17, 85, 255);\n"
"\n"
"\n"
"")



        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1532, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Packing wedgits in window 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "ChatBot"))
        self.pushButton.setText(_translate("MainWindow", "Login"))
        self.label_2.setText(_translate("MainWindow", "Username"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.label_4.setText(_translate("MainWindow", "Login"))

    


    # Fetching User Info
    def loggedin(self):
        username = self.textEdit.toPlainText()
        print(username)
        password = self.textEdit_2.toPlainText()
        print(password)


    # Inserting Data into DataBase
    def InsertData(self):
        username = self.textEdit.toPlainText()
        password = self.textEdit_2.toPlainText()

        # db = mysql.connector.connect(
        # host = "localhost/Server IP Address",
        # user = "YourUserName",
        # passwd = "YourPassword",
        # database = "ChatBot_Base"

        # )

        # mycursor = db.cursor()

        # mycursor.execute("INSERT INTO BotUserData (username,password,logintime) VALUES (%s,%s,%s)",(username,password,datetime.now()))  
        # db.commit()
        # mycursor.execute("SELECT * FROM BotUserData")

        # Authenticaing users 
 

        # for details in mycursor:
        #     print(details)
        if password == "1234" :
            from subprocess import call 
            MainWindow.close()
            # Redirecting to Main Window
        #     call(["python","C:\\Users\\91738\\Desktop\\ChatBot_Project_FInal\\ChatbotUI.py"])

            #ADD MainChatbot.py File Location whenever you download it 
            call(["python","D:\\Coding\\VsCode\\New folder\\Chatbot-Alice\\MainChatbot.py"])
            

                
                
            

# UI setup 

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())
