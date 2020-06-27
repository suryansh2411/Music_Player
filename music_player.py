import os # to fetch songs and directories 
from tkinter.filedialog import askdirectory # for selecting our song directory
import pygame # for playing music
from mutagen.id3 import ID3 # For tagging the meta data to our songs
from tkinter import * # for UI

root = Tk()
root.minsize(50,72)
root.title('Music Player')
scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = BOTH) 

listofsongs = []
realnames = []

v = StringVar()
songlabel = Label(root,textvariable=v,width=70)
index = 0

def directorychooser():

    directory = askdirectory()
    os.chdir(directory)
    #Loop over all the files in that directory
    for file in os.listdir(directory):
        # only add them if they end with .mp3
        if file.endswith(".mp3"):
            realdir = os.path.realpath(file)
	# load the meta data of that song into audio variable. (A dictionary)
            audio = ID3(realdir)
	# TIT2 refers to the TITLE of the song, So let’s append that to realnames
            realnames.append(audio['TIT2'].text[0])
            listofsongs.append(file)
    
    # initialize pygame
    pygame.mixer.init()
    # load the first song
    pygame.mixer.music.load(listofsongs[0])

directorychooser()

def updatelabel():
    global index # If you do not use global, new index variable will be defined
    global songname
    v.set(realnames[index]) # set our StringVar to the real name 
    #return songname

def nextsong(event):
    global index
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def prevsong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")

def playsong(event):
    pygame.mixer.music.play()
    updatelabel()

def pausesong(event):
    pygame.mixer.music.pause()

def unpausesong(event):
    pygame.mixer.music.unpause()

label = Label(root,text='Music Player') # set the heading
label.pack()

listbox = Listbox(root, height=25,width=150)
listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)
listbox.pack()

realnames.reverse()

for items in realnames:
    listbox.insert(0,items)

realnames.reverse()

nextbutton = Button(root,text = 'Next Music',bg="light blue")
nextbutton.pack(padx=30, pady=10, side=BOTTOM)

previousbutton = Button(root,text = 'Previous Music',bg="light blue")
previousbutton.pack(padx=5, pady=10,side=BOTTOM)

stopbutton = Button(root,text='Stop Music',bg="light blue")
stopbutton.pack(padx=5, pady=10,side=BOTTOM)

playbutton = Button(root, text='Play Music From Start',bg="light blue")
playbutton.pack(padx=5, pady=10,side=BOTTOM)

pausebutton = Button(root, text='Pause Music',bg="light blue")
pausebutton.pack(padx=5, pady=10,side=BOTTOM)

unpausebutton = Button(root, text='Resume Music',bg="light blue")
unpausebutton.pack(padx=5, pady=10,side=BOTTOM)

playbutton.bind("<Button-1>",playsong)
pausebutton.bind("<Button-1>",pausesong)
stopbutton.bind("<Button-1>",stopsong)
unpausebutton.bind("<Button-1>",unpausesong)
nextbutton.bind("<Button-1>",nextsong)
previousbutton.bind("<Button-1>",prevsong)

songlabel.pack()

root.mainloop()