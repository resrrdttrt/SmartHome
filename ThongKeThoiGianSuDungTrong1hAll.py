import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os

big_folder_path = 'data'
for item in os.listdir(big_folder_path):
    folder_path = os.path.join(big_folder_path, item)
    fig, axes = plt.subplots(4, 7, figsize=(21, 9))
    i=0
    j=0

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'): 
            file_path = os.path.join(folder_path, filename)
            final_data =  {i: None for i in range(24)}
            data = pd.read_csv(file_path, parse_dates=['ts'])
            data = data.drop_duplicates(subset='ts',keep=False)
            grouped = data.groupby(data['ts'].dt.hour)
            list_of_dfs = [group.reset_index(drop=True) for _, group in grouped]
            for _,df in enumerate(list_of_dfs):
                df = df.sort_values(by='ts', ascending=True)
                sample_datetime_1 = datetime(df['ts'].iloc[0].year,df['ts'].iloc[0].month,df['ts'].iloc[0].day,df['ts'].iloc[0].hour,0,0)
                sample_datetime_2 = datetime(df['ts'].iloc[0].year,df['ts'].iloc[0].month,df['ts'].iloc[0].day,df['ts'].iloc[0].hour,59,59)
                time_intervals = df.diff()
                time_intervals.iloc[0] = df['ts'].iloc[0] - sample_datetime_1 ,-1 if df['str_v'].iloc[0] == 0 else 1
                # time_intervals.loc[0, 'str_v'] = -1 if df.loc[0, 'str_v'] == 0 else 1
                new_data = {'ts':  sample_datetime_2 - df['ts'].iloc[-1],
                            'str_v': -time_intervals['str_v'].iloc[-1]}
                new_row_df = pd.DataFrame([new_data])
                time_intervals = pd.concat([time_intervals, new_row_df], ignore_index=True)
                total_time_in_state_1 = time_intervals[time_intervals['str_v'] == -1]['ts'].sum()
                final_data[int(f'{df["ts"][0].hour}')] = total_time_in_state_1



            keys = [int(key) for key in final_data.keys()]
            values = list(final_data.values())
            final_df = pd.DataFrame({'hour': keys, 'timedelta': values})
            final_df['timedelta'] = final_df['timedelta'].apply(lambda x: x.total_seconds()/60)
            for index, row in final_df.iterrows():
                if pd.isna(row["timedelta"]):
                    target_time = datetime(data['ts'].iloc[0].year,data['ts'].iloc[0].month,data['ts'].iloc[0].day,int(row['hour']),0,0)
                    try:
                        previous_row = data[data['ts'] < target_time].iloc[0]
                        final_df.loc[row['hour'],'timedelta'] = 60 if previous_row["str_v"] == 1 else 0
                    except:
                        after_row=data[data['ts'] > target_time].iloc[0]
                        final_df.loc[row['hour'],'timedelta'] = 60 if after_row["str_v"] == 0 else 0
            # print(final_df)
            hours = final_df['hour']
            values = final_df['timedelta']
            ax = axes[i, j]
            ax.plot(hours, values, color='b')
            ax.set_title(filename.replace('.csv', ''))
            ax.set_xticks([])
            ax.set_ylim(0,60)
            if j<6:
                j=j+1
            else:
                i=i+1
                j=0
    user = item.replace('\data','')
    plt.savefig(f'Thoigiansudung1h/{user}.png')
    plt.close();