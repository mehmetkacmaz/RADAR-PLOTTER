#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 07:27:26 2021

@author: mehmet - emre
"""

import os                                                     # This module provides a portable way of using operating system dependent functionality
import h5py                                                   # The h5py package is a Pythonic interface to the HDF5 binary data format
import numpy as np                                            # NumPy is the fundamental package for scientific computing in Python
from numpy import asarray                                     # Convert the input to an array.
from numpy import savetxt                                     # Save an array to a text file.
import matplotlib.pyplot as plt                               # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python
from matplotlib.ticker import AutoMinorLocator                # Locator for minor ticks when the axis is linear and the major ticks are uniformly
                                                              # spaced. Subdivides the major tick interval into a specified number of minor
                                                              # intervals, defaulting to 4 or 5 depending on the major interval.
import csv                                                    # The so-called CSV (Comma Separated Values) format is the most common import and export format for
                                                              # spreadsheets and databases.
import time                                                   # This module provides various time-related functions.

os.listdir('.')                                               # os.listdir() method in python is used to get the list of all files and directories in the specified directory.

filename = 'aspirlLab_00000001.h5'                            # HDF5 file that analysed in project
f = h5py.File(filename)                                       # Opening file
print(list(f.keys()))                                         # output: T00000000,T00000001, ... ,T00000474

first_ch1 = np.zeros((2700,200))                              # a NumPy array that filled with zeros (2700,200)

# creating an array that give us output of "print(list(f.keys()))"
my_list = []                                                  # An empty array
for q in range(475):                                          
    w= ("T" + str(q).zfill(8))
    my_list.append(w)                                          
###############################
for i in my_list:
    t, x, y, n, m = 0, 0, 0, 0, 0
    a = []
    b = []
    
    t0 = f[(i)][:]
    t = np.linspace(0, 5400, 5400)

    # I Data
    for y in range(0,200):
        for x in range(0,5400):
            a.append(t0[y][x][0])
        
    # Q Data
    for n in range(0,200):
        for m in range(0,5400):
            b.append(t0[n][m][1])

    a = np.array(a)                             # I DATA - tuple to numpy array
    b = np.array(b)                             # Q DATA - tuple to numpy array

    a = a.reshape(200,5400)                     # I DATA - reshape to 200x5400
    b = b.reshape(200,5400)                     # Q DATA - reshape to 200x5400 

    a_channel1 = a[:, ::2]                     # I DATA - CHANNEL 1
    b_channel1 = b[:, ::2]                     # Q DATA - CHANNEL 1

    channel1 = a_channel1 + 1j * b_channel1
    
    channel1_real = channel1.real
    channel1_imag = channel1.imag
    
    channel1 = channel1.reshape(200,2700)
    channel1 = np.rot90(channel1)
    
    channel1 = np.append(first_ch1, channel1, axis=1)
    first_ch1 = channel1
    
    np.save('channel1.npy', channel1)                # save
    print("i: ",i)
print(channel1.shape)

i = 0

first_ch1 = np.zeros((2700,200))                              # a NumPy array that filled with zeros (2700,200)

# creating an array that give us output of "print(list(f.keys()))"
my_list = []                                                  # An empty array
for q in range(475):                                          
    w= ("T" + str(q).zfill(8))
    my_list.append(w)                                         # output of my_list is "T00000000,T00000001, ... ,T00000474"
###############################
for i in my_list:
    t, x, y, n, m = 0, 0, 0, 0, 0
    a = []
    b = []
    
    t0 = f[(i)][:]
    t = np.linspace(0, 5400, 5400)

    # I Data
    for y in range(0,200):
        for x in range(0,5400):
            a.append(t0[y][x][0])
        
    # Q Data
    for n in range(0,200):
        for m in range(0,5400):
            b.append(t0[n][m][1])

    a = np.array(a)                             # I DATA - tuple to numpy array
    b = np.array(b)                             # Q DATA - tuple to numpy array

    a = a.reshape(200,5400)                     # I DATA - reshape to 200x5400
    b = b.reshape(200,5400)                     # Q DATA - reshape to 200x5400 
    
    a_channel2 = a[:, 1::2]                     # I DATA - CHANNEL 2
    b_channel2 = b[:, 1::2]                     # Q DATA - CHANNEL 2

    channel2 = a_channel2 + 1j * b_channel2

    channel2_real = channel2.real
    channel2_imag = channel2.imag

    channel2 = channel2.reshape(200,2700)
    channel2 = np.rot90(channel2)
    
    channel2 = np.append(first_ch2, channel2, axis=1)
    first_ch2 = channel2


    np.save('channel2.npy', channel2)                # save
    print("i: ",i)                                            # output: T00000000,T00000001, ... ,T00000474          
    
    """
    # save numpy array as csv file
    channel2 = asarray(channel2)
    savetxt(("channel1_1.csv"), channel2.real + channel2.imag, delimiter=',')
    savetxt(("channel2_1.csv"), channel2.real + channel2.imag, delimiter=',')
    """
print(channel2.shape)

channel1 = np.load('channel1.npy')                            # load
channel1 = channel1.real + channel1.imag
channel1 = np.log10(channel1)
channel1 = channel1[:, 200:]
np.save('channel1_snr.npy', channel1)                         # save

channel2 = np.load('channel2.npy')                            # load
channel2 = channel2.real + channel2.imag
channel2 = np.log10(channel2)
channel2 = channel2[:, 200:]
np.save('channel2_snr.npy', channel2)                         # save

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
