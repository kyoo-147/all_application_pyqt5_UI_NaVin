import ctypes
from math import ceil
import socket
import cv2
import os, time, json, datetime
from triggers import Trigger
from image_manager import ImageManager
from PyQt5.QtCore import QThread, pyqtSignal

class ServerConnection(QThread):
    CHECK_CONNECTION_MSG_SEND = 'connected?'
    CHECK_CONNECTION_MSG_RECEIVED = 'connected'
    MSG_REQUEST_VIDEO = 'send-video'
    SEC_UNTIL_TIMEOUT_CONNECTION = 8
    FRAGMENT_SIZE = 1000
    IMAGE_PORT = 4444
    NOTIFICATION_PORT = 4445
    onClientUpdate = pyqtSignal(bool)

    def __init__(self, onClientUpdate):
        super(ServerConnection, self).__init__()
        self.serverIP = '0.0.0.0'
        self.onClientUpdate.connect(onClientUpdate)
        self.triggerQueue: list[Trigger] = []
        self.bSendVideo = False
        self.ImageSocket = None
        self.notifConn = None
        self.imageConn = None
        self.aspectRatio = 1080.0 / 1920.0
        self.newImgSize = 500

    def run(self):
        self.ImageSocket = self.createTCPSocket((self.serverIP, self.IMAGE_PORT))
        self.NotificationSocket = self.createTCPSocket((self.serverIP, self.NOTIFICATION_PORT))
        self.NotificationSocket.listen(1)
        print("LISTENING AT:", (self.serverIP, self.NOTIFICATION_PORT))

        while True:
            print('[Notifications] Waiting connection')
            self.onClientUpdate.emit(False)
            self.notifConn, address = self.NotificationSocket.accept()
            print('[Notifications] GOT CONNECTION FROM:', address)
            self.queryTriggerEvents()

            try:
                self.notifConn.settimeout(self.SEC_UNTIL_TIMEOUT_CONNECTION)
                self.notifConn.send(bytes(self.CHECK_CONNECTION_MSG_SEND, encoding='utf-8'))
                msg = self.notifConn.recv(1024).decode('utf-8')
            except:
                self.stopSendingVideo()
                self.notifConn.close()
                continue
            
            print('msg =', msg)
            if (msg.startswith(self.CHECK_CONNECTION_MSG_RECEIVED)
                or msg.startswith(self.MSG_REQUEST_VIDEO)):
                self.onClientUpdate.emit(True)
                self.checkConnection()
            else:
                self.stopSendingVideo()
                continue

    def checkConnection(self):
        while True:
            try:
                self.notifConn.send(bytes(self.CHECK_CONNECTION_MSG_SEND, encoding='utf-8'))
                msg = self.notifConn.recv(1024).decode('utf-8')
            except Exception as e:
                print(e)
                self.stopSendingVideo()
                break
        
            print('msg>', msg)

            if msg.startswith(self.MSG_REQUEST_VIDEO):
                if not self.bSendVideo:
                    self.startSendingVideo()
            elif not msg.startswith(self.CHECK_CONNECTION_MSG_RECEIVED):
                self.stopSendingVideo()
                break

            time.sleep(3)

    def startSendingVideo(self):
        self.ImageSocket.listen(1)
        print('[Image] Waiting connection')
        self.imageConn, address = self.ImageSocket.accept()
        print('[Image] GOT CONNECTION FROM:', address)

        self.bSendVideo = True
        ImageManager.onUpdateFrame.append(self.sendFrame)

    def stopSendingVideo(self):
        self.bSendVideo = False
        try:
            ImageManager.onUpdateFrame.remove(self.sendFrame)
        except:
            print('exception while removing self.sendFrame')

    def sendFrame(self, frame):
        frame = cv2.resize(frame, (self.newImgSize, int(self.newImgSize * self.aspectRatio)))
        ret, frame = cv2.imencode('.jpg', frame)
        
        if not ret:
            print('Encoding failed')
            return

        frameSize = len(frame)
        numPackets = ceil(frameSize / self.FRAGMENT_SIZE)

        # MESSAGE FORMAT: [----: 4 bytes][framesize: 4 bytes][imageFragment: (FRAGMENT_SIZE) bytes]
        data = (b'----'
                + bytes(ctypes.c_uint32(frameSize))
                + bytes(frame[:self.FRAGMENT_SIZE]))

        try:
            self.imageConn.send(data)

            packetID = 1
            while(packetID < numPackets):
                fragIni = packetID * self.FRAGMENT_SIZE
                data = bytes(frame[fragIni:fragIni + self.FRAGMENT_SIZE])
                self.imageConn.send(data)
                packetID += 1
        except Exception as e:
            print('couldn\'t send frame:')
            print(e)
            self.stopSendingVideo()
            return

    def createTCPSocket(self, address) -> socket.socket:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)
            
        try:
            sock.bind(address)
        except socket.error as message:
            print('Bind failed. Msg: ' + message)
            os._exit(1)

        # sock.listen(2)

        return sock

    def sendNotification(self, trigger: Trigger):
        print('sending notification')
        try:
            alarmInfo = {
                'local': trigger.name,
                'dateTime': time.mktime(datetime.datetime.now().timetuple()),
            }
            
            if self.notifConn is not None:
                data = b'trigger-notification' + bytes(json.dumps(alarmInfo), encoding='utf-8')
                self.notifConn.send(data)
                return True
            else:
                print('notifConn is None')
                return False
        except Exception as e:
            print('[exception while sending notification]')
            print(e)

    def sendAlarm(self, trigger: Trigger):
        try:
            alarmInfo = {
                'local': trigger.name,
                'dateTime': time.mktime(datetime.datetime.now().timetuple()),
            }
            
            if self.notifConn is not None:
                data = b'trigger-alarm' + bytes(json.dumps(alarmInfo), encoding='utf-8')
                self.notifConn.send(data)
                return True
            else:
                print('notifConn is None')
                return False
        except Exception as e:
            print('exception while sending alarm:')
            print(e)

    def queryTriggerEvents(self):
        for trigger in self.triggerQueue:
            self.fireTrigger(trigger)

    def fireTrigger(self, trigger: Trigger):
        isSent = True
        try:
            self.triggerQueue.remove(trigger)
        except:
            pass

        if trigger.action == 'Alarm':
            isSent = self.sendAlarm(trigger)
        elif trigger.action == 'Notification':
            isSent = self.sendNotification(trigger)

        if not isSent:
            self.triggerQueue.append(trigger)

