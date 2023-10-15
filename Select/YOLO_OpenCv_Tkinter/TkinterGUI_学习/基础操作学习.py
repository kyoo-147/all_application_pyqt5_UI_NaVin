from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import os


window = Tk() # 创建一个窗口对象
window.title(" First window")   # 命名窗口左上角
window.geometry("900x800")    # 设置窗口大小


"""设置标签"""
lbl1 = Label(window, text="hello", font=("Arial Bold", 50)) # 添加添加一个标签组件, text为显示内容，font设置格式
lbl1.grid(column=0, row=0)     # 调用函数显示位置

# 设置按钮
# btn = Button(window, text="Click Me", fg="red") # 在窗口中加一个按钮，text按钮名,fg颜色
# btn.grid(column=1, row=0)   # 调用函数显示按钮


"""设置按钮点击事件"""
def clicked():
    lbl2 = Label(window, text="Button was clicked") # 添加添加一个标签组件, text为显示内容，font设置格式
    lbl2.grid(column=0, row=2) 
    #lbl.configure(text="Button was clicked")

btn = Button(window, text="Click me1", command=clicked)  # 设置按钮的属性，与对应的函数方法
btn.grid(column=0, row=1)

"""添加一个文本框"""
txt1 = Entry(window, width=10) # 添加一个输入文本框
txt1.grid(column=0, row=3)     # 设置文本框显示位置
# txt1.focus()       # 设置输入焦点，打开程序自动聚焦到文本输入框

"""再添加一个按钮，点击按钮在屏幕上显示文本框的内容"""
def clicked2():
    res = txt1.get()
    lbl3 = Label(window, text=res)
    lbl3.grid(column=0, row=5)
btn2 = Button(window, text="Click Me2", command=clicked2)
btn2.grid(column=0, row=4)


"""添加一个组合框"""
combo = Combobox(window) # 添加复选框到窗口中
combo['values'] = (1, 2, 3, 4, 5, "Text") # 设置可选择的内容
combo.current(1)   # 一次选择一个
combo.grid(column=0, row=6)  # 设置显示位置

"""添加一个复选框"""
chk_state = BooleanVar()  # 设置一个框 
chk_state.set(True)   # 设置框内默认初始状态
chk = Checkbutton(window, text="Choose", var=chk_state) # 设置框后面的显示文字， 显示框
chk.grid(column=0, row=7)  # 显示复选框，设置位置

"""添加单选框"""
def clicked3():
    lbl4 = Label(window, text='第二个')
    lbl4.grid(column=4, row=8)

rad1 = Radiobutton(window, text="First", value=1)  # 单选框也可以指定一个函数，点击出现效果
rad2 = Radiobutton(window, text='Second', value=2, command=clicked3)
rad3 = Radiobutton(window, text='Third', value=3)
rad1.grid(column=0, row=8)
rad2.grid(column=1, row=8)
rad3.grid(column=2, row=8)


"""获取单选框的值"""
def clicked4():
    lbl4 = Label(window, text=selected.get())
    lbl4.grid(column=0, row=10)
selected = StringVar()   # 有IntVar()和StringVar(),文本内容使用Str
rad4 = Radiobutton(window, text="four", value='wu', variable=selected)  # 单选框也可以指定一个函数，点击出现效果
rad5 = Radiobutton(window, text='five', value=5, variable=selected)
rad6 = Radiobutton(window, text='six', value=6, variable=selected)
btn3 = Button(window, text="click me", command=clicked4)
rad4.grid(column=0, row=9)
rad5.grid(column=1, row=9)
rad6.grid(column=2, row=9)
btn3.grid(column=3, row=9)

"""添加文本区"""
txt1 = scrolledtext.ScrolledText(window, width=40, height=10) # 指定高宽，不然会占满画面
txt1.insert(INSERT, "Text goes here")   # 添加文本框初始显示内容
txt1.grid(column=0, row=12)

"""创建消息框"""
def clicked5():
    messagebox.showinfo("message title", "Message content")  # 设置消息框名称和显示内容
btn4 = Button(window, text="消息框clicked", command=clicked5)
btn4.grid(column=0, row=14)

"""添加Spinbox"""
spin = Spinbox(window, from_=0, to=100, width=15)   # Spinbox是输入控件，与Entry类似，但可以指定输入范围
spin.grid(column=0, row=15)   # 不仅可以指定范围，也可以指定特定的值

"""添加进度条"""
bar = Progressbar(window, length=400)
bar['value'] = 30  # 设置进度条的进度值
bar.grid(column=0, row=16)

"""添加一个打开文件对话框的按钮"""
def clicked6():
    file = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__)) 
    # 当你选择一个文件并点击打开，file变量将会保存该文件的路径
btn5 = Button(window, text="Open file", command=clicked6)
btn5.grid(column=0, row=18)

"""显示图片"""
b1 = Canvas(window)
pic = PhotoImage(file='C:/deeplearn/Projiect/OpenCV/1.png')
b1.create_image(160, 160, image=pic)



# 显示窗口
window.mainloop()     # 调用函数，显示窗口