import numpy as np
from datetime import datetime


class HeaterDataProcessor:
    def __init__(self, data_path, save_path):
        self.data_path = data_path
        self.save_path = save_path
        self.date_format = '%H:%M:%S'

    def process_data(self):
        now = datetime.now()
        current_time_1 = now.strftime(self.date_format)

        i = 0
        arrays_list = []

        for q in range(0, 1000, 2):
            heateroff_0 = np.array(np.load(f"{self.data_path}/heateroff{str(q).zfill(5)}.npz")['arr_0'])
            heateroff_1 = np.array(np.load(f"{self.data_path}/heateroff{str(q + 1).zfill(5)}.npz")['arr_0'])

            heateroff = np.rot90(np.concatenate((heateroff_0, heateroff_1), axis=0))
            
            print(f"heateroff{str(q).zfill(5)}.npz + heateroff{str(q + 1).zfill(5)}.npz = heateroff{str(i).zfill(5)}.npz")
            heateroff = (heateroff.mean(axis=1)).reshape(5600, 1, 2)
            i += 1
            arrays_list.append(heateroff)

        print("Concatenating arrays in the list...")
        heateroff = np.hstack(np.array(arrays_list))
        print("Arrays concatenated")

        np.save(f"{self.save_path}/heateroff_integrated_for_2_seconds_merged_new", heateroff)

        now = datetime.now()
        current_time_2 = now.strftime(self.date_format)
        process_time = datetime.strptime(current_time_2, self.date_format) - datetime.strptime(current_time_1, self.date_format)
        print("Process time: ", process_time)


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time}")
        return result

    return wrapper


@measure_execution_time
def main():
    data_processor = HeaterDataProcessor("/run/media/mehmet/DEPO/npz_data", "/home/mehmet/Documents/radar_plotter_2.0/Project_3/merged_2_second_integrated")
    data_processor.process_data()


if __name__ == "__main__":
    main()
