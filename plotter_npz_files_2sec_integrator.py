import numpy as np
import matplotlib.pyplot as plt
from numpy import float64
from datetime import datetime

date_format = '%H:%M:%S'

now = datetime.now()
current_time_1 = now.strftime(date_format)
#print("Current Time =", current_time_1)
   
heateroff = np.load('/home/mehmet/Documents/radar_plotter_2.0/Project_3/merged_2_second_integrated/heateroff_integrated_for_2_seconds_merged.npy')
    
heateroff_0 = heateroff[:,:,0]
heateroff_1 = heateroff[:,:,1]

# 10.log(10.(I^2+Q^2))    
heateroff_0 = np.log10((np.add(np.square(np.abs(np.array(heateroff_0.real, dtype=float64)+1)),
                               np.square(np.abs(np.array(heateroff_0.imag, dtype=float64)+1))))*10) * 10
heateroff_1 = np.log10((np.add(np.square(np.abs(np.array(heateroff_1.real, dtype=float64)+1)),
                               np.square(np.abs(np.array(heateroff_0.imag, dtype=float64)+1))))*10) * 10

print(heateroff_0.shape)
print(heateroff_1.shape)

now = datetime.now()
current_time_2 = now.strftime(date_format)
process_time = datetime.strptime(current_time_2, date_format) - datetime.strptime(current_time_1, date_format)
print("Process time: ", process_time)

############################################################### MATPLOTLIB #################################################################
csfont = {'fontname':'Times New Roman'}                       # font applied as 'Times New Roman'
fig, ax = plt.subplots()

plt.subplot(211)                                              # Channel 1 located
plt.imshow(heateroff_0, cmap='viridis',                       # Channel 1 is plotted with [plt.imshow()], colormap is 'viridis'
           interpolation='nearest',                           
           aspect='auto')               # 475 number is time(s) and 405 number is range(km)
plt.title(r'Reveiver Channel A',**csfont)                     # plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)                             # Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  # Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.clim(60,80)
cbar = plt.colorbar()                                         # colorbar located
cbar.set_label('POWER (dB)',**csfont)                         # 'POWER (dB)' text printed next to colorbar

plt.subplot(212)                                              # Channel 2 located
plt.imshow(heateroff_1, cmap='viridis',                       # Channel 2 is plotted with [plt.imshow()], colormap is 'viridis' 
           interpolation='nearest', 
           aspect='auto')               # 475 number is time(s) and 405 number is range(km)
plt.title(r'Reveiver Channel B',**csfont)                     # plot title is written and font has been set as 'Times New Roman'
plt.ylabel('RANGE (km)',**csfont)                             # Text('RANGE') has been printed on the y-axis
plt.xlabel('LOCAL TIME (hh:mm:ss)',**csfont)                  # Text('LOCAL TIME (hh:mm:ss)') has been printed on the x-axis
plt.clim(60,85)
cbar = plt.colorbar()                                         # colorbar located
cbar.set_label('POWER (dB)',**csfont)                         # 'POWER (dB)' text printed next to colorbar

fig.tight_layout()                                            # tight_layout automatically adjusts subplot params so that the
                                                              # subplot(s) fits in to the figure area.
plt.show()
