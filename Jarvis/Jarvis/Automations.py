from datetime import datetime
from os import startfile
import os
from pyautogui import click
from keyboard import press
from keyboard import press_and_release
from keyboard import write
from time import sleep
from notifypy import Notify
import pyttsx3
import speech_recognition as sr
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import webbrowser as web

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def Speak(audio):
    print(" ")
    print(f": {audio}")
    engine.say(audio)
    engine.runAndWait()
    print(" ")

def TakeCommand():
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
        Speak( "say that again please..." )
        return "none"
    return query

def GoogleMaps(Place):

    Url_Place = "https://www.google.com/maps/place/" + str(Place)

    geolocator = Nominatim(user_agent="myGeocoder")

    location = geolocator.geocode(Place , addressdetails= True)

    target_latlon = location.latitude , location.longitude

    web.open(url=Url_Place)

    location = location.raw['address']

    target = {'city' : location.get('city',''),
                'state' : location.get('state',''),
                'country' : location.get('country','')}

    current_loca = geocoder.ip('me')

    current_latlon = current_loca.latlng

    distance = str(great_circle(current_latlon,target_latlon))
    distance = str(distance.split(' ',1)[0])
    distance = round(float(distance),2)


    Speak(target)
    Speak(f"Sir , {Place} iS {distance} Kilometre Away From Your Location . ")

def Notepad():

    Speak("Tell Me The Query .")
    Speak("I Am Ready To Write .")
    writes = TakeCommand()
    time = datetime.now().strftime("%H:%M")
    filename = str(time).replace(":","-") + "-note.txt"
    with open(filename,"w") as file:
        file.write(writes)
    path_1 = "" + str(filename)
    path_2 = "DataBase\\NotePad\\" + str(filename)
    os.rename(path_1,path_2)
    os.startfile(path_2)

def TimeTable():
    Speak("Checking....")
    from DataBase.TimeTable.TimeTable import Time
    value = Time()
    Noti = Notify()
    Noti.title = "TimeTable"
    Noti.message = str(value)
    Noti.send()
    Speak("AnyThing Else Sir ??")

def WhatsappMsg(name,message):
     
    startfile("C:\\Users\\happy\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk")
    sleep(10)
    click(x=225, y=151)
    sleep(1)
    write(name)
    sleep(1)
    click(x=267, y=237)
    sleep(1)
    click(x=706, y=968)
    sleep(1)
    write(message)
    press('enter')

def WhatsappCall(name):
    startfile("C:\\Users\\happy\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk")
    sleep(5)
    click(x=188, y=133)
    sleep(2)
    write(name)
    sleep(2)
    click(x=276, y=288)
    sleep(2)
    click(x=1210, y=95)

def WhatsappvideoCall(name):
    startfile("C:\\Users\\happy\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk")
    sleep(5)
    click(x=188, y=133)
    sleep(2)
    write(name)
    sleep(2)
    click(x=276, y=288)
    sleep(2)
    click(x=1140, y=94)

def WhatsappChat(name):
    startfile("C:\\Users\\happy\\OneDrive\\Desktop\\WhatsApp - Shortcut.lnk")
    sleep(5)
    click(x=225, y=151)
    sleep(2)
    write(name)
    sleep(2)
    click(x=267, y=237)
    sleep(2)
    click(x=714, y=963)
    sleep(1)
    
def YouTubeAuto(command):
    
    #Speak("Which command want to use on Youtube")
    query = command
    if 'stop video' in query or 'top video' in query:
        press('space bar')
        Speak("done sir")

    elif 'resume video' in query:
        press('space bar')
        Speak("done sir")

    elif 'full screen' in query:
        press('f')
        Speak("done sir")

    elif 'film screen' in query:
        press('t')
        Speak("done sir")

    elif 'forward video' in query:
        press('l')
        Speak("done sir")

    elif 'backward video' in query:
        press('j')
        Speak("done sir")

    elif 'increase speed' in query:
        press_and_release('SHIFT + .')
        Speak("done sir")

    #elif 'decrease speed' in query:
       # press_and_release('SHIFT + ,')
        #Speak("done sir")

    elif 'play previous video' in query:
        press_and_release('SHIFT + p')
        Speak("done sir")

    elif 'play next video' in query:
        press_and_release('SHIFT + n')
        Speak("done sir")

    elif 'search on youtube' in query:
        click(x=627, y=128)
        Speak("What To Search Sir ?")
        search = TakeCommand().lower()
        write(search)
        sleep(0.8)
        press('enter')
        Speak("done sir")

    elif 'mute' in query:
        press('m')
        Speak("done sir")

    elif 'unmute' in query:
        press('m')
        Speak("done sir")
    
    else:
        Speak("No Command Found!")

def WindiowsAuto(command):

    #Speak("Which command want to use on Windows")
    query = command
    query=query.replace("jarvis ", "")

    if 'home screen' in query:
        press_and_release('windows + m')
        Speak("Done sir")

    elif 'minimize' in query or 'minimise' in query:
        press_and_release('windows + m')
        Speak("Done sir")

    elif 'show start' in query or 'so start' in query:
        press('windows')
        Speak("Done sir")

    elif 'open setting' in query:
        press_and_release('windows + i')
        Speak("Done sir")

    elif 'open search' in query:
        press_and_release('windows + s')
        Speak("Done sir")

    #elif 'take screenshot' in query:
       # press_and_release('PrtSc')
       # Speak("Done sir")

   # elif 'restore windows' in  query:
      #  press_and_release('Windows + Shift + M')
      #  Speak("Done sir")

    else:
        Speak("Sorry , No Command Found!")

def MicrosoftedgeAuto(name):
    
    #Speak("Which Command want to use on Chrome")
    #query=TakeCommand().lower()
    query=name

    if 'new tab' in query:
        press_and_release('ctrl + t')
        Speak("done sir")

    elif 'close tab' in query:
        press_and_release('ctrl + w')
        Speak("done sir")

    elif 'new window' in query:
        press_and_release('ctrl + n')
        Speak("done sir")

    elif 'open history' in query:
        press_and_release('ctrl + h')
        Speak("done sir")

    elif 'open download' in query:
        press_and_release('ctrl + j')
        Speak("done sir")

    elif 'bookmark' in query:
        press_and_release('ctrl + d')
        press('enter')
        Speak("done sir")

    #elif 'incognito' in query:
       # press_and_release('Ctrl + Shift + n')
        #Speak("done sir")

    #elif 'switch tab' in query:
        #Speak("tell me tab number")
        #query=TakeCommand().lower()
        #num = int(query)
        #bb = f'ctrl + {num}'
        #press_and_release(bb)
        #Speak("done sir")

    elif 'open' in query:
        Speak("what want to open")
        name=TakeCommand().lower()
        NameA = str(name)
        NameA=NameA.replace("open in browser", "")
        NameA=NameA.replace("Jarvis", "")

        if 'youtube' in NameA:
            web.open("https://www.youtube.com/")

        elif 'instagram' in NameA:
            web.open("https://www.instagram.com/")

        else:
            string = "https://www." + NameA + ".com"
            string_2 = string.replace(" ","")
            web.open(string_2)
    else:
        Speak("Sorry , No Command Found!")
