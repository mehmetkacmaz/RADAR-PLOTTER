# RADAR-PLOTTER

This project aims to analyzing and plotting the 'aspirlLab_00000001.h5' file, which contains radar data on a Penn State University web page, by means of the python programming language.


ABOUT HDF5

Hierarchical Data Format (HDF) is a set of file formats (HDF4, HDF5) designed to store and organize large amounts of data. Originally developed at the National Center for Supercomputing Applications, it is supported by The HDF Group, a non-profit corporation whose mission is to ensure continued development of HDF5 technologies and the continued accessibility of data stored in HDF.

Our HDF5 file contains 475 datasets (T00000000, T00000001, ..... T00000474) and each dataset includes 5400 real and 5400 imaginer datas. This file contains data of both channel1 and channel2 at the same time, and in our code, the parsing is made for channel1 and channel2.

![Screenshot from 2021-05-07 00-09-39](https://user-images.githubusercontent.com/52501795/118412274-cbcafd80-b6a1-11eb-8293-237e4058e1a5.png)



The following .png file was obtained by plotting the 'aspirlLab_00000001.h5' file.

![radar_plotter_final](https://user-images.githubusercontent.com/52501795/118411989-282d1d80-b6a0-11eb-9b2a-a01eca2cdcf4.PNG)

