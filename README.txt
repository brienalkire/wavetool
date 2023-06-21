Project title: wavetool

This project implements utilities for modifying wavefiles and has a Tkinter front-end. Utilities include filtering, converting between stereo and mono, 
and mid-side processing, etc.

The class with all the math is defined in "wavetool.py".  There's a GUI
front-end in "wavetool_gui.py". There's also a file called wavetool_test.py that can be used for test and development.

Note that the application can read and write 16 and 32 bit integer formats, and 32-bit floating point formats. It can read 24-bit
integer formats, but not write them. I recommend using this application with 32-bit floating point formats for serious audio
applications (for instance, Pro Tools can bounce tracks and mixes to 32-bit floating point).

Citation:
	wavetool, by Brien Alkire, brienalkire@protonmail.com, September 2022


