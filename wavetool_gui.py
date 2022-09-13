# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:40:23 2022

@author: brien
"""

#### PACKAGE DEPENDENCIES #####
# Packages for the GUI
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile

# Constants and global variables
strRevHistory='Wavetool, by Brien Alkire. Revision 13 Sep 2022.'
bStereoFileOpen=FALSE
bMonoFileOpen=FALSE

# Other misc packages

#### A WRAPPER CLASS FOR TK SO THAT EXCEPTION HANDLING CAN BE CUSTOMIZED ####
class FaultTolerantTk(tk.Tk):
    def report_callback_exception(self, exc, val, tb):
        messagebox.showerror('Error!', val)

#### STRUCTURE OF THE CODE ####
# There are separate tabs Here's a summary of the tabs:
#  Tab 0: provides information about the application, including revision.
#  
#
# The purpose of this code is to 
#
# This code uses exception handling for trapping errors. There is a 
# callback exception handler implemented in
# the FaultTolerantTk class for handling errors once the GUI is up and running.
# If an exception is raised while the GUI is running, a messagebox will display 
# the associated error message, and the main window app will continue 
# once the messagebox is closed.

                             
# Use the wrapper class rather than Tk so that exception handling can be customized
root = FaultTolerantTk()#tk.Tk()
root.geometry('320x150')
root.title("Brien's WaveTool")
tabControl = ttk.Notebook(root)

#################### FILE MENU FUNCTIONS ##############
def file_open():
    global bMonoFileOpen, bStereoFileOpen
    bMonoFileOpen=TRUE
    bStereoFileOpen=FALSE
    set_menu_states()
    return

def file_close():
    global bMonoFileOpen, bStereoFileOpen
    bMonoFileOpen=FALSE
    bStereoFileOpen=FALSE
    set_menu_states()

#################### PROCESSING MENU FUNCTIONS ##########
def processing_stereotomono():
    print("processing_stereotomono")
    return

def processing_monotostereo():
    print('processing_monotostereo')
    return

def processing_midsideprocessing():
    print('processing_midsideprocessing')
    return

def processing_rumblefilter():
    print('processing_rumblefilter')
    return

#################### ABOUT MENU FUNCTIONS #############
def help_about():
    messagebox.showinfo("About Wavetool",strRevHistory)
    return

#################### CREATE MENUS #####################

# CREATE MENUBAR
menubar = Menu(root)
root.config(menu=menubar)

# CREATE FILE MENU
file_menu = Menu(
    menubar,
    tearoff=0
)

file_menu.add_command(label='Open...',
                      command=file_open)
file_menu.add_command(label='Close',
                      command=file_close)
file_menu.add_separator()
file_menu.add_command(
    label='Exit',
    command=root.destroy
)
menubar.add_cascade(
    label="File",
    menu=file_menu
)

# CREATE PROCESSING MENU
processing_menu=Menu(
    menubar,
    tearoff=0)

processing_menu.add_command(label='Stereo to Mono (x2)',
                            command=processing_stereotomono,
                            state=DISABLED)
processing_menu.add_command(label='Mono (x2) to Stereo',
                            command=processing_monotostereo,
                            state=DISABLED)
processing_menu.add_command(label='Mid-side Processing',
                            command=processing_midsideprocessing,
                            state=DISABLED)
processing_menu.add_command(label='Rumble Filter',
                            command=processing_rumblefilter,
                            state=DISABLED)
menubar.add_cascade(
    label="Processing",
    menu=processing_menu)

# CREATE HELP MENU
help_menu = Menu(
    menubar,
    tearoff=0
)

help_menu.add_command(label='About',
                      command=help_about)

menubar.add_cascade(
    label="Help",
    menu=help_menu
)

#################### UTILITY FUNCTIONS #################

def set_menu_states():
    if TRUE == bStereoFileOpen or TRUE==bMonoFileOpen:
        file_menu.entryconfig(0,state=DISABLED)
        file_menu.entryconfig(1,state='normal')    
        processing_menu.entryconfig(3,state='normal')
    if TRUE == bStereoFileOpen and FALSE==bMonoFileOpen:
        processing_menu.entryconfig(0,state='normal')
        processing_menu.entryconfig(2,state='normal')
    if FALSE == bStereoFileOpen and TRUE ==bMonoFileOpen:
        processing_menu.entryconfig(1,state='normal')
    if FALSE == bStereoFileOpen and FALSE == bMonoFileOpen:
        file_menu.entryconfig(0,state='normal')
        file_menu.entryconfig(1,state=DISABLED)
        processing_menu.entryconfig(0,state=DISABLED)
        processing_menu.entryconfig(1,state=DISABLED)
        processing_menu.entryconfig(2,state=DISABLED)
        processing_menu.entryconfig(3,state=DISABLED)
    return
        
set_menu_states()
tabControl.pack(expand=1, fill="both")
root.mainloop() 