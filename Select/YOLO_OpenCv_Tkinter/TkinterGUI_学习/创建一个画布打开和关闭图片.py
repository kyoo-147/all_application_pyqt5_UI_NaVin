from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk

"""创建窗口"""
window = Tk()
window.title("Picture")
window.geometry("900x800")


"""创建一个canvas用于显示图片"""
canvas1 = Canvas(window, height=400, width=400, bg="white")
canvas1.grid(column=0, row=1)


"""创建一个按钮用于获取图片文件并打开"""
def OpenImage():
    global photo
    file = filedialog.askopenfilename()
    img = Image.open(file)
    photo = ImageTk.PhotoImage(img)
    canvas1.create_image(0, 0, image=photo)

btn1 = Button(window, text="OpenImage", command=OpenImage)
btn1.grid(column=0, row=2)

"""创建一个按钮用于关闭图片"""

def clearall():
    canvas1.delete(ALL)

btn2 = Button(window, text="cleasimage", command=clearall)
btn2.grid(column=0, row=3)

window.mainloop()



