from PyQt5 import QtCore, QtGui, QtWidgets           #GUI Libs
from datetime import datetime                        #Time module
from datetime import date
import pyjokes                                       #Jokes module 
import time                                             
# import mysql.connector                               # DBMS 
import Reso                                          # Importing Resource file
# from playsound import playsound

# Initializing UI Window
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2445, 943)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 190, 752, 29))
        self.label_2.setStyleSheet("color: rgb(255, 90, 7);\n"
"background-color: rgb(0, 0, 0);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(0, 0, 0, 0));\n"
"font: 14pt \"MV Boli\";\n"
"text-decoration: underline;")

        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(630, 150, 751, 161))
        self.label_3.setStyleSheet("color: rgb(255, 90, 7);\n"
"background-color: rgb(0, 0, 0);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(0, 0, 0, 0));\n"
"font: 14pt \"MV Boli\";\n"
"text-decoration: underline;")

        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(680, 680, 60, 31))
        self.label_4.setStyleSheet("color: rgb(255, 90, 7);\n"
"font: 16pt \"Forte\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(0, 0, 0, 0));")
        self.label_4.setObjectName("label_4")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(750, 270, 411, 411))
        self.textEdit_2.setStyleSheet("font: 12pt \"Times New Roman\";\n" 
"color: rgb(136, 255, 247);")

        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.append("\t\tWelcome !\n   This is Alice A ChatBot ! How may i assist you?")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1560, 740, 96, 36))
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(136, 255, 247);\n" 
"font: 14pt \"High Tower Text\";")
        self.pushButton_2.setObjectName("pushButton_2")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 10, 151, 111))
        self.frame.setStyleSheet("image: url(:/newPrefix/logo.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(1560, 790, 301, 31))
        self.textEdit_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(0, 0, 0, 0));\n"
"font: 10pt \"Times New Roman\";")
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_3.setAcceptRichText(False)
        

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(200, 0, 595, 133))
        self.label.setStyleSheet("color: rgb(85, 255, 255);\n"
"font: 60pt \"Ravie\";")

        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 140, 2931, 20))
        self.line.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(0, 0, 0, 255));\n"
"color: rgb(0, 0, 0);")

        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1680, 70, 93, 41))
        self.pushButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0,0,0,0));\n"
"font: 16pt \"Mongolian Baiti\";\n"
"color: rgb(85, 255, 255);\n"
"")

        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.logout)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(750, 680, 361, 31))
        self.textEdit.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255));\n"
