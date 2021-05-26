import numpy as np
import matplotlib.pyplot as plt
from numpy import float64
from datetime import datetime

def integrator(data, rows, cols):
    return data.reshape(rows, (data.shape[0]//rows), cols, (data.shape[1]//cols)).sum(axis=1).sum(axis=2)

integration_value = 8
npz_files = 51
date_format = '%H:%M:%S'

my_list = []                                                  # An empty array
for q in range(npz_files):                                          
    w = ("heateroff" + str(q).zfill(5) + ".npz")
    my_list.append(w) 

first_heateroff_0 = np.zeros((167,5600))
first_heateroff_1 = np.zeros((167,5600))

now = datetime.now()
current_time_1 = now.strftime(date_format)
#print("Current Time =", current_time_1)

for npz_file in my_list:    
    heateroff = np.load(npz_file)['arr_0']  
    
    heateroff_0 = heateroff[:,:,0]
    heateroff_1 = heateroff[:,:,1]
    
    # 10.log(10.(I^2+Q^2))    
    heateroff_0 = np.log10((np.add(np.square(np.abs(np.array(heateroff_0.real, dtype=float64)+1)),
                                   np.square(np.abs(np.array(heateroff_0.imag, dtype=float64)+1))))*10) * 10
    heateroff_1 = np.log10((np.add(np.square(np.abs(np.array(heateroff_1.real, dtype=float64)+1)),
                                   np.square(np.abs(np.array(heateroff_0.imag, dtype=float64)+1))))*10) * 10

    #np.concatenate((first_heateroff_0, heateroff_0), axis=0)
    heateroff_0 = np.append(first_heateroff_0, heateroff_0, axis=0)
    first_heateroff_0 = heateroff_0

    #np.concatenate((first_heateroff_1, heateroff_1), axis=0)
    heateroff_1 = np.append(first_heateroff_1, heateroff_1, axis=0)
    first_heateroff_1 = heateroff_1
    
    print("npz_file: ", npz_file)

now = datetime.now()
current_time_2 = now.strftime(date_format)
#print("Current Time =", current_time_2)

process_time = datetime.strptime(current_time_2, date_format) - datetime.strptime(current_time_1, date_format)
print("Process time: ", process_time)

heateroff_0 = np.rot90(heateroff_0)
heateroff_1 = np.rot90(heateroff_1)

heateroff_0 = heateroff_0[:, 167:]        # channel1 
heateroff_1 = heateroff_1[:, 167:]        # channel2

############################################################### INTEGRATION #################################################################
heateroff_0_shape = heateroff_0.shape
heateroff_1_shape = heateroff_1.shape

row = heateroff_0_shape[1]
column = heateroff_0_shape[0]
seconds = row / 167
trash = (row) % (integration_value)
print("trash: ",trash)

heateroff_0 = (np.delete(heateroff_0, np.s_[(row-trash):row], axis= 1))
heateroff_1 = (np.delete(heateroff_1, np.s_[(row-trash):row], axis =1))

heateroff_0 = np.array(heateroff_0, dtype=float64).reshape(column,(row-trash))                               # I DATA - tuple to numpy array
heateroff_1 = np.array(heateroff_1, dtype=float64).reshape(column,(row-trash))                               # I DATA - tuple to numpy array

heateroff_0 = integrator(heateroff_0, column, row//integration_value)
heateroff_1 = integrator(heateroff_1, column, row//integration_value)

heateroff_0 = heateroff_0/(integration_value)
heateroff_1 = heateroff_1/(integration_value)

heateroff = (np.delete(heateroff, np.s_[(row-trash):row], axis=1))

############################################################### MATPLOTLIB #################################################################
csfont = {'fontname':'Times New Roman'}                       # font applied as 'Times New Roman'
fig, ax = plt.subplots()

plt.subplot(211)                                              # Channel 1 located
plt.imshow(heateroff_0, cmap='viridis',                         # Channel 1 is plotted with [plt.imshow()], colormap is 'viridis'
           interpolation='nearest',                           
           aspect='auto')               # 475 number is time(s) and 405 number is range(km)
plt.title(r'Reveiver Channel A',**csfont)                     # plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)                             # Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  # Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.clim(75,85)
cbar = plt.colorbar()                                         # colorbar located
cbar.set_label('POWER (dB)',**csfont)                         # 'POWER (dB)' text printed next to colorbar

plt.subplot(212)                                              # Channel 2 located
plt.imshow(heateroff_1, cmap='viridis',                         # Channel 2 is plotted with [plt.imshow()], colormap is 'viridis' 
           interpolation='nearest', 
           aspect='auto')               # 475 number is time(s) and 405 number is range(km)
plt.title(r'Reveiver Channel B',**csfont)                     # plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)                             # Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  # Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.clim(70,90)
cbar = plt.colorbar()                                         # colorbar located
cbar.set_label('POWER (dB)',**csfont)                         # 'POWER (dB)' text printed next to colorbar

fig.tight_layout()                                            # tight_layout automatically adjusts subplot params so that the
                                                              # subplot(s) fits in to the figure area.
plt.show()
