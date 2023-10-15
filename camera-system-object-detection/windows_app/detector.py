import os
import numpy as np
import time
import cv2
import math
from PyQt5.QtCore import QThread
from benchmark import Benchmark
import triggers

class SSDDetector(QThread):
    def __init__(self, onFrameProcessed):
        super(SSDDetector, self).__init__()
        self.onFrameProcessed = onFrameProcessed
        self.blobSizes = [400, 600]
        self.blobSizeRange = [10, 2000]
        self.frame = None
        self.bDetect = False
        self.detections = None
        self.resizeStartPoint = None
        self.resizeEndPoint = None
        self.onlyDetectCroppedFrame = True
        self.detectionColor = (0, 0, 200)
        self.confidenceDrawDetection = .5
        self.benchmark = Benchmark('Detector')
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
                        "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike",
                        "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

        rootFolder = __file__[:-len(os.path.basename(__file__))]
        PROTOTXT = rootFolder + "/neural_networks/MobileNetSSD_deploy.prototxt"
        MODEL = rootFolder + "/neural_networks/MobileNetSSD_deploy.caffemodel"
        GPU_SUPPORT = 0

        self.net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
        if GPU_SUPPORT:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def run(self):
        self.benchmark.restartExecutionTime()
        while(True):
            if self.bDetect:
                
                if self.frame is None:
                    self.bDetect = False
                    continue

                if len(triggers.triggersList) != 0:
                    if self.onlyDetectCroppedFrame:
                        croppedFrame = self.frame[
                            self.resizeStartPoint[0]:self.resizeEndPoint[0],
                            self.resizeStartPoint[1]:self.resizeEndPoint[1]
                        ]
                        
                        detections = self.detect(croppedFrame)
                        self.detections = self.convertCoordsCroppedToOriginal(detections)
                    else:
                        self.detections = self.detect(self.frame)

                    self.onFrameProcessed(self.detections)

                time.sleep(.01)
            else:
                if self.frame is not None:
                    self.updateDetectionArea()
                    self.bDetect = True
                time.sleep(0.5)

    def detect(self, frame):
        self.benchmark.startTimer()

        blobShape = (
            int(self.blobSizes[0]
                * self.aspectRatio
            ),
            int(self.blobSizes[0]
            ))
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, blobShape, 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        self.benchmark.stopTimer()

        return detections

    def setFrame(self, frame):
        self.frame = frame

    def setOnlyDetectCroppedFrame(self, value):
        if value:
            self.updateDetectionArea()
        else:
            self.aspectRatio = self.frame.shape[1] / self.frame.shape[0]
        self.onlyDetectCroppedFrame = value

    def convertCoordsCroppedToOriginal(self, detections):
        '''
        Convert bounding boxes' normalized coordinates from cropped frame to normal sized frame
        '''
        croppedFrameHeight, croppedFrameWidth = self.croppedFrameResolution
        frameHeight, frameWidth = self.frame.shape[:2]
        for i in np.arange(0, detections.shape[2]):
            idx = int(detections[0, 0, i, 1])
            if idx != 15: continue # idx 15 is person

            detections[0, 0, i, 3] = (detections[0, 0, i, 3] * croppedFrameWidth + self.resizeStartPoint[1]) / frameWidth
            detections[0, 0, i, 4] = (detections[0, 0, i, 4] * croppedFrameHeight + self.resizeStartPoint[0]) / frameHeight
            detections[0, 0, i, 5] = (detections[0, 0, i, 5] * croppedFrameWidth + self.resizeStartPoint[1]) / frameWidth
            detections[0, 0, i, 6] = (detections[0, 0, i, 6] * croppedFrameHeight + self.resizeStartPoint[0]) / frameHeight

            if detections[0, 0, i, 3] < 0:
                detections[0, 0, i, 3] = 0
            if detections[0, 0, i, 4] < 0:
                detections[0, 0, i, 4] = 0
            if detections[0, 0, i, 5] > 1:
                detections[0, 0, i, 5] = 1
            if detections[0, 0, i, 6] > 1:
                detections[0, 0, i, 6] = 1

        return detections
    
    def updateDetectionArea(self):
        '''
        Update detection area
        '''
        if len(triggers.triggersList) == 0: return

        startPoint = [math.inf, math.inf]
        endPoint = [-math.inf, -math.inf]

        for trigger in triggers.triggersList:
            if trigger.areaStartY < startPoint[0]:
                startPoint[0] = trigger.areaStartY
            if trigger.areaEndY > endPoint[0]:
                endPoint[0] = trigger.areaEndY
            if trigger.areaStartX < startPoint[1]:
                startPoint[1] = trigger.areaStartX
            if trigger.areaEndX > endPoint[1]:
                endPoint[1] = trigger.areaEndX
        
        frameHeight, frameWidth = self.frame.shape[:2]

        # Convert normalized (0 - 1) to pixels
        self.resizeStartPoint = (int(startPoint[0] * frameHeight), int(startPoint[1] * frameWidth))
        self.resizeEndPoint = (int(endPoint[0] * frameHeight), int(endPoint[1] * frameWidth))

        self.croppedFrameResolution = (
            self.resizeEndPoint[0] - self.resizeStartPoint[0],
            self.resizeEndPoint[1] - self.resizeStartPoint[1]
        )
        self.aspectRatio = self.croppedFrameResolution[1] / self.croppedFrameResolution[0]

    def setBlobSize(self, value, index):
        try:
            value = int(value)
        except ValueError:
            print('invalid blob size value')
            return

        if value < self.blobSizeRange[0] or value > self.blobSizeRange[1]:
            print('invalid blob size value')
            return

        self.blobSizes[index] = value

    def drawDetections(self, frame):
        if self.detections is None: return frame

        frame = np.array(frame, dtype=np.uint8)

        h, w = frame.shape[:2]
        for i in np.arange(0, self.detections.shape[2]):
            idx = int(self.detections[0, 0, i, 1])
            if idx != 15: continue # If not a person

            confidence = self.detections[0, 0, i, 2]
            if confidence > self.confidenceDrawDetection:
                box = self.detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startX, startY, endX, endY = box.astype("int")
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), self.detectionColor, 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.detectionColor, 2)
        
        return frame