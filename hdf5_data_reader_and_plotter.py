import h5py
from h5py._hl import group
import numpy as np
import matplotlib.pyplot as plt
from numpy import  float64
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from numpy.core.fromnumeric import reshape

def integrator(data, rows, cols):
    return data.reshape(rows, (data.shape[0]//rows), cols, (data.shape[1]//cols)).sum(axis=1).sum(axis=2)

def time_interval(hour_list, minute_list, second_list, interval):
    return [f"{str(m).zfill(2)}:{str(i).zfill(2)}:{str(j).zfill(2)}" 
        	for m in range(hour_list)
        	for i in range(minute_list)
        	for j in range(second_list)
        	if j % interval == 0]

x_label_list = time_interval(1, 8, 55, 60)

seconds = 475
date_format = '%H:%M:%S'

filename = 'aspirlLab_00000001.h5'
f = h5py.File(filename)
#print(list(f.keys()))  -------> T00000000,T00000001,T00000002,T00000003, ... ,T00000474

my_list = []                                                  # An empty array
for q in range(seconds):
    w= ("T" + str(q).zfill(8))
    my_list.append(w)

now = datetime.now()
current_time_1 = now.strftime(date_format)

ch1_list = []
ch2_list = []

for groups in my_list:
    group = f[(groups)][:]

    i_data = group['real']
    q_data = group['imag']

    i_data = np.array(i_data, dtype=float64)
    q_data = np.array(q_data, dtype=float64)    
    
    # 10.log(10.(I^2+Q^2)+1) then rotate array w/ np.rot90()
    power_ch1 = np.rot90(np.array(np.log10(((np.add(np.square(np.abs(i_data[:, ::2])) , np.square(np.abs(q_data[:, ::2]))))*10)+1)*10 , dtype=float64))
    power_ch2 = np.rot90(np.array(np.log10(((np.add(np.square(np.abs(i_data[:, 1::2])), np.square(np.abs(q_data[:, 1::2]))))*10)+1)*10, dtype=float64))
   
    ch1_list.append(power_ch1)
    ch2_list.append(power_ch2)

    print("Group: ", groups)

print("Concatenating arrays in the list...")

power_ch1 = np.hstack(np.array(ch1_list))
power_ch2 = np.hstack(np.array(ch2_list))

print("Arrays concatenated")

######################################################################### INTEGRATION #########################################################################
power_shape = power_ch1.shape

row = power_shape[1]
column = power_shape[0]
integration_value = row//1000
trash = (row) % (integration_value)
print("trash columns after integration: ",trash)

power_ch1 = np.delete(power_ch1, np.s_[(row-trash):row], axis= 1)
power_ch2 = np.delete(power_ch2, np.s_[(row-trash):row], axis =1)

power_ch1 = np.array(power_ch1, dtype=float64).reshape(column,(row-trash))
power_ch2 = np.array(power_ch2, dtype=float64).reshape(column,(row-trash))

power_ch1 = integrator(power_ch1, column, row//integration_value)
power_ch2 = integrator(power_ch2, column, row//integration_value)

power_ch1 = power_ch1/(integration_value)
power_ch2 = power_ch2/(integration_value)

###############################################################################################################################################################

now = datetime.now()
current_time_2 = now.strftime(date_format)
process_time = datetime.strptime(current_time_2, date_format) - datetime.strptime(current_time_1, date_format)
print("Process time: ", process_time)

######################################################################### MATPLOTLIB ##########################################################################
x_ticks = np.arange(0,475,60)

csfont = {'fontname':'Times New Roman'}                       	# font applied as 'Times New Roman'
fig, ax = plt.subplots()

plt.subplot(211)                                              	# Channel 1 located
plt.imshow(power_ch1, cmap='viridis',                         	# Channel 1 is plotted with [plt.imshow()], colormap is 'viridis'
           interpolation='nearest',                           
           aspect='auto', extent=[0,seconds,0,405])             # 475 number is time(s) and 405 number is range(km)
plt.title(r'Reveiver Channel A',**csfont)                     	# plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)                             	# Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  	# Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.clim(54,57)
plt.xticks(x_ticks, x_label_list, rotation = 0, ha="right")   	# ticks set on x-axis and 'array_clock' printed here
cbar = plt.colorbar()                                     	    # colorbar located
cbar.set_label('POWER (dB)',**csfont)                        	 # 'POWER (dB)' text printed next to colorbar

plt.subplot(212)                                              	# Channel 2 located
plt.imshow(power_ch2, cmap='viridis',                         	# Channel 2 is plotted with [plt.imshow()], colormap is 'viridis' 
           interpolation='nearest', 
           aspect='auto', extent=[0,seconds,0,405])           # 475 number is time(s) and 405 number is range(km)

plt.title(r'Reveiver Channel B',**csfont)      	               	# plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)               	            # Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  	# Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.clim(45,55)
plt.xticks(x_ticks, x_label_list, rotation = 0, ha="right")   	# ticks set on x-axis and 'array_clock' printed here
cbar = plt.colorbar()                                         	# colorbar located
cbar.set_label('POWER (dB)',**csfont)                         	# 'POWER (dB)' text printed next to colorbar

fig.tight_layout()                                            	# tight_layout automatically adjusts subplot params so that the
                                                              	# subplot(s) fits in to the figure area.
plt.show()
###############################################################################################################################################################