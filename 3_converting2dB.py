import os                                                     # This module provides a portable way of using operating system dependent functionality
import h5py                                                   # The h5py package is a Pythonic interface to the HDF5 binary data format
import numpy as np                                            # NumPy is the fundamental package for scientific computing in Python
import matplotlib.pyplot as plt                               # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python

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
