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
from tkinter import filedialog as fd

# The custom package with the audio file tools and associated math
import wavetool as wt

# Constants and global variables
strRevHistory='Wavetool, by Brien Alkire. Revision 13 Sep 2022.'
bStereoFileOpen=FALSE
bMonoFileOpen=FALSE
bFilterDesigned=FALSE
filename_open1=''
Wavefile1 = wt.AudioFile()

# Other misc packages

#### A WRAPPER CLASS FOR TK SO THAT EXCEPTION HANDLING CAN BE CUSTOMIZED ####
class FaultTolerantTk(tk.Tk):
    def report_callback_exception(self, exc, val, tb):
        messagebox.showerror('Error!', val)

#### STRUCTURE OF THE CODE ####
# There are 3 menus. Here's a summary of the menus:
#  File: has items for opening and closing wavefiles, and exiting the app.
#  Processing: once a wave file has been opened, this mention provides items for
#   for processing. Some processing options only work if the file is mono, 
#   and some only for stereo, and some for both.
#  Help: this menu has help related items, including an "About" item to 
#   display revision information.
#
# The purpose of this code is to provide tools for manipulating wavefiles, mostly
# for audio engineering purposes. For instance, you can take a stereo file and
# split it into two mono files. Or you can do some filtering.
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
    global bMonoFileOpen, bStereoFileOpen, filename_open1, Wavefile1
    
    filetypes = (
        ('Wave files', '*.wav'),
        ('All files', '*.*')
    )

    filename_open1 = fd.askopenfilename(
        title='Open a file',
#        initialdir='/',
        filetypes=filetypes)
    
    Wavefile1.read_wavefile(filename_open1)
    if 2 == Wavefile1.m_numchannels:
        bStereoFileOpen=TRUE
    elif 1 == Wavefile1.m_numchannels:
        bMonoFileOpen=TRUE
    else:
        raise ValueError('The wave file has an invalid number of channels.')
    set_menu_states()
    display_wavefile_info()
    return

def file_close():
    global bMonoFileOpen, bStereoFileOpen
    bMonoFileOpen=FALSE
    bStereoFileOpen=FALSE
    display_wavefile_info()
    set_menu_states()

#################### PROCESSING MENU FUNCTIONS ##########
def processing_stereotomono():
    files = [('Wave Files', '*.wav'), 
             ('All Files', '*.*')]
    filename_left=Wavefile1.append_filename_tag(filename_open1,'_Left')
    filename_right=Wavefile1.append_filename_tag(filename_open1,'_Right')
    filename_left = fd.asksaveasfilename(filetypes = files, 
                         defaultextension = files,
                         initialfile=filename_left,
                         title='Left Channel Filename')
    if 0 >= len(filename_left):
        return

    filename_right = fd.asksaveasfilename(filetypes = files, 
                         defaultextension = files,
                         initialfile=filename_right,
                         title='Right Channel Filename')   

    if 0 >= len(filename_right):
        return

    Wavefile1.stereo_to_mono(filename_left, filename_right)
    return

def processing_monotostereo():
    global Wavefile1
    
    answer = messagebox.askyesno("Left and Right Channel Selection",
                                 "Is the current file the left channel (channel 1)? Answer 'no' if it is the right channel (channel 2).")

    Wavefile2=wt.AudioFile()
    filetypes = (
        ('Wave files', '*.wav'),
        ('All files', '*.*')
    )

    # Get the filename for the second wavefile and open it
    if True == answer:
        msg='Open file for the right channel (channel 2)'
    else:
        msg='Open file for the left channel (channel 1)'
    filename_open2 = fd.askopenfilename(
        title=msg,
#        initialdir='/',
        filetypes=filetypes)
    
    Wavefile2.read_wavefile(filename_open2)
    if 1 != Wavefile2.m_numchannels:
        raise ValueError('The wave file is not mono.')
        
    # Get the filename for the stereo results
    filename_stereo = fd.asksaveasfilename(filetypes = filetypes, 
                         defaultextension = ".wav",
                         initialfile="stereo.wav",
                         title='Filename for Stereo File')
    if 0 >= len(filename_stereo):
        return

    # Write the wavefile
    if True == answer:
        Wavefile1.mono_to_stereo(
            filename_stereo,
            Wavefile1.m_samplerate_Hz,
            Wavefile1.m_data,
            Wavefile2.m_data)
    elif False == answer:
        Wavefile1.mono_to_stereo(
            filename_stereo,
            Wavefile1.m_samplerate_Hz,
            Wavefile2.m_data,
            Wavefile1.m_data)
        
    return

def processing_midsideprocessing():
    print('processing_midsideprocessing')
    return

def processing_designrumblefilter():
    global bFilterDesigned
    bFilterDesigned=TRUE
    print('processing_designrumblefilter')
    set_menu_states()
    return

def processing_applyfilter():
    print('processing_applyfilter')
    return

################### FILTERING MENU FUNCTIONS ###########
def dummycommand():
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

menubar.add_cascade(
    label="Processing",
    menu=processing_menu)

# CREATE CASCADED FILTER MENU
filtering_menu=Menu(
    processing_menu,
    tearoff=0)

filtering_menu.add_command(label='Design Rumble Filter',
                           command=processing_designrumblefilter,
                           state=DISABLED)
filtering_menu.add_command(label='Apply Filter',
                           command=processing_applyfilter,
                           state=DISABLED)
processing_menu.add_cascade(label='Filtering',
                            menu=filtering_menu)

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

def display_wavefile_info():
    global Wavefile1,filename_open1,text_tk
    
#    text_tk=Text(root)
    
    # If no file is open, clear the information and return
    if FALSE == bStereoFileOpen and FALSE == bMonoFileOpen:
        text_tk.delete('1.0',END)
        return
    
    # Trim the path from the filename for brevity is the soul of wit
    if 0 > filename_open1.rfind('/'):
        short_filename=filename_open1
    else:
        short_filename=filename_open1[filename_open1.rfind('/')+1:len(filename_open1)]
    
    # Display text information about the open wavefile
    text_tk.insert(INSERT, "Filename: " + short_filename)
    text_tk.insert(END, "\nNum channels: "+str(Wavefile1.m_numchannels))
    text_tk.insert(END,"\nSample Rate (Hz): "+str(Wavefile1.m_samplerate_Hz))
    text_tk.insert(END,"\nFormat: "+str(Wavefile1.m_data.dtype))
    text_tk.insert(END,"\nNum samples: "+str(Wavefile1.m_numsamples))
    text_tk.insert(END,f"\nDuration (sec): {Wavefile1.m_duration_s:.2f}")
    text_tk.pack()

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
    if FALSE == bFilterDesigned:
        filtering_menu.entryconfig(0,state='normal')
        filtering_menu.entryconfig(1,state=DISABLED)
    else:
        filtering_menu.entryconfig(0,state='normal')
        filtering_menu.entryconfig(1,state='normal')
    return

text_tk=Text(root)        
set_menu_states()
tabControl.pack(expand=1, fill="both")
root.mainloop() 