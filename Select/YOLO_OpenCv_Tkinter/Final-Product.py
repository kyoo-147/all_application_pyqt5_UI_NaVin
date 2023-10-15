import cv2 as cv
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from ultralytics import YOLO

cap = cv.VideoCapture(0)  # 选择摄像头
model = YOLO('yolov8n.pt')

"""创建一个窗口"""
window = tk.Tk()      #
window.title("显示摄像头")
window.geometry("1000x800")

"""创建一个画布"""
canvas=Canvas(window, bg='white', width=720, height=480)
canvas.grid(column=0, row=0)
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('pirdect_yolo_tkinter.avi', fourcc, 20.0, (640, 480))

a = True
b = False

"""创建一个按钮用于打开摄像头"""
def openvideo():
    global photo,frame,img1, img2, a, pir_frame
    a = True
    while a:
        _, frame=cap.read()
        results = model(frame)
        pir_frame = results[0].plot()
        img1 = cv.cvtColor(pir_frame, cv.COLOR_RGB2BGR)
        img2 = Image.fromarray(img1)
        photo = ImageTk.PhotoImage(img2)
        canvas.create_image(0, 0, anchor=NW, image=photo)
        window.update_idletasks()
        window.update()
        if b:
            out.write(pir_frame)

        
    cv.destroyAllWindows()
btn1 = Button(window, text="打开摄像头", command=openvideo)
btn1.grid(column=0,row=1)

"""创建一个按钮用于关闭摄像头"""
def clearall():
    global a
    a = False
    canvas.delete(ALL)

btn2 = Button(window, text="关闭摄像头", command=clearall)
btn2.grid(column=0, row=3)


"""创建一个按钮用于保存已经预测好的视频"""

def savevideos():
    global b
    b = True


btn3 = Button(window, text="保存视频", command=savevideos)
btn3.grid(column=0, row=4)

"""创建一个按钮关闭保存"""
def cleasesavevideos():
    global b
    b = False
    out.release()



btn4 = Button(window, text="关闭保存", command=cleasesavevideos)
btn4.grid(column=0, row=5)


window.mainloop()
out.release()
cap.release()
cv.destroyAllWindows()