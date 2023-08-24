import matplotlib.pyplot as plt
import pandas as pd
import os
big_folder_path = 'data'
for item in os.listdir(big_folder_path):
    folder_path = os.path.join(big_folder_path, item)

    fig, axes = plt.subplots(4, 7, figsize=(21, 9))
    i=0
    j=0
    max_value=0
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'): 
            file_path = os.path.join(folder_path, filename)
            data = pd.read_csv(file_path, parse_dates=['ts'])
            data['hour'] = data['ts'].dt.hour
            hourly_counts = data.groupby('hour')['str_v'].sum()
            all_hours = pd.DataFrame({"hour": range(24)})
            merged_df = all_hours.merge(hourly_counts, on="hour", how="left")
            merged_df["str_v"] = merged_df["str_v"].fillna(0).astype(int)
            hours = merged_df['hour']
            values = merged_df['str_v']
            if max_value<values.max(): 
                max_value = values.max()
            ax = axes[i, j]
            ax.plot(hours, values, color='b')
            ax.set_title(filename.replace('.csv', ''))
            ax.set_xticks([])
            if j<6:
                j=j+1
            else:
                i=i+1
                j=0
    for ax in axes.flat:
        ax.set_ylim(0,max_value)
    user = item.replace('\data','')
    plt.savefig(f'SoLanBat/{user}.png')
    plt.close();

