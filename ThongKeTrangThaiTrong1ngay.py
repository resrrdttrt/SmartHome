import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

user = '217c57c7-726b-4231-a98d-a05c961f5678'
folder_path = f'data/{user}'  


fig, axes = plt.subplots(4, 7, figsize=(21, 9))
i=0
j=0

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'): 
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        timestamps = df['ts']
        date = pd.to_datetime(timestamps.iloc[0]).date()
        new_element_first = pd.Series([f"{date} 00:00:00"])
        new_element_last = pd.Series([f"{date} 23:59:59"])
        updated_timestamps = pd.concat([new_element_last, timestamps, new_element_first], ignore_index=True)


        binary_values = df['str_v']
        new_value_first = 1 - binary_values.iloc[0]
        new_value_last = binary_values.iloc[-1]
        new_element_first = pd.Series([new_value_first])
        new_element_last = pd.Series([new_value_last])
        updated_values = pd.concat([new_element_last, binary_values,new_element_first], ignore_index=True)


        datetime_objects = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in updated_timestamps]
        time_points = date2num(datetime_objects)
        ax = axes[i, j]
        ax.step(time_points, updated_values, where='pre', color='b')
        ax.set_title(filename.replace('.csv', ''))
        ax.set_xticks([])
        ax.set_yticks([])
        if j<6:
            j=j+1
        else:
            i=i+1
            j=0
# plt.savefig(f'figure/{user}.png')
# plt.close();
plt.tight_layout()
plt.show()