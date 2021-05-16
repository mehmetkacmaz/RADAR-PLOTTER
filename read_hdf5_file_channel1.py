import os                                                     # This module provides a portable way of using operating system dependent functionality
import h5py                                                   # The h5py package is a Pythonic interface to the HDF5 binary data format
import numpy as np                                            # NumPy is the fundamental package for scientific computing in Python
import matplotlib.pyplot as plt                               # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python
import csv                                                    # The so-called CSV (Comma Separated Values) format is the most common import and export format for
                                                              # spreadsheets and databases.
import time                                                   # This module provides various time-related functions.
from numpy import asarray                                     # Convert the input to an array.
from numpy import savetxt                                     # Save an array to a text file.

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
    
    """
    # save numpy array as csv file
    channel1 = asarray(channel1)
    savetxt(("channel1_1.csv"), channel1.real + channel1.imag, delimiter=',')
    savetxt(("channel2_1.csv"), channel2.real + channel2.imag, delimiter=',')
    """
print(channel1.shape)
