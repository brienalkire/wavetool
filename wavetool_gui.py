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

                             
#### CREATE THE NOTEBOOK ####
# Use the wrapper class rather than Tk so that exception handling can be customized
root = FaultTolerantTk()#tk.Tk()
root.title("Brien's WaveTool")
tabControl = ttk.Notebook(root)

##############################
#### TAB0: ABOUT ####

tab0 = ttk.Frame(tabControl)
tabControl.add(tab0, text='0: About this app')
ttk.Label(tab0,text="Developed by Brien Alkire, revision 20220913").grid(column=0,row=0,padx=30,pady=30)

#### END TAB0 ####
##############################

tabControl.pack(expand=1, fill="both")
root.mainloop() 