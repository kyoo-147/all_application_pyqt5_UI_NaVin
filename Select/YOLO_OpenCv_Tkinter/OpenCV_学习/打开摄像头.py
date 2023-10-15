import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    cv.imshow("Video", frame)

    if cv.waitKey(1) == ord('q'):
        break



cap.release()
cv.destroyAllWindows()