# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 13:30:11 2022

@author: brien
"""

## This file is used to develop/test/debug the wavetool functions.
## It can be used in place of the GUI.

import wavetool as wt

#filename='.\TrackWithRumble.wav'
filename='.\CarmenSeguidillia_V16.wav'

wf=wt.AudioFile()
wf.read_wavefile(filename)