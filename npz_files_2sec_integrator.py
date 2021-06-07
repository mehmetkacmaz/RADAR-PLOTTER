import numpy as np
import matplotlib.pyplot as plt
from numpy import float64
from datetime import datetime

date_format = '%H:%M:%S'

now = datetime.now()
current_time_1 = now.strftime(date_format)
#print("Current Time =", current_time_1)

i,q = 0,0
arrays_list = []

for q in range(0,1000,2):
    heateroff_0 = np.array((np.load("/run/media/mehmet/DEPO/npz_data/heateroff" +   str(q).zfill(5) + ".npz")['arr_0']))
    heateroff_1 = np.array((np.load("/run/media/mehmet/DEPO/npz_data/heateroff" + str(q+1).zfill(5) + ".npz")['arr_0']))

    heateroff = np.rot90(np.concatenate((heateroff_0,heateroff_1), axis=0))
    
    print("heateroff" +   str(q).zfill(5) + ".npz + heateroff" +   str(q+1).zfill(5) + ".npz = heateroff" +   str(i).zfill(5) + ".npz")
    heateroff = (heateroff.mean(axis=1)).reshape(5600,1,2)
    print("heateroff.shape: ", heateroff.shape)
    #np.save('/home/mehmet/Documents/radar_plotter_2.0/Project_3/merged_2_second_integrated/heateroff_integrated_for_2_seconds_{}'.format(i) ,heateroff)
    i +=1
    arrays_list.append(heateroff)

print("Concatenating arrays in the list...")
heateroff = np.hstack(np.array(arrays_list))
print("Arrays concatenated")

np.save('/home/mehmet/Documents/radar_plotter_2.0/Project_3/merged_2_second_integrated/heateroff_integrated_for_2_seconds_merged_new', heateroff)

now = datetime.now()
current_time_2 = now.strftime(date_format)
process_time = datetime.strptime(current_time_2, date_format) - datetime.strptime(current_time_1, date_format)
print("Process time: ", process_time)
