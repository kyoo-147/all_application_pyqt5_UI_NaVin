import cv2
import numpy as np
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from image_manager import ImageManager

class DetectionTester:
    AREA_COLOR = (20, 0, 220)
    AREA_CONTOUR_COLOR = (80, 0, 80)
    
    def __init__(self, widget):
        self.startPoint = None
        self.endPoint = None
        self.widget = widget
        self.boxSize = (10, 16)
        self.areas = []

    def updateFakeDetection(self, frame):
        areas = np.zeros_like(frame, np.uint8)
        h, w = frame.shape[:2]
        # print('shape', h, w)

        mouseX, mouseY = self.getWidgetCoord()
        self.startPoint = (mouseX - self.boxSize[0], mouseY - self.boxSize[1])
        self.endPoint = (mouseX + self.boxSize[0], mouseY + self.boxSize[1])
        
        import triggers
        for trigger in triggers.triggersList:
            startPointMouse = (int(trigger.areaStartX * w), int(trigger.areaStartY * h))
            endPointMouse = (int(trigger.areaEndX * w), int(trigger.areaEndY * h))

            # print(startPoint, endPoint)
            if (self.startPoint[0] >= (trigger.areaStartX * w)) & (self.endPoint[0] <= (trigger.areaEndX * w)) & (self.startPoint[1] >= (trigger.areaStartY * h)) & (self.endPoint[1] <= (trigger.areaEndY * h)):
                areaColor = (0, 200, 0)
            else:
                areaColor = (200, 0, 0)
            cv2.rectangle(areas, startPointMouse, endPointMouse, areaColor, cv2.FILLED)
            # cv2.rectangle(areas, area[0], area[1], self.AREA_CONTOUR_COLOR, 2) # Contorno
            
        frame = cv2.rectangle(frame, self.startPoint, self.endPoint, areaColor, 2)

        mask = areas.astype(bool)
        alpha = 0.5
        frame[mask] = cv2.addWeighted(frame, alpha, areas, 1 - alpha, 0)[mask]

    def getWidgetCoord(self):
        globalCoords = QCursor.pos()
        coords = self.widget.mapFromGlobal(globalCoords)
        return (coords.x(), coords.y())