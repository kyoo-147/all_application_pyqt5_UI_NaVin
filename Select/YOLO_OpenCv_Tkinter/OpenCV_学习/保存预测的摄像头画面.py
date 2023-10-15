import cv2 as cv
from ultralytics import YOLO
 
model = YOLO('yolov8n.pt')  # 选择预测的模型

cap = cv.VideoCapture(0)  # 选择要使用的摄像头

fourcc = cv.VideoWriter_fourcc(*'XVID')  # 设置输出视频的格式

out = cv.VideoWriter('predict_yolov8n_2.avi', fourcc, 20.0, (640, 480)) # 设置视频保存格式信息

while cap.isOpened():    # 当视像头打开时
    ret, frame = cap.read()   # 读取摄像头拍到的内容
    if not ret:
        print("Can`t receive frame (stream end?) Exiting...") # 读取不到摄像头，返回一个信息
        break # 读取不到摄像头打破循环
    results = model(frame)  # 对读取到的每个画面使用模型预测
    
    annotated_frame = results[0].plot()   # 将预测的框套在图像上

    out.write(annotated_frame)  # 将预测好带框的画面写入到输出文件中

    cv.imshow('frame', annotated_frame) # 显示摄像头预测画面

    if cv.waitKey(1) == ord('q'):   # 设置按q停止录制
        break

 
 # 录制结束后，释放占用的资源
cap.release()
out.release()
cv.destroyAllWindows()