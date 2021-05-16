import os                                                     # This module provides a portable way of using operating system dependent functionality
import h5py                                                   # The h5py package is a Pythonic interface to the HDF5 binary data format
import numpy as np                                            # NumPy is the fundamental package for scientific computing in Python
import matplotlib.pyplot as plt                               # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python

from matplotlib.ticker import AutoMinorLocator                # Locator for minor ticks when the axis is linear and the major ticks are uniformly
                                                              # spaced. Subdivides the major tick interval into a specified number of minor
                                                              # intervals, defaulting to 4 or 5 depending on the major interval.

array_clock = (("14:54:24"),(""),(""),(""),(""),(""),         # this array will be located on the x-axis of the image to be plotted later
               ("14:54:25"),(""),(""),(""),(""),(""),
               ("14:54:26"),(""),(""),(""),(""),(""),
               ("14:54:27"),(""),(""),(""),(""),(""),
               ("14:54:28"),(""),(""),(""),(""),(""),
               ("14:54:29"),(""),(""),(""),(""),(""),
               ("14:54:30"),(""),(""),(""),(""),(""),
               ("14:54:31"),(""),(""),(""),(""),(""))

array_clock = np.array(array_clock)                           # array_clock converted to numpy array
print(type(array_clock))                                      # output = <class 'numpy.ndarray'>
print(array_clock.shape)                                      # output = (48,)

x = np.arange(0,475,10)                                       # customizing ticks for x-axis (begin:0, finish:475, each time increased by 10)
y = np.arange(5,406,20)                                       # customizing ticks for y-axis (begin:5, finish:405, each time increased by 20)

csfont = {'fontname':'Times New Roman'}                       # font applied as 'Times New Roman'

fig, ax = plt.subplots()

channel1 = np.load('channel1_snr.npy')                        # loading demodulated channel_1 data that converted dB form
plt.subplot(211)                                              # Channel 1 located
plt.imshow(channel1, cmap='viridis',                          # Channel 1 is plotted with [plt.imshow()], colormap is 'viridis'
           interpolation='nearest',                           
           aspect='auto' ,extent=[0,475,0,405])               # 475 number is time(s) and 405 number is range(km)
plt.title(r'Reveiver Channel A',**csfont)                     # plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)                             # Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  # Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.xticks(x, array_clock)                                    # ticks set on x-axis and 'array_clock' printed here
plt.yticks(y)                                                 # ticks set on y-axis
cbar = plt.colorbar()                                         # colorbar located
cbar.set_label('POWER (dB)',**csfont)                         # 'POWER (dB)' text printed next to colorbar

channel2 = np.load('channel2_snr.npy')                        # loading demodulated channel_2 data that converted dB form
plt.subplot(212)                                              # Channel 2 located
plt.imshow(channel2, cmap='viridis',                          # Channel 2 is plotted with [plt.imshow()], colormap is 'viridis' 
           interpolation='nearest', 
           aspect='auto', extent=[0,475,0,405])               # 475 number is time(s) and 405 number is range(km)
plt.title(r'Reveiver Channel B',**csfont)                     # plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)                             # Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  # Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.xticks(x, array_clock)                                    # ticks set on x-axis and 'array_clock' printed here
plt.yticks(y)                                                 # ticks set on y-axis
cbar = plt.colorbar()                                         # colorbar located
cbar.set_label('POWER (dB)',**csfont)                         # 'POWER (dB)' text printed next to colorbar

fig.tight_layout()                                            # tight_layout automatically adjusts subplot params so that the
                                                              # subplot(s) fits in to the figure area.

plt.show()                                                    # Display all open figures.
