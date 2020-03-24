# Name: Omri Ben Tov
#ID: 204087894

import tkinter as tk
from tkinter import *
import os
import sys
from PIL import Image, ImageTk
import imageProcessing

# Hi! this is GUI program. every screen is applied by a different function.
# The functions are writen first, the root window is defined at the bottom.


def frame_raise(frame): # This function switches frames when called
    frame.tkraise()


def screen_1():
    global frame1
    def callback():    #This function creates a listbox out of path givem by user
        global path
        path = (textbox.get())
        try:                   # Validation of the path given
            os.chdir(path)
            files = os.listdir(path)
            b2.grid_forget()            # the grid_forget and delete commands are to erase the listbox when 'choose is pressed again
            listbox.grid_forget()
            listbox.delete(0,END)
            listbox.grid()
            for item in files:
                if item.split('.')[-1] in ['jpg', 'jpeg', 'gif', 'bmp']:
                    listbox.insert('end', item)
            b2.grid()
        except OSError or FileNotFoundError:
            print('')
    # Frame 1 widgets configurations
    w1 = Label(frame1, text="Please enter image path", background = 'light blue')
    w1.config(font=("Courier"))
    w1.grid(sticky  = NE)
    textbox = tk.Entry(frame1)
    textbox.grid()
    b1 = tk.Button(frame1, text="Choose", command= callback)
    listbox = tk.Listbox(frame1, selectmode=MULTIPLE)
    b2 = tk.Button(frame1, text="Next", command= lambda: nextCallBack(listbox))
    b1.grid_configure()
    frame_raise(frame1)

def nextCallBack(listbox):      # Here we create a list of the files chosen cy user and call screen 2
     chosen = []               # this list contain the files chosen and i will use it till the end of the program
     selected = listbox.curselection()
     for i in selected:
         values = listbox.get(i)
         chosen.append(values)
     screen_2(chosen)

def screen_2(chosen):
    def backbutton(frame1):   #This function takes us back to frame 1 when 'back button (b4) is pressed. it clears the image and the buttons
        frame_raise(frame1)
        img.destroy()
        b3.destroy()
        b4.destroy()

    global frame2
    for value in chosen:
        pic = ImageTk.PhotoImage(file= value)
    labelpic = ImageTk.PhotoImage(file=chosen[0])     # Here the first image is displayed
    img = Label(frame2, image = labelpic,width = 300, height = 300, background = 'light blue',anchor = CENTER)
    img.image = labelpic
    img.grid()

    #Buttons configuration
    b3 = Button(frame2, text = 'next', command = lambda : screen_3(chosen))
    b4 = tk.Button(frame2, text = 'back', command = lambda: backbutton(frame1))
    b3.grid(row = 1,column = 6, sticky = SE)
    b4.grid(column = 0, sticky = SW)
    frame_raise(frame2)    #Raise frame 2




def  screen_3(chosen):  # The third frame is called by the second next button (b3)
    global frame3
    w2 = Label(frame3, text = 'Please choose an operation: ', background = 'light blue')
    w2.config(font=("Courier"))
    w2.grid()
    operations = ['Rotate', 'Mirror', 'Edge' ,'Resize' , 'MessiScale']      # Create a listbox of operations
    global listbox2
    listbox2 = tk.Listbox(frame3, selectmode = SINGLE)
    listbox2.grid()
    for item in operations:
        listbox2.insert('end', item)
    b5 = Button(frame3, text = 'Next', command =lambda: screen_4(chosen))
    b5.grid()
    frame_raise(frame3)     # Raise frame 3


def screen_4(chosen):      # This function is called by the third 'next button (b5). it takes the user process selection and calls for screen 4
    global operation
    operation = list(listbox2.curselection())
    global frame4
    frame_raise(frame4)
    b6 = Button(frame4, text='Next', command= lambda: director(operation,chosen))
    b6.grid()


def director(operation, chosen):       # This function is called by the fourth 'next' button (b6). it takes the path and directs us to the image processing part
    targetimagepath = textbox2.get()
    w4 = Label(frame4, text = 'Apply process and save?' + '\n' + 'Press SAVE and go to path given to see the new image.' + '\n' 'The process may take a few seconds',background = 'light blue')
    w4.grid()
    b7 = Button(frame4,text = 'SAVE',command = lambda: imageProcessing.the_process(operation, chosen, targetimagepath, root))
    b7.grid()

# Root window and frames configurations
root = tk.Tk()

frame1 = Frame(root, background='light blue')
frame2 = Frame(root, background='light blue')
frame3 = Frame(root, background='light blue')
frame4 = Frame(root, background='light blue')
for frame in [frame1,frame2,frame3,frame4]:
    frame.grid(row=0, column=0,sticky='news')

# Frame 4 labels and textbox configuration
w3 = Label(frame4, text = 'Please enter processed-image path ', background = 'light blue')
w3.config(font=("Courier"))
w3.grid()
textbox2 = Entry(frame4)
textbox2.grid()
threshold = 20

chosen = []
screen_1()
root.title("Image select")
root.mainloop()





