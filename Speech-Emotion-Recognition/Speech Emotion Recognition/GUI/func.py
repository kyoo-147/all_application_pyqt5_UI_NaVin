import threading
import librosa
import numpy as np
import pyaudio
import wave
import speech_recognition as sr
from pygame import mixer
from keras.models import load_model



from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal,QResource

class Clock(QObject):

    def __init__(self):
        QObject.__init__(self)
    recieveTime = pyqtSignal(str, arguments=['_predict'])
    emotions_used = ('Anger', 'Excited', 'Frustration', 'Happiness', 'Neutral', 'Sadness')
    globalpath=''

    saved_model = load_model('my_model.h5')
    @pyqtSlot()
    def predict(self):
        if self.globalpath!="":
            start_thread = threading.Thread(target=self._predict)
            start_thread.daemon = True
            start_thread.start()
            #print('thread_has started4')
    def _predict(self):
        music= self.globalpath
        sound, s = librosa.load(music, sr=16000, duration=8.0)  # Downsample 44.1kHz to 16kHz
        sound = librosa.util.pad_center(sound, 128000, mode='symmetric')  # change type 'constant'
        ps = librosa.feature.melspectrogram(y=sound, sr=16000, n_fft=2048, hop_length=512)
        ps_db = librosa.power_to_db(ps ** 2, ref=np.median)  # np and mean not max
        ps_db = np.expand_dims(ps_db, axis=0)
        ps_db = np.expand_dims(ps_db, axis=3)

        # saved_model = load_model('resources/my_model.h5')
        prediction = self.saved_model.predict(ps_db)

        self.recieveTime.emit(self.emotions_used[prediction.argmax(axis=1)[0]])

    @pyqtSlot()
    def record(self):
        start_thread = threading.Thread(target=self._record)
        start_thread.daemon = True
        start_thread.start()
       # print('thread_has started3')
    def _record(self):
        mixer.init()
        mixer.music.load('chime1.mp3')
        mixer.music.play()

        r = sr.Recognizer()
        r.pause_threshold = 0.7
        r.energy_threshold = 400
        with sr.Microphone() as source:
            audio=r.record(source, duration = 10)
               # audio = r.listen(source, timeout=5)
        mixer.music.load('chime2.mp3')
        mixer.music.play()



        with open("microphone-results.wav", "wb") as f:
            self.globalpath="microphone-results.wav"
            f.write(audio.get_wav_data())

    @pyqtSlot()
    def play(self):
        if self.globalpath!='':
            start_thread = threading.Thread(target=self._play)
            start_thread.daemon = True
            start_thread.start()
           # print('thread_has started2')

    def _play(self):
        chunk = 1024
        fname=self.globalpath
        # open a wav format music
        f = wave.open(fname, "rb")
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        # read data
        data = f.readframes(chunk)

        # play stream
        while data:
            stream.write(data)
            data = f.readframes(chunk)

            # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()

    @pyqtSlot(str)
    def start_clock(self,*pathes):
        start_thread = threading.Thread(target=self._start_clock,args=pathes)
        start_thread.daemon = True
        start_thread.start()
      #  print('thread_has started')

    def _start_clock(self,*pat):

            pat = str(pat[0]).replace('file:///','')
            #print(pat)

            pat=str(pat).split(',')
           # print(pat)
            music=pat[0]

            self.globalpath =pat[0]





