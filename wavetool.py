# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 10:40:46 2022

@author: Brien Alkire
"""
from scipy.io import wavfile
from scipy import signal
import scipy.io
import numpy as np

class AudioFilter:
    """NAME\n\tAudioFilter\n
DESCRIPTION\n
An object with methods and members for filtering audio data."""

    # Constructor    
    def __init__(self)->None:
        """ NAME\n\t__init__\n
DESCRIPTION\n
A constructor for the AudioFilter class.\n
INPUTS: None.
OUTPUTS: None."""
        self.m_passbandedgefrequency_Hz=0
        self.m_stopbandedgefrequency_Hz=0
        self.m_ripple_dB=0.5
        self.m_stopbandattenuation_dB=60
        self.m_b=0
        self.m_a=0
        self.m_w=0
        self.m_h=0
        
    # Design a high-pass rumble filter
    def design_rumble_filter(self,samplerate_Hz: float)->None:
        """NAME\n\tdesign_rumble_filter\n
DESCRIPTION\n
Design an ellipitcal IIR rumble filter (high-pass).
INPUTS: None.
OUTPUTS: None."""
        ws=2*self.m_stopbandedgefrequency_Hz/samplerate_Hz # Stop band edge frequency in cycles per sample ON SCALE OF 0 TO 1 (not 0 to 0.5)
        wp=2*self.m_passbandedgefrequency_Hz/samplerate_Hz # Pass band cutoff frequency in cycles per sample ON SCALE OF 0 TO 1 (not 0 to 0.5)

        n,wc=signal.ellipord(wp,ws,self.m_ripple_dB,self.m_stopbandattenuation_dB) # Determine the filter order
        self.m_b, self.m_a = signal.ellip (n, self.m_ripple_dB, self.m_stopbandattenuation_dB, wc,"high") # Design the coefficients

        # Get the sample response
        self.m_w,self.m_h=signal.freqz(self.m_b,self.m_a,2**16)    

        return

    # Apply filter
    def apply_filter(self,input_data):
        """NAME\n\tapply_filter\n
DESCRIPTION\n
Applies the current (member) filter.
INPUTS: 
    arg1: numpy array of data to be filtered (may be n-by-1 if mono or n-by-2 if stereo)
OUTPUT:
    numpy array of filtered data (same dimensions as input)."""
        # Apply the filter to channel 1
        output_data=input_data

        if 1 == len(input_data.shape):
            output_data=signal.lfilter(self.m_b,self.m_a,input_data).astype(input_data.dtype)
        else:
            output_data[:,0]=signal.lfilter(self.m_b,self.m_a,input_data[:,0]).astype(input_data.dtype)
            output_data[:,1]=signal.lfilter(self.m_b,self.m_a,input_data[:,1]).astype(input_data.dtype)
        return output_data
    
class AudioFile:
    """NAME\n\tAudioFile\n
DESCRIPTION\n
An object with methods and members for processing audio files."""

    # Data members
    m_samplerate_Hz=0
    m_numchannels=0
    m_duration_s=0
    m_numsamples=0
    m_data=np.zeros(1)
    
    # Constructor    
    def __init__(self)->None:
        """ NAME\n\t__init__\n
DESCRIPTION\n
A constructor for the AudioFile class.\n
INPUTS: None.
OUTPUTS: None."""
        self.m_samplerate_Hz=0
        self.m_data=np.zeros(1)

    # Read a wavefile and populate the AudioFile data
    def read_wavefile(self,filename: str)->None:
        """ NAME\n\tread_wavefile\n
DESCRIPTION\n
Opens a wavefile, reads the contents and populates the AudioFile data.\n
INPUTS:
    arg1: filename and path for the wavefile.
OUTPUTS: None."""
        self.m_samplerate_Hz, self.m_data = wavfile.read(filename)
        self.m_numchannels=len(self.m_data.shape)
        self.m_numsamples=self.m_data.shape[0]
        self.m_duration_s=self.m_numsamples/self.m_samplerate_Hz
        
    # Wrapper for writing data to a wavefile.
    def write_wavefile(self,filename: str,samplerate_Hz: int,data)->None:
        """ NAME\n\twrite_wavefile\n
DESCRIPTION\n
Writes data to a wavefile.\n
INPUTS\n
    arg1: filename and path for the wavefile
    arg2: sample rate in Hertz
    arg3: numpy array(s) of data to be written.
OUTPUTS: None."""
        wavfile.write(filename,
                      samplerate_Hz,
                      data.astype(data.dtype))
        
    # Takes stereo wavefile data and writes it to two mono wavefiles.
    def stereo_to_mono(self,filename_left: str,filename_right: str)->None:
        """ NAME\n\tstereo_to_mono\n
DESCRIPTION\n
Writes stereo data to two mono wave files.\n
INPUTS\n
    arg1: filename and path for the left channel (channel 1)
    arg2: filename and path for the right channel (channel 2)
OUTPUTS: None."""
        self.write_wavefile(filename_left,
                       self.m_samplerate_Hz,
                       self.m_data[:,0])
        self.write_wavefile(filename_right,
                       self.m_samplerate_Hz,
                       self.m_data[:,1])
        
    # Takes data from two mono wavefiles and writes it to a stereo wavefile.
    def mono_to_stereo(self,filename_stereo: str,samplerate_Hz: int,data_left,data_right)->None:
        """ NAME\n\tmono_to_stereo\n
DESCRIPTION\n
Writes mono data from two wave files to a stero wavefile.\n
INPUTS\n
    arg1: filename and path for the stereo wavefile.
    arg2: sample rate in Hertz for both datasets
    arg3: numpy array of data for left channel (channel 1)
    arg4: numpy array of data for right channel (channel 2)
    Note: arg3 and arg4 must be the same length and type
OUTPUTS: None."""
        if data_left.dtype != data_right.dtype:
            raise ValueError('The data types for the left and right channels do not match.')
        if 1 != len(data_left.shape) or 1 != len(data_right.shape):
            raise ValueError('Stereo data was detected where mono data expected.')
        data_stereo=np.array((data_left,data_right),data_left.dtype).transpose()        
        self.write_wavefile(filename_stereo,
                       samplerate_Hz,
                       data_stereo)

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




