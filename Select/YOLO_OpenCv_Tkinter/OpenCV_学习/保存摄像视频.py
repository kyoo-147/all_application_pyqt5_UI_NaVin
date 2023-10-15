import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
# 定义编译器并创建VideoWriter对象
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output1.avi', fourcc, 20.0, (640, 480))
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can`t receive frame (stream end?) .Exiting...")
        break


    out.write(frame)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# 完成工作后释放所有内容
cap.release()
out.release()
cv.destroyAllWindows()