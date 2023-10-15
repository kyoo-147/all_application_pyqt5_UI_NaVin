"""
Triggers
========

1. Define class Trigger
2. Manage triggers list
3. Update triggers periodically
"""

import numpy as np
import time
import sip
import math
import os
from playsound import playsound
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QCheckBox
import database as db
import layout

class Trigger:
    checkboxSilenceAlarms: QCheckBox = None
    soundThread = None
    triggersWindow = None
    keepPlayingSound = False
    isAlarmSilenced = False
    MAX_SOUNDING_TIME = 10

    def __init__(
            self,
            id,
            name,
            initialTime,
            finalTime,
            maxStayTime,
            action,
            areaStartX,
            areaStartY,
            areaEndX,
            areaEndY):
        self.id = id
        self.name = name
        self.initialTime = initialTime
        self.finalTime = finalTime
        self.maxStayTime = maxStayTime
        self.action = action
        self.areaStartX = areaStartX
        self.areaStartY = areaStartY
        self.areaEndX = areaEndX
        self.areaEndY = areaEndY
        self.stayedTime = .0
        self.fired = False
        self.detectionLastTime = -math.inf
        self.timeSinceLastUpdate = time.time()
        self.incrementLastTime = -math.inf
        self.bDetectionInside = False
        self.widget = None
        self.lStayedTime = None
        self.camera = 0

    def remove(self):
        db.deleteTrigger(self.id)
        self.triggersWindow.vBoxTriggers.removeWidget(self.widget)
        triggersList.remove(self)
        sip.delete(self.widget)
        self.widget = None

    def reset(self):
        self.stayedTime = 0.
        self.timeSinceLastUpdate = 0.
        self.fired = False
        Trigger.keepPlayingSound = False

        if self.widget is not None:
            self.triggersWindow.resetTriggerUI.emit(self)

        if self.lStayedTime is not None:
            self.lStayedTime.setText(str(round(self.stayedTime, 3)))

    def print(self):
        print('TRIGGER:',
                self.id,
                self.name,
                self.initialTime,
                self.finalTime,
                self.maxStayTime,
                self.action,
                self.areaStartX,
                self.areaStartY,
                self.areaEndX,
                self.areaEndY)

    def startAlarmSound():
        Trigger.soundThread = QThread()
        Trigger.soundThread.run = Trigger.playAlarmSound
        Trigger.soundThread.start()

    def playAlarmSound():
        Trigger.keepPlayingSound = True
        initTime = time.time()

        while Trigger.keepPlayingSound:
            playsound('./sounds/mixkit-warning-alarm-buzzer.wav')
            time.sleep(0.5)
            if time.time() - initTime > Trigger.MAX_SOUNDING_TIME:
                print('alarm stopped')
                break

        Trigger.keepPlayingSound = False

class UpdateTriggersPeriodicallyThread(QThread):
    '''Update triggers every THREAD_TIME_SLEEP seconds'''
    changeTriggerStateSignal = pyqtSignal(Trigger, bool) # Changes in UI must happen in main thread
    isPlayingSound = False

    def run(self):
        THREAD_TIME_SLEEP = 0.1 # Time (in seconds) in which the thread will sleep and increase stayed times
        MAX_TIME_INC_LAST_DETECTION = 1.0 # Keep increasing stayed time until x seconds without detection
        TIME_LIMIT_TO_RESET = 10 # Time without detections until trigger reset

        while True:
            for trigger in triggersList:
                timeSinceLastDetection = time.time() - trigger.detectionLastTime
                timeSinceLastIncrement = time.time() - trigger.incrementLastTime
                trigger.incrementLastTime = time.time()

                if timeSinceLastDetection > MAX_TIME_INC_LAST_DETECTION:
                    if not trigger.bDetectionInside:
                        if timeSinceLastDetection > TIME_LIMIT_TO_RESET:
                            trigger.reset()

                    continue

                trigger.stayedTime += timeSinceLastIncrement

                if trigger.lStayedTime is not None:
                    trigger.lStayedTime.setText(str(round(trigger.stayedTime, 3)))
                
                if trigger.fired: continue

                if trigger.stayedTime > trigger.maxStayTime and not trigger.fired:
                    trigger.fired = True
                    print(f'TRIGGER [{trigger.name}] FIRED')

                    if not Trigger.checkboxSilenceAlarms.isChecked():
                        Trigger.startAlarmSound()

                    self.changeTriggerStateSignal.emit(trigger, True)

            time.sleep(THREAD_TIME_SLEEP)

def updateTriggersAfterDetection(detections):
    anyDetection = False
    for i in np.arange(0, detections.shape[2]):
        idx = int(detections[0, 0, i, 1])
        if idx != 15: continue # Se não for pessoa, vai para a próxima detecção
        anyDetection = True

        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            boundingBox = detections[0, 0, i, 3:7]

            timeNow = datetime.now()
            
            global triggersList
            for trigger in triggersList:
                if testHorario(trigger, timeNow) and testBoundingBox(trigger, *boundingBox):
                    trigger.stayedTimeBeforeDetection = trigger.stayedTime
                    trigger.detectionLastTime = time.time()
                    trigger.bDetectionInside = True
                else:
                    trigger.bDetectionInside = False
    if not anyDetection:
        for trigger in triggersList:
            trigger.bDetectionInside = False

triggersList: list[Trigger] = []

def initTriggers(updateTriggerState):
    global triggersList
    triggersList.clear()

    for triggerRow in db.selectTriggers():
        trigger = Trigger(*triggerRow)
        triggersList.append(trigger)

    thread = UpdateTriggersPeriodicallyThread()
    thread.changeTriggerStateSignal.connect(updateTriggerState)
    thread.start()

    return thread

def createTrigger(*args):
    trigger = Trigger(-1, *args)
    db.createTrigger(trigger)
    layout.addTriggerOnViewList(Trigger.triggersWindow, trigger)
    triggersList.append(trigger)

def testHorario(trigger: Trigger, timeNow: datetime) -> bool:
    '''Check if current time is between trigger's active time'''

    iniHour = int(trigger.initialTime[:2])
    iniMinute = int(trigger.initialTime[3:])
    finalHour = int(trigger.finalTime[:2])
    finalMinute = int(trigger.finalTime[3:])

    if iniHour < timeNow.hour and finalHour > timeNow.hour:
        return True
    if iniHour == timeNow.hour:
        return iniMinute <= timeNow.minute
    if finalHour == timeNow.hour:
        return finalMinute >= timeNow.minute

    return False

def testBoundingBox(trigger: Trigger, boxStartX: float, boxStartY: float, boxEndX: float, boxEndY: float) -> bool:
    '''Test if detection is inside trigger'''
    xThreshold = 0.01041
    yThreshold = 0.0185

    return (boxStartX >= trigger.areaStartX - xThreshold
            and boxEndX   <= trigger.areaEndX + xThreshold
            and boxStartY >= trigger.areaStartY - yThreshold
            and boxEndY   <= trigger.areaEndY + yThreshold)
