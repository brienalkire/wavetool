# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 13:30:11 2022

@author: brien
"""

## This file is used to develop/test/debug the wavetool functions.
## It can be used in place of the GUI.

import wavetool as wt
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

mono_filename='.\TrackWithRumble.wav'
stereo_filename='.\CarmenSeguidillia_V16.wav'

wf_stereo=wt.AudioFile()
wf_mono=wt.AudioFile()
wf_stereo.read_wavefile(stereo_filename)
wf_mono.read_wavefile(mono_filename)
#mydata=np.array((wf_mono.m_data,wf_mono.m_data),dtype=np.int16).transpose()

Filter1=wt.AudioFilter()
Filter1.m_passbandedgefrequency_Hz=40
Filter1.m_stopbandedgefrequency_Hz=20
Filter1.design_rumble_filter(wf_stereo.m_samplerate_Hz)

#Filter1.apply_filter(wf_stereo.m_data)
input_data=wf_stereo.m_data
output_data=input_data

if 1 == len(input_data.shape):
    output_data=signal.lfilter(Filter1.m_b,Filter1.m_a,input_data)
else:
    output_data[:,0]=signal.lfilter(Filter1.m_b,Filter1.m_a,input_data[:,0])
    output_data[:,1]=signal.lfilter(Filter1.m_b,Filter1.m_a,input_data[:,1])




