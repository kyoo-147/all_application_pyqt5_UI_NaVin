import pywhatkit
import wikipedia
from pywikihow import RandomHowTo, search_wikihow
import os
import speech_recognition as sr
import webbrowser as web
import bs4
import pyttsx3
from time import sleep
import requests


engine =pyttsx3.init("sapi5")
voices =engine.getProperty("voices")
engine.setProperty("voices",voices[1].id)

def Speak(audio):
    
    print(f": {audio}")
    engine.say(audio)
    engine.runAndWait()
    print(" ")

def takecommand():
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

def YouTubeSearch(term):
    Speak("What want to you search ")
    term=takecommand()
    result = "https://www.youtube.com/results?search_query=" + term
    web.open(result)
    Speak("This Is What I Found For Your Search .")
    pywhatkit.playonyt(term)
    Speak("This May Also Help You Sir .")

def My_Location():
    op = "https://www.google.co.in/maps/place/LDRP+Institute+of+Technology+and+Research/@23.2393286,72.6365421,17z/data=!3m1!4b1!4m6!3m5!1s0x395c2b933477ba9f:0xe440409e66bea08a!8m2!3d23.2393286!4d72.6387308!16s%2Fm%2F07s50xh"
    Speak("Checking....")
    web.open(op)
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    state = geo_d['city']
    country = geo_d['country']
    Speak(f"Sir , You Are Now In {state , country} .")