from tkinter import *
import time
import threading
root = Tk()
root.geometry('300x300')

def increase(x):
    while x<10:
        x+=1
        l1['text'] = str(x)
        time.sleep(1)
        #root.update_idletasks()


def decrease(x):
    while x>1:
        x-=1
        l2['text'] = str(x)
        time.sleep(1)
        #root.update_idletasks()

l1 =Label(root,text='1')
l1.pack(side=LEFT,padx=10)

l2  = Label(root,text='10')
l2.pack(side=LEFT,padx=20)

Button(root,text='Increase Label-1',command=lambda:increase(1)).pack()

Button(root,text='Decrease Label-2',command=lambda:decrease(10)).pack()

root.mainloop()