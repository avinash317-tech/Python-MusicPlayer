import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
print(root.get_themes())                 # Returns a list of all themes that can be set
root.set_theme("vista")         # Sets an available theme

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
#
# Styles - normal, bold, roman, italic, underline, and overstrike.

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Select Music",)
subMenu.add_command(label="Exit")


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us")

mixer.init()  # initializing the mixer

root.title("Melody")
root.iconbitmap(r'images/melody.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add")
addBtn.pack(side=LEFT)



delBtn = ttk.Button(leftframe, text="- Del")
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack(fill=X,expand=YES)

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text='--:--', relief=GROOVE,font=('corbel',60))
currenttimelabel.pack(fill=X,expand=YES,anchor=CENTER)

progressbar=ttk.Progressbar(topframe,value=0)
progressbar.pack(fill=X,expand=YES)




middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

labelFrame = LabelFrame(middleframe,bd=5)
labelFrame.pack(fill=X,expand=YES,anchor=W,side=BOTTOM)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(labelFrame, image=playPhoto)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(labelFrame, image=stopPhoto)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(labelFrame, image=pausePhoto)
pauseBtn.grid(row=0, column=2, padx=10)

previousPhoto = PhotoImage(file='images/previous.png')
previousBtn = ttk.Button(labelFrame, image=previousPhoto)
previousBtn.grid(row=0, column=3, padx=10)

backwordPhoto = PhotoImage(file='images/backword.png')
backwordBtn = ttk.Button(labelFrame, image=backwordPhoto)
backwordBtn.grid(row=0, column=4, padx=10)

forwardPhoto = PhotoImage(file='images/forward.png')
forwardBtn = ttk.Button(labelFrame, image=forwardPhoto)
forwardBtn.grid(row=0, column=5, padx=10)

nextPhoto = PhotoImage(file='images/nextSong.png')
nextBtn = ttk.Button(labelFrame, image=nextPhoto)
nextBtn.grid(row=0, column=6, padx=10)


mutePhoto = PhotoImage(file='images/mute.png').subsample(1,1)
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(labelFrame, image=volumePhoto)
volumeBtn.grid(row=0, column=7)

scale = ttk.Scale(labelFrame, from_=0, to=100, orient=HORIZONTAL)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=8, pady=15, padx=30)


root.mainloop()
