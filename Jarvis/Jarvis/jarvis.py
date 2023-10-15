import sys
from socket import timeout
import cv2
import pyaudio
import pyttsx3
from requests import get
import speech_recognition as sr
import datetime 
import os
import webbrowser as web
import pywhatkit as kit
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvisui import Ui_MainWindow
import smtplib
import wikipedia
import pyjokes
import random
from playsound import playsound
from pyautogui import click
from keyboard import press
from keyboard import press_and_release
from keyboard import write
from time import sleep
import subprocess,os



engine =pyttsx3.init("sapi5")
voices =engine.getProperty("voices")
engine.setProperty("voices",voices[1].id)

def speak(audio):
    
    print(f": {audio}")
    engine.say(audio)
    engine.runAndWait()
    print(" ")
    
def wish():
        hour = int( datetime.datetime.now().hour )

        if hour >= 0 and hour <= 12:
            speak( "good morning" )
        elif hour>12 and hour<18:
            speak( "good afternoon" )
        else:
            speak( "good evening" )
        speak("i am jarvis sir  please tell me how can i help for you")

def sendEmail(to, content):
                server = smtplib.SMTP( "smtp.gmail.com", 587 )
                server.ehlo()
                server.starttls()
                server.login( "ravianimation@gmail.com", "oshjehrypxdhavus" )  # oshjehrypxdhavus
                server.sendmail( "ravianimation@gmail.com", to, content )
                server.close()

class Harry(QThread):
                def __init__(self):
                    super(Harry,self).__init__()
                def run(self):
                    self.TaskExecution()

                # to convert voice to txt

                def takecommand(self):
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        print(": Listening....")
                        print(" ")
                        r.pause_thread=1
                        audio=r.listen( source, timeout=10,phrase_time_limit=20 )
                    try:
                        print(": Recognizing...")
                        print(" ")
                        query = r.recognize_google( audio, language="en-in" )
                        print(f": Your Command : {query}\n")

                    except Exception as e:
                        speak( "say that again please..." )
                        return "none"
                    return query

                def TaskExecution(self):
                    playsound('1.mp3')
                    wish()
            
                    while True:
                        self.query = self.takecommand().lower()
                        
                        if "open notepad" in self.query:
                            speak( "okay sir , opening notepad" )
                            npath = "C:\\Windows\\system32\\notepad.exe"
                            os.startfile( npath )

                        elif "close notepad" in self.query:
                            speak( "okay sir , closing notepad" )
                            os.system( "taskkill /f /im notepad.exe" )

                        elif "open cmd" in self.query:
                            speak( "okay sir , opening cmd" )
                            os.system( "start cmd" )  

                        #elif "close cmd" in self.query:
                           # speak( "okay sir , closing cmd" )
                           # os.system( "taskkill /f /im cmd.exe" )  

                        elif "open camera" in self.query:
                            speak( "okay sir , opening camera" )
                            subprocess.run('start microsoft.windows.camera:', shell=True)

                        elif "close camera" in self.query:
                            speak( "okay sir , closing camera" )
                            subprocess.run('Taskkill /IM WindowsCamera.exe /F', shell=True)

                        elif "play music" in self.query:
                            music_dir = 'Music\\'
                            songs = os.listdir(music_dir)
                            rd=random.choice(songs)
                            for song in songs:
                                if song.endswith( ".mp3" ):
                                    os.startfile( os.path.join( music_dir, song ) )

                        elif "ip address" in self.query:
                            ip = get( "https://api.ipify.org" ).text
                            speak( f"your IP address is {ip}" )

                        elif "open youtube" in self.query:
                            web.open( "www.youtube.com" )

                        elif "open facebook" in self.query:
                            web.open( "www.facebook.com" )

                        elif "open google map" in self.query:
                            web.open( "www.google.com/maps/" )

                        elif "open google" in self.query:
                            speak( "sir, what should i search on google" )
                            cm = self.takecommand().lower()
                            web.open( f"{cm}" )

                        elif "you can sleep now" in self.query:
                            speak("thanks for using me sir, have a good day")
                            sys.exit()

                        elif "set alarm" in self.query:
                            time1 = int( datetime.datetime.now().hour )
                            if time1 == 19:         #change time
                                music_dir = 'alarm\\'
                                songs = os.listdir( music_dir )
                                os.startfile( os.path.join( music_dir, songs[0] ) )

                        elif "tell me joke" in self.query :
                            joke = pyjokes.get_joke()
                            speak( joke )
                        elif "shutdown" in self.query:
                            os.system( "shutdown /s /t 5" )

                        elif "restart" in self.query:
                            os.system( "shutdown /r /t 5" )

                        elif "sleep" in self.query:
                            os.system( "rundll32.exe powrprof.dll,SetSuspendState 0,1,0" )
#---------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------New Function-----------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
                        elif 'youtube search' in self.query:
                            self.Query = self.query.replace("jarvis","")
                            self.query = self.Query.replace("youtube search","")
                            
                            from Features import YouTubeSearch
                            YouTubeSearch(self.query)
                        
                        elif 'my location' in self.query:
                            from Features import My_Location
                            My_Location()

                        elif 'where is' in self.query:
                            from Automations import GoogleMaps
                            Place = self.query.replace("where is ","")
                            Place = Place.replace("jarvis" , "")
                            GoogleMaps(Place)

                        elif 'write a note' in self.query:
                            from Automations import Notepad
                            Notepad()

                        elif 'time table' in self.query:
                            from Automations import TimeTable
                            TimeTable()
