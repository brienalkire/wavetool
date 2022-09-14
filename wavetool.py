# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 10:40:46 2022

@author: brien
"""
from scipy.io import wavfile
import scipy.io
import numpy as np

class AudioFile:
    # Data members
    m_samplerate_Hz=0
    m_numchannels=0
    m_duration_s=0
    m_numsamples=0
    m_data=np.zeros(1)
    
    
    """NAME\n\tAudioFile\n
DESCRIPTION\n
An object with methods and members for processing audio files."""
    def __init__(self)->None:
        """ NAME\n\t__init__\n
DESCRIPTION\n
A constructor for the AudioFile class.\n
INPUTS: None.
OUTPUTS: None."""
        self.m_samplerate=0
        self.m_data=np.zeros(1)

    def read_wavefile(self,filename: str)->None:
        self.m_samplerate_Hz, self.m_data = wavfile.read(filename)
        self.m_numchannels=len(self.m_data.shape)
        self.m_numsamples=self.m_data.shape[0]
        self.m_duration_s=self.m_numsamples/self.m_samplerate_Hz
        
    def write_wavefile(self,filename: str,samplerate_Hz: int,data)->None:
        wavfile.write(filename,samplerate_Hz,data)
        
    def stereo_to_mono(self,filename_left: str,filename_right: str)->None:
        self.write_wavefile(filename_left,
                       self.m_samplerate_Hz,
                       self.m_data[:,0])
        self.write_wavefile(filename_right,
                       self.m_samplerate_Hz,
                       self.m_data[:,1])

    # Append a tag to a filename (e.g., '_left')
    def append_filename_tag(self,filename: str,tag: str)->str:
        """NAME\n\tappend_filename_tag\n
DESCRIPTION\n
Append a tag to a filename. The tag will be appended just before the file extension\t
if there is an extension, or at the end of the filename if there is not an extension.
INPUTS:
    filename - (str) the filename to be appended.
    tag - (str) the tag to append.
OUTPUTS:
    (str) the new filename."""         
        index=filename.rfind('.')
        if 0 < index:
            newfilename=filename[0:index]+tag+filename[index:len(filename)]
        else:
            newfilename=filename+tag
        return newfilename
                