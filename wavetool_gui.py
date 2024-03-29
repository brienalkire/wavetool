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
from tkinter import simpledialog
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
                                               NavigationToolbar2Tk)

# The custom package with the audio file tools and associated math
import wavetool as wt

# Constants and global variables
strRevHistory='WaveTool, by Brien Alkire. Revision 30 Sep 2022.'
bStereoFileOpen=FALSE
bMonoFileOpen=FALSE
bFilterDesigned=FALSE
filename_open1=''
Wavefile1 = wt.AudioFile()
Filter1=wt.AudioFilter()

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

# This function is used for testing and development and can be called
# from the File menu when the menu item is added.    
def test_command():
    
    # Create a child window for the plot
    top= Toplevel(root)
    top.geometry("750x250")
    mytitle="My title"
    top.title(mytitle)
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
     # adding the subplot
    plot1 = fig.add_subplot(111)    
    # plotting the graph
    x=np.linspace(0,20*np.pi)
    y=np.sin(x)
    plot1.plot(x,y)
    plot1.set_xlabel("x",fontsize=12)
    plot1.set_ylabel("y",fontsize=12,rotation=0,labelpad=30)
    plot1.set_xlim([0,20*np.pi])
    plot1.set_ylim([-1,1])
    ax2=plot1.twinx()
    plot1.grid()
    fig.set_tight_layout(tight=True)
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = top)  
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()       
    return

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
    global Wavefile1, filename_open1
    
    # Create the mid and side channel wavefile objects
    Wavefile_mid = wt.AudioFile()
    Wavefile_mid.m_samplerate_Hz=Wavefile1.m_samplerate_Hz
    Wavefile_mid.m_numchannels=1
    Wavefile_mid.m_duration_s=Wavefile1.m_duration_s
    Wavefile_mid.m_numsamples=Wavefile1.m_numsamples
    Wavefile_side = wt.AudioFile()
    Wavefile_side.m_samplerate_Hz=Wavefile1.m_samplerate_Hz
    Wavefile_side.m_numchannels=2
    Wavefile_side.m_duration_s=Wavefile1.m_duration_s
    Wavefile_side.m_numsamples=Wavefile1.m_numsamples    
    Wavefile_side.m_data=Wavefile1.m_data.astype(Wavefile1.m_data.dtype)
    
    # Ask the user if the mid channel is the left and side right or vice versa
    mid_is_left = messagebox.askyesno("Mid and Side Channel Selection",
                                 "Is the left channel (channel 1) the mid channel and right channel (channel 2) the side channel? Answer 'no' if it is the reverse.")    
    
    # Process the data
    if True == mid_is_left:
        Wavefile_mid.m_data=Wavefile1.m_data[:,0].astype(Wavefile1.m_data.dtype) 
        Wavefile_side.m_data[:,0]=(-1*Wavefile_side.m_data[:,1]).astype(Wavefile1.m_data.dtype)
    else:
        Wavefile_mid.m_data=Wavefile1.m_data[:,1].astype(Wavefile1.m_data.dtype) 
        Wavefile_side.m_data[:,1]=(-1*Wavefile_side.m_data[:,0]).astype(Wavefile1.m_data.dtype)
    
    # Save the mid data
    files = [('Wave Files', '*.wav'), 
             ('All Files', '*.*')]
    filename_mid=Wavefile1.append_filename_tag(filename_open1, "_mid")
    filename_mid = fd.asksaveasfilename(filetypes = files, 
                         defaultextension = files,
                         initialfile=filename_mid,
                         title='Filename for Mid-channel Mono Wavefile')
    if 0 < len(filename_mid):
        Wavefile_mid.write_wavefile(
                filename_mid,
                Wavefile_mid.m_samplerate_Hz,
                Wavefile_mid.m_data.astype(Wavefile_mid.m_data.dtype))
    
    filename_side=Wavefile1.append_filename_tag(filename_open1, "_side")
    filename_side = fd.asksaveasfilename(filetypes = files, 
                         defaultextension = files,
                         initialfile=filename_side,
                         title='Filename for Side Data Stereo Wavefile')
    if 0 < len(filename_side):
        Wavefile_side.write_wavefile(
                filename_side,
                Wavefile_side.m_samplerate_Hz,
                Wavefile_side.m_data.astype(Wavefile_side.m_data.dtype))    # Save the side data

    return

