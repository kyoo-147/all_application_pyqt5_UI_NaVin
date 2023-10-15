import os
import time
import cv2
from queue import Queue
from PyQt5.QtCore import QThread
from helpers.blob_size_tester import BlobSizeTester as dt

class ImageManager:
    onUpdateFrame = []
    onVideoEnd = []
    FPS = 8
    frameResolution = (300, 300)

    def __init__(self, maxBufferSize):
        self.isVideo = True
        if self.isVideo:
            self.cap = cv2.VideoCapture('./recordings/Burglars Break Into Home.mp4')
            self.playRange = (0, 23000) # Video start-end in ms
            self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
        else:
            self.cap = cv2.VideoCapture(0)
        self.isVideoPaused = False
        self.bVideoEnded = False
        self.imageBuffer = Queue(maxsize=maxBufferSize)
        ret, self.lastFrameRead = self.cap.read()
        if not ret:
            raise Exception('Reading image failed')
        ImageManager.frameResolution = self.lastFrameRead.shape[:2]
        self.frametime = 1 / ImageManager.FPS
        self.showPersonTester = False
        self.personTesterSize = 2
        dt.addTesterToList((.5, .5))

        self.readFrameThread = QThread()
        self.readFrameThread.run = self.readFrame
        self.readFrameThread.start()

        self.feedFrameThread = QThread()
        self.feedFrameThread.run = self.feedFrame
        self.feedFrameThread.start()

    def readFrame(self) -> None:
        """
        1. Read images from cameras
        2. Put in the buffer
        """
        while True:
            if self.imageBuffer.full():
                time.sleep(0.05)
                continue

            ret, frame = self.cap.read()
            
            if self.isVideo and (not ret or self.cap.get(cv2.CAP_PROP_POS_MSEC) > self.playRange[1]):
                self.bVideoEnded = True
                self.cap.set(cv2.CAP_PROP_POS_MSEC, self.playRange[0])
                time.sleep(0.1)
                continue
                
            self.imageBuffer.put(frame)

    def feedFrame(self) -> None:
        '''
        Deliver frames to subscribed functions
        '''

        while True:
            initTime = time.time()

            if self.showPersonTester:
                self.lastFrameRead = dt.drawPeople(self.lastFrameRead, self.personTesterSize)

            for function in self.onUpdateFrame:
                function(self.lastFrameRead)

            if self.isVideoPaused:
                time.sleep(0.2)
                continue
                    
            self.lastFrameRead = self.imageBuffer.get()

            while self.lastFrameRead is None:
                time.sleep(0.05)
                self.lastFrameRead = self.imageBuffer.get()

                if self.bVideoEnded:
                    for function in self.onVideoEnd:
                        function()
            
            elapsedTime = time.time() - initTime
            sleepTime = self.frametime - elapsedTime
            if sleepTime > 0.005:
                time.sleep(sleepTime - 0.002)

    def setShowPersonTester(self, value):
        self.showPersonTester = value

    def setPersonTesterSize(self, value):
        self.personTesterSize = value

    def togglePauseVideo(self):
        self.isVideoPaused = not self.isVideoPaused