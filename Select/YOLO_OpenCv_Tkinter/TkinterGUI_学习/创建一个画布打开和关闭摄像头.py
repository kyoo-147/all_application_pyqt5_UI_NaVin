import cv2 as cv
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

cap = cv.VideoCapture(0)  # 选择摄像头

"""创建一个窗口"""
window = tk.Tk()      #
window.title("显示摄像头")
window.geometry("1500x1000")

"""创建一个画布"""
canvas=Canvas(window, bg='white', width=1280, height=720)
canvas.grid(column=0, row=0)

a = True

"""创建一个按钮用于打开摄像头"""
def openvideo():
    while a:
        global photo,frame,img1, img2

        _, frame=cap.read()
        img1 = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        img2 = Image.fromarray(img1)
        photo = ImageTk.PhotoImage(img2)
        canvas.create_image(0, 0, anchor=NW, image=photo)
        window.update_idletasks()
        window.update()
    cap.release()
    cv.destroyAllWindows()
btn1 = Button(window, text="打开摄像头", command=openvideo)
btn1.grid(column=0,row=1)

"""船舰一个按钮用于关闭摄像头"""
def clearall():
    global a
    a = False
    cap.release()
    cv.destroyAllWindows()
    canvas.delete(ALL)

btn2 = Button(window, text="cleasimage", command=clearall)
btn2.grid(column=0, row=3)

window.mainloop()
cap.release()
cv.destroyAllWindows()