def processing_rumblefilter():
    global bFilterDesigned,Wavefile1,Filter1,filename_open1
    
    minedgefreq_Hz=40
    maxedgefreq_Hz=160
    defaultedgefreq_Hz=70
    
    # Prompt the user to select the passband edge frequency.
    Filter1.m_passbandedgefrequency_Hz = simpledialog.askfloat("Rumble Filter Passband Edge Frequency", "What is the passband edge frequency (40 to 160 Hz)?", 
                                   initialvalue=defaultedgefreq_Hz,
                                   minvalue=minedgefreq_Hz, maxvalue=maxedgefreq_Hz)
    
    if None == Filter1.m_passbandedgefrequency_Hz:
        return
    
    # Set the stopband frequency
    Filter1.m_stopbandedgefrequency_Hz=Filter1.m_passbandedgefrequency_Hz/2
    
    # Set the attenuation
    Filter1.m_stopbandattenuation_dB=66
    
    # Design the filter
    Filter1.design_rumble_filter(Wavefile1.m_samplerate_Hz)
    
    # PLOT THE FILTER
    # Create a child window for the plot
    top= Toplevel(root)
    top.geometry("750x250")
    top.title(f"{Filter1.m_passbandedgefrequency_Hz:0.0f} Hz Rumble Filter ({Filter1.m_stopbandattenuation_dB:0.0f} dB/Octave)")
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
    # adding the subplot
    plot1 = fig.add_subplot(111)    
    plot1.plot(Filter1.m_w*Wavefile1.m_samplerate_Hz/np.pi/2,
             20*np.log10(abs(Filter1.m_h)),
                 color='black',
                 label='Magnitude',
                 alpha=0.8)
    plot1.set_xlim([0,2*Filter1.m_passbandedgefrequency_Hz])
    plot1.set_ylim([-80,1])
    plot1.set_xlabel('Frequency (Hz)')
    plot1.set_ylabel('Magnitude (dB)')   
    plot1.grid('both')

    f = np.linspace(0,Wavefile1.m_samplerate_Hz)
    outline_hp_pass_x = [Filter1.m_passbandedgefrequency_Hz, Filter1.m_passbandedgefrequency_Hz, max(f)]
    outline_hp_pass_y = [-80     , -Filter1.m_ripple_dB  , Filter1.m_ripple_dB]
    outline_hp_stop_x = [min(f)  , Filter1.m_stopbandedgefrequency_Hz, Filter1.m_stopbandedgefrequency_Hz]
    outline_hp_stop_y = [-Filter1.m_stopbandattenuation_dB  , -Filter1.m_stopbandattenuation_dB  , -80]
    plot1.plot (outline_hp_pass_x, outline_hp_pass_y,
          color='black',
          linestyle='dashed',
          )
    plot1.plot( outline_hp_stop_x, outline_hp_stop_y,
         color='black',
         linestyle='dashed'
         )        
    
    ax2=plot1.twinx()
    ax2.plot(Filter1.m_w*Wavefile1.m_samplerate_Hz/np.pi/2,
                 np.arctan2(np.imag(Filter1.m_h),np.real(Filter1.m_h))*180/np.pi,
                 color='blue',
                 label='Phase',
                 alpha=0.8)   
    ax2.yaxis.label.set_color('blue')
    ax2.tick_params(axis='y', colors='blue')
    ax2.spines['right'].set_color('blue')
    
    ax2.set_ylabel('Phase (Degrees)')
    ax2.set_ylim([-180,180])

    fig.set_tight_layout(tight=True)
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = top)  
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()       
    
    # Ask the user if they want to apply the filter or cancel.
    answer = messagebox.askyesno("Apply Filter?",
                                 "Would you like to apply the filter? Answer 'yes' to apply the filter and save the results or to'no' to cancel.")

    # If yes, apply the filter and save
    if True == answer:
        filtered_data=Filter1.apply_filter(Wavefile1.m_data)
        
        files = [('Wave Files', '*.wav'), 
             ('All Files', '*.*')]
        filename_filtered=Wavefile1.append_filename_tag(filename_open1,'_Filtered')
        filename_filtered = fd.asksaveasfilename(filetypes = files, 
                         defaultextension = files,
                         initialfile=filename_filtered,
                         title='Filename for Filtered Wavefile')
        if 0 < len(filename_filtered):
            Wavefile1.write_wavefile(
                filename_filtered,
                Wavefile1.m_samplerate_Hz,
                filtered_data.astype(Wavefile1.m_data.dtype))
    
    # Close the window with the plot of the filter
    top.destroy()
    
    bFilterDesigned=TRUE
    
    return
    #############
    
################### FILTERING MENU FUNCTIONS ###########


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

# This is a menu item that can be used to run a routine for testing
# and development.  Simply comment this out when not in use.
#file_menu.add_command(label='Test',
#                      command=test_command,
#                      state="normal")

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

filtering_menu.add_command(label='Rumble Filter',
                           command=processing_rumblefilter,
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
        filtering_menu.entryconfig(0,state='normal')
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
    else:
        filtering_menu.entryconfig(0,state='normal')
        filtering_menu.entryconfig(1,state='normal')
    return

text_tk=Text(root)        
set_menu_states()
tabControl.pack(expand=1, fill="both")
root.mainloop() 