"color: rgb(0, 0, 0);\n"
"font: 10pt \"Times New Roman\";")

        self.textEdit.setObjectName("textEdit")
        self.textEdit.setAcceptRichText(False)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1780, 830, 81, 41))
        self.pushButton_3.setStyleSheet("font: 10pt \"Mongolian Baiti\";\n"
"color: rgb(85, 255, 255);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0,0,0,0));")

        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.ressed)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1110, 680, 51, 31))
        self.pushButton_4.setStyleSheet("image: url(:/newPrefix/logo (1).png);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0,0,0,0));")

        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.givemytext)
        self.pushButton_4.clicked.connect(self.clearing)
        
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 270, 491, 451))
        self.frame_2.setStyleSheet("image: url(:/newPrefix/chat.jpg);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(1360, 260, 511, 451))
        self.frame_3.setStyleSheet("image: url(:/newPrefix/Human_AI_final.jpg);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.pushButton_2.raise_()
        self.frame.raise_()
        self.textEdit_3.raise_()
        self.textEdit_2.raise_()
        self.label.raise_()
        self.line.raise_()
        self.pushButton.raise_()
        self.textEdit.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.frame_2.raise_()
        self.frame_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2445, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ChatBot - Alice"))
        self.label_2.setText(_translate("MainWindow", "\"We are no longer teaching people how to communicate with system"))
        self.label_3.setText(_translate("MainWindow", "we\'re teaching systems to communicate with people.\""))
        self.label_4.setText(_translate("MainWindow", "Type:"))
        self.pushButton_2.setText(_translate("MainWindow", "Feedback"))
        self.label.setText(_translate("MainWindow", "CHATBOT"))
        self.pushButton.setText(_translate("MainWindow", "Logout"))
        self.pushButton_3.setText(_translate("MainWindow", "Submit"))

    # Data processing

    def givemytext(self,textpass):
        textpass = self.textEdit.toPlainText().lower()
        self.textEdit_2.append(f" You : {f'{textpass}'}")
    
        # Fetching time from Time module
        t  = datetime.now()
        hr  = t.strftime("%I")
        min  = t.strftime("%M")
        period  = t.strftime("%p")
        # song = playsound('C:\\Users\\91738\\Desktop\\ChatBot_FInal\\Despacito.mp3')

        jokes = pyjokes.get_joke()
        Current_Time = f"{hr}:{min} {period}"
        
        # Initializing dict
        
        respo_dict = {


                    "hi":"Hello, how are you?",
                    "hello":"Hi,How are you doing?",
                    "good morning": "Good morning ,How are you doing?",
                    "good afternoon":"Good afternoon, How can i help you?",
                    "good evening":"Good evening , How are you?",
                        
        }

        Intro_dict = {
                            "who are you": "I am Alice,How can i help you",
                            "what is your name":"I am  Alice , a bot",
                            "what is your age ":"I am bot, created by fellow programmers",
                            "how are you " : "Hey I am good , How are you doing?",
                            "tell me something about yourself":"Hey I am Alice - a bot ,I was programmed by RT's Developers to assist you",
                            
                } 
        
        Filter_dict = {
                            ''' You can write any words that you want to filter from user input ''': '''#####'''
                            
                        }
        Prob_dict = {

                        "what you can do":"I can perform multiple number of tasks like human interaction,songs,date,timejokes,..etc",
                        "time":f"The current time is {Current_Time}",
                        "who developed you":"TEAM PROTON - Lead by Younus",
                        "reminder":"Reminder is set for",
                        "date":f"Today's date - {date.today()}",
                        "where do you live":"I live in a server of las vegas..",
                        "when is your birthday":"30 Feb",
                        "are you a human being":"No i am Alice - a chatbot",
                        "what is your purpose":"I am here to assist you...",
                        "what do you eat":"I consume electricity",
                        "which languages do you speak":"I speak same as you",
                        "tell me a joke":f"{jokes}",
                        "recomend me a movie":"Silicon valley",  
                        # "song":f"{song}"



                    }

        Terminate_dict = {

                                "exit":"Thank you for using me...!Bye.",
                                "bye":"See you next time...",
                                "good night":"Good night...",
                                "sleep":"Good night....!Bye",
                                "kill":"See you in after live",
                                
                                
                            } 
        
        # Assigning keys 
        Terminating_Server = Terminate_dict.keys() 

        # Merging dicts
        def Merge(dict1, dict2):
            for i in dict2.keys():
                dict1[i]=dict2[i]
            return dict1


        d1 = Merge(respo_dict,Intro_dict)
        d2 = Merge(Prob_dict,Filter_dict)
        d3 = Merge(d1,d2)
        d4 = Merge(d3,Terminate_dict)
        
        # BOT responses
        try:

            xx = d4.keys()
            if textpass in xx and textpass not in Terminating_Server:
                reply = d4.get(textpass)
                print(f"Alice : {reply} ")

            if textpass not in xx :
                reply = "Given inuput is not recorginized..."
                print(reply)
                                
            elif textpass in Terminating_Server :
                print("Your session terminated...")
                time.sleep(2)
                exit()

            else :
                Not_rec = "Given input is not recoginised..."

        except Exception as e :

            return f"An error Occured : {e}"
        
        self.textEdit_2.append(f"| Alice | : " + f'{reply}\n')
        print(textpass)
        print(reply)
        response_list = []

        # Fething user data & Bot data
        
        def DataManagment(self) :
            responses = response_list.append(reply)
            feedtext = self.textEdit_3.toPlainText()
        
            # Initializing Database with MySQL

        #     db = mysql.connector.connect(
        #         host="localhost/Server IP Address",
        #         user = "YourUserName",
        #         passwd = "YourPassword",
        #         database = "ChatBot_Base"
        #         )

        #     mycursor = db.cursor()
        #     responses = str(responses)

        #     # Inserting fetched data into database

        #     mycursor.execute("INSERT INTO BotUserData (user_query,Bot_response,feedback) VALUES (%s,%s,%s)",(textpass,reply,feedtext))
        #     db.commit()

        #     mycursor.execute("SELECT * FROM BotUserData")

        #     for details__ in mycursor :
        #         print(details__)


        # DataManagment(self)


    def clearing(self):
        
        self.textEdit.clear()
        
    def ressed(self):
        feedtext = self.textEdit_3.toPlainText()
        self.textEdit_3.clear()
        print(feedtext)

    def logout(self):
            exit()

# UI setup 

if __name__ == "__main__":  
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())
    
