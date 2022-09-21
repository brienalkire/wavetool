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
mydata=np.array((wf_mono.m_data,wf_mono.m_data),dtype=np.int16).transpose()

# Filter design
fp=float(70) # Passband edge frequency in Hz

if 40 > fp or 160 < fp:
    raise ValueError("The passband edge frequency must be between 40 and 160 Hz.")
    
fs=fp/2 # Stopband edge frequency in Hz
rp=0.5 # Maximum passband ripple in dB
rs=66 # Stopband attenuation in dB
# DIGITAL FREQUENCIES IN RADIANS/SAMPLE, NORMALIZED BY PI
ws=2*fs/wf_stereo.m_samplerate_Hz # Stop band edge frequency in cycles per sample ON SCALE OF 0 TO 1 (not 0 to 0.5)
wp=2*fp/wf_stereo.m_samplerate_Hz # Pass band cutoff frequency in cycles per sample ON SCALE OF 0 TO 1 (not 0 to 0.5)

n,wc=signal.ellipord(wp,ws,rp,rs) # Determine the filter order
b, a = signal.ellip (n, rp, rs, wc,"high") # Design the coefficients

# Get the sample response
w,h=signal.freqz(b,a,2**16)

# Plot
fig,(ax1)=plt.subplots(1,1)
ax1.plot(w*wf_stereo.m_samplerate_Hz/np.pi/2,20*np.log10(abs(h)),
         color='black',
         label='Filter Magnitude')

ax2=ax1.twinx()
ax2.plot(w*wf_stereo.m_samplerate_Hz/np.pi/2,
         np.arctan2(np.imag(h),np.real(h))*180/np.pi)


f = np.linspace(0,wf_stereo.m_samplerate_Hz)
outline_hp_pass_x = [fp, fp, max(f)]
outline_hp_pass_y = [-80     , -rp  , rp]
outline_hp_stop_x = [min(f)  , fs, fs]
outline_hp_stop_y = [-rs  , -rs  , -80]
ax1.plot (outline_hp_pass_x, outline_hp_pass_y,
          color='black',
          linestyle='dashed',
          )
ax1.plot( outline_hp_stop_x, outline_hp_stop_y,
         color='black',
         linestyle='dashed'
         )
plt.title(str(n)+'th Order Elliptical IIR Rumble Filter')
ax1.set_xlim([0,2*fp])
ax1.set_ylim([-80,1])
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Magnitude (dB)')
ax2.set_ylabel('Phase (Degrees)')
ax2.set_ylim([-180,180])
ax1.grid('both')
ax1.text(fp+2,-5,f'Passband edge {fp:0.1f} Hz')
ax1.text(fp+2,-10,f'Max ripple {rp:0.1f} dB')
ax1.text(fs+2,-rs,f'Stopband edge {fs:0.1f} Hz')
ax1.text(fs+2,-rs-4,f'Rolloff {rs:0.1f} dB per octave')