#---------------------------------------------------------------------------------------------------------------------------------
                        elif 'whatsapp message' in self.query:
                            
                            name = self.query.replace("whatsapp message","")
                            name = name.replace("send ","")
                            name = name.replace("to ","")
                            name = name.replace("jarvis ","")
                            Name = str(name)
                            speak(f"Whats The Message For {Name}")
                            MSG = self.takecommand()
                            from Automations import WhatsappMsg
                            WhatsappMsg(Name,MSG)

                        elif 'whatsapp voice call to' in self.query:
                            
                            name = self.query.replace("whatsapp voice call to","")
                            name = name.replace("jarvis ","")
                            Name = str(name)
                            from Automations import WhatsappCall
                            WhatsappCall(Name)

                        elif 'whatsapp video call to' in self.query:
                            
                            name = self.query.replace("whatsapp video call to","")
                            name = name.replace("jarvis ","")
                            Name = str(name)
                            from Automations import WhatsappvideoCall
                            WhatsappvideoCall(Name)

                        elif 'whatsapp chat so' in self.query or 'whatsapp chat so' in self.query or 'whatsapp chat show' in self.query:
                            speak("With Whom ?")
                            name = self.takecommand()
                            from Automations import WhatsappChat
                            WhatsappChat(name)
#---------------------------------------------------------------------------------------------------------------------------------
                        elif'open age' in self.query:
                            web.open( "www.google.com" )
                        
                        elif 'age automation'in self.query or 'age auto' in self.query or 'edge automation' in self.query or 'edge auto' in self.query:
                            from Automations import MicrosoftedgeAuto
                            MicrosoftedgeAuto(self.query)
                            

                        elif 'windows automation'in self.query or 'windows auto' in self.query:
                            from Automations import WindiowsAuto
                            WindiowsAuto(self.query)

                        elif 'youtube automation'in self.query or 'youtube auto' in self.query:
                            YouTubeAuto(self.query)
            
#---------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------Youtube Function-----------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
                        elif 'stop video' in self.query or 'top video' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'resume video' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'full screen' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'film screen' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'forward video' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'backward video' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'increase speed' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        #elif 'decrease speed' in query:
                        # press_and_release('SHIFT + ,')
                            #Speak("done sir")

                        elif 'play previous video' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'play next video' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'search on youtube' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)
                        
                        elif 'mute' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)

                        elif 'unmute' in self.query:
                            from Automations import YouTubeAuto
                            YouTubeAuto(self.query)
#--------------------------------------------------------------------------------------------------------------------------------- 
#--------------------------------------------------Windows Function------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------  
                        elif 'home screen' in self.query:
                            from Automations import WindiowsAuto
                            WindiowsAuto(self.query)

                        elif 'minimize' in self.query or 'minimise' in self.query:
                            from Automations import WindiowsAuto
                            WindiowsAuto(self.query)

                        elif 'show start' in self.query or 'so start' in self.query:
                            from Automations import WindiowsAuto
                            WindiowsAuto(self.query)

                        elif 'open setting' in self.query:
                            from Automations import WindiowsAuto
                            WindiowsAuto(self.query)

                        elif 'open search' in self.query:
                            from Automations import WindiowsAuto
                            WindiowsAuto(self.query)

#--------------------------------------------------------------------------------------------------------------------------------- 
#--------------------------------------------------Microsoft Browser Function------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------

                        elif 'new tab' in self.query:
                            from Automations import MicrosoftedgeAuto
                            MicrosoftedgeAuto(self.query)
                            #press_and_release('ctrl + t')
                            #speak("done sir")

                        elif 'close tab' in self.query:
                            from Automations import MicrosoftedgeAuto
                            MicrosoftedgeAuto(self.query)

                        elif 'open new window' in self.query:
                            from Automations import MicrosoftedgeAuto
                            self.query=self.query.replace("open", "")
                            MicrosoftedgeAuto(self.query)

                        elif 'open history' in self.query:
                            from Automations import MicrosoftedgeAuto
                            MicrosoftedgeAuto(self.query)

                        elif 'open download' in self.query:
                            from Automations import MicrosoftedgeAuto
                            MicrosoftedgeAuto(self.query)

                        elif 'bookmark' in self.query:
                            from Automations import MicrosoftedgeAuto
                            MicrosoftedgeAuto(self.query)

                        elif 'open in browser' in self.query:
                            from Automations import MicrosoftedgeAuto
                            MicrosoftedgeAuto(self.query)
                            

                            

#--------------------------------------------------------------------------------------------------------------------------------- 
#---------------------------------------------------------Windows Function------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------- 

#---------------------------------------------------------------------------------------------------------------------------------
                        speak("sir, do you have any other work")




                  #to wish
startExecution = Harry()
   # speak("i am jarvis sir  please tell me how can i help for you")
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
        
    def startTask(self):
        self.ui.movie = QtGui.QMovie("images/jarvis_robot.gif")
        self.ui.jarvis_gif.setMovie(self.ui.movie)
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie( "images/main video.gif")
        self.ui.main_gif.setMovie( self.ui.movie )
        self.ui.movie.start()

        self.ui.movie = QtGui.QMovie( "images/intial_loading.gif")
        self.ui.intial_loadin_gif.setMovie( self.ui.movie )
        self.ui.movie.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(2000)
        startExecution.start()
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_time)
        self.ui.textBrowser_2.setText( label_date)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())




