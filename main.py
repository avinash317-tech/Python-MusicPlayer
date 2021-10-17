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


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Select Music", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music player build using Python Tkinter\n by Vikas Pathak @GisTech')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Melody")
root.iconbitmap(r'images/melody.ico')

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
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

total_length=0
def show_details(play_song):
    global  total_length
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()


    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


current_time=0
def start_count(t):
    import  math
    global paused
    global  start_from
    global  current_time
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = start_from
    pv=t/100
    progressbar['value'] = current_time/pv
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = '' + timeformat
            time.sleep(1)
            current_time += 1
            if current_time%math.ceil(pv)==0:
                v = progressbar['value']
                v += 1
                progressbar['value'] = v
                print(v)

    if current_time >=t:
        mixer.music.fadeout(2000)
        next_Song()




start_from=0
playIndex=-1
def play_music(*event):
    global paused
    global  start_from
    global t1
    global  playIndex

    if paused and playIndex == playlistbox.curselection()[0]:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:

            mixer.music.stop()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            playIndex= selected_song
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play(0,start_from)
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    global start_from
    mixer.music.stop()
    #mixer.music.fadeout(1000)
    statusbar['text'] = "Music Stopped"
    start_from=0
    progressbar['value'] = 0


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    global cur_vol
    if muted:  # Unmute the music
        mixer.music.set_volume(cur_vol*0.01)    #vol/100
        volumeBtn.configure(image=volumePhoto)
        scale.set(cur_vol)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        cur_vol=scale.get()
        scale.set(0)
        muted = TRUE


def next_Song():
    global  start_from
    start_from=0
    progressbar['value']=0
    s  = playlistbox.curselection()
    print(s)
    if len(s)!=0:
        print(s[0])
        if s[0] < playlistbox.size()-1:
            playlistbox.selection_clear(0,END)
            playlistbox.selection_set(s[0]+1)
        else:
            playlistbox.selection_clear(0, END)
            playlistbox.selection_set(0)
    else:
        tkinter.messagebox.showinfo('No Selection','No Song is Selected ..')
    global  paused
    paused=False
    play_music()


def prev_Song():
    global start_from
    start_from = 0
    progressbar['value']=0
    s  = playlistbox.curselection()
    print(s)
    if len(s)!=0:
        print(s[0])
        if s[0] > 0:
            playlistbox.selection_clear(0,END)
            playlistbox.selection_set(s[0]-1)
        else:
            playlistbox.selection_clear(0, END)
            playlistbox.selection_set(END)
    else:
        tkinter.messagebox.showinfo('No Selection','No Song is Selected ..')
    global  paused
    paused=False
    play_music()


def backword_song():
    global  start_from
    global  current_time
    start_from = current_time - 10
    if start_from < 0:
        start_from=0
    play_music()



def forward_Song():
    global start_from
    global total_length
    global current_time
    start_from = current_time + 10
    if start_from >= total_length:
        stop_music()
    else:
        play_music()



middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

labelFrame = LabelFrame(middleframe,bd=5)
labelFrame.pack(fill=X,expand=YES,anchor=W,side=BOTTOM)

playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(labelFrame, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(labelFrame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(labelFrame, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

previousPhoto = PhotoImage(file='images/previous.png')
previousBtn = ttk.Button(labelFrame, image=previousPhoto,command=prev_Song)
previousBtn.grid(row=0, column=3, padx=10)

backwordPhoto = PhotoImage(file='images/backword.png')
backwordBtn = ttk.Button(labelFrame, image=backwordPhoto,command=backword_song)
backwordBtn.grid(row=0, column=4, padx=10)

forwardPhoto = PhotoImage(file='images/forward.png')
forwardBtn = ttk.Button(labelFrame, image=forwardPhoto,command=forward_Song)
forwardBtn.grid(row=0, column=5, padx=10)

nextPhoto = PhotoImage(file='images/nextSong.png')
nextBtn = ttk.Button(labelFrame, image=nextPhoto,command=next_Song)
nextBtn.grid(row=0, column=6, padx=10)


mutePhoto = PhotoImage(file='images/mute.png').subsample(1,1)
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(labelFrame, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=7)

scale = ttk.Scale(labelFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=8, pady=15, padx=30)



#Binding Double-clic event to play music -
playlistbox.bind("<Double-Button>",play_music)



def on_closing():
    stop_music()
    root.destroy()


#root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
