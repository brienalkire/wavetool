# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 13:30:11 2022

@author: brien
"""

## This file is used to develop/test/debug the wavetool functions.
## It can be used in place of the GUI.

import wavetool as wt
import numpy as np

mono_filename='.\TrackWithRumble.wav'
stereo_filename='.\CarmenSeguidillia_V16.wav'

wf_stereo=wt.AudioFile()
wf_mono=wt.AudioFile()
wf_stereo.read_wavefile(stereo_filename)
wf_mono.read_wavefile(mono_filename)
mydata=np.array((wf_mono.m_data,wf_mono.m_data),dtype=np.int16).transpose()

