import h5py
from h5py._hl import group
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import  float64
import datetime as dt
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from numpy.core.fromnumeric import reshape
from progress.bar import Bar

def integrator(data, rows, cols):
    return data.reshape(rows, (data.shape[0]//rows), cols, (data.shape[1]//cols)).sum(axis=1).sum(axis=2)

aspirlLab_file_number = int(input("Please enter AspirlLab_ file numbers: "))
#aspirlLab_file_number = 6
seconds = 474
date_format = '%H:%M:%S'
integration = int(input("Please enter the integration value: "))

aspirlLab_list = []
seconds_list = []
my_list = []

b=0
for a in range(aspirlLab_file_number):
    my_list.append([b,0])
    b +=95000

for i in range(aspirlLab_file_number):
	aspirlLab_list.append('/home/mehmetkcmz/radar_plotter/aspirlLab_files/aspirlLab_'+str(i+1).zfill(8)+'.h5')

for q in range(aspirlLab_file_number*475):
    seconds_list.append("T" + str(q).zfill(8))

seconds_list = np.array(seconds_list).reshape(aspirlLab_file_number, 475)
#print(seconds_list.shape)
now = datetime.now()
current_time_1 = now.strftime(date_format)

i=0
sec_counter = 0

for filename in aspirlLab_list:
    f = h5py.File(filename)
    bar = Bar('aspirlLab_'+str(i+1).zfill(8)+'.h5', fill='■', suffix='%(percent)d%%', max=475)
    ch1_list, ch2_list= [], []
    for groups in seconds_list[sec_counter]:
        #print(list(f.keys()))  -------> T00000000,T00000001,T00000002,T00000003, ... ,T00000474
        #groups = "T" + str(i).zfill(8)
        group = f[(groups)][:]
        
        i_data = group['real']
        q_data = group['imag']

        i_data = np.array(i_data, dtype=float64)
        q_data = np.array(q_data, dtype=float64)    

        # 10.log(10.(I^2+Q^2)+1) then rotate array w/ np.rot90()
        power_ch1 = np.rot90(np.array(np.log10(((np.add(np.square(np.abs(i_data[:, ::2])) , np.square(np.abs(q_data[:, ::2]))))*10)+0.00000001)*10 , dtype=float64))
        power_ch2 = np.rot90(np.array(np.log10(((np.add(np.square(np.abs(i_data[:, 1::2])), np.square(np.abs(q_data[:, 1::2]))))*10)+0.00000001)*10, dtype=float64))
        ch1_list.append(power_ch1)
        ch2_list.append(power_ch2)
        #print("Filename: ", filename, "Group: ", groups)
        bar.next()
    #print("\n\tConcatenating arrays in the list...")
    power_ch1 = np.hstack(np.array(ch1_list))
    power_ch2 = np.hstack(np.array(ch2_list))
    #print("\tArrays concatenated")
    bar.finish()
    #######################################################################
    power_shape = power_ch1.shape
    row = power_shape[1]
    column = power_shape[0]
    trash = (row) % (integration)
    #print("\tTrash columns after integration: ",trash)

    power_ch1 = np.delete(power_ch1, np.s_[(row-trash):row], axis= 1)
    power_ch2 = np.delete(power_ch2, np.s_[(row-trash):row], axis =1)

    power_ch1 = np.array(power_ch1, dtype=float64).reshape(column,(row-trash))
    power_ch2 = np.array(power_ch2, dtype=float64).reshape(column,(row-trash))

    power_ch1 = integrator(power_ch1, column, row//integration)
    power_ch2 = integrator(power_ch2, column, row//integration)

    power_ch1 = power_ch1/(integration)
    power_ch2 = power_ch2/(integration)
    #print("power_ch1.shape", power_ch1.shape, "power_ch2.shape", power_ch2.shape)
    #######################################################################
    
    tx, ty = my_list[i]
    #print("\tGroup: ", groups, "\n\n")

	#fig, ax = plt.subplots()
	
    plt.subplot(211)
    plt.xlim(0, 95000*aspirlLab_file_number)
    plt.ylim(0, 2700)
    plt.imshow(power_ch1, cmap='viridis', interpolation='nearest', aspect='auto', vmin=52, vmax=65, extent = (tx, tx+95000, ty, ty+2700))
    plt.title(r'Reveiver Channel A')                     	# plot title is written and font has been set as 'Times New Roman'
    plt.ylabel('RANGE (km)')                             	# Text('RANGE') has been printed on the y-axis
    plt.xlabel('LOCAL TIME (hh:mm:ss)')                  	# Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
    
    plt.subplot(212)
    plt.xlim(0, 95000*aspirlLab_file_number)
    plt.ylim(0, 2700)
    plt.imshow(power_ch2, cmap='viridis', interpolation='nearest', aspect='auto', vmin=45, vmax=57, extent = (tx, tx+95000, ty, ty+2700))
    plt.title(r'Reveiver Channel B')      	               	# plot title is written and font has been set as 'Times New Roman'
    plt.ylabel('RANGE (km)')               	                # Text('RANGE') has been printed on the y-axis
    plt.xlabel('LOCAL TIME (hh:mm:ss)')                  	# Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
    #plt.pause(0.0000000001)
    i +=1
    sec_counter +=1
    plt.savefig("/home/mehmetkcmz/radar_plotter/plot.pdf")

now = datetime.now()
current_time_2 = now.strftime(date_format)
process_time = datetime.strptime(current_time_2, date_format) - datetime.strptime(current_time_1, date_format)
print("Process time: ", process_time)

#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()

figure = plt.gcf()
figure.set_size_inches(18, 10)

plt.tight_layout()

plt.savefig("/home/mehmetkcmz/radar_plotter/plot.pdf")
#plt.savefig("/home/mehmetkcmz/radar_plotter/plot.pdf", dpi=1000)
plt.show()
exit()
