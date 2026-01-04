import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 8,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8
})

include = ["0_0_72h_real_time", "3_0_72h_real_time"]

fig = plt.figure(figsize=(3.4, 3))

t_hours = [1800*i for i in range(72*2)]

for filename in include:
    
    route_data_df = pd.read_csv(f"data/sim_data/{filename}/route_data.csv")
    route_data_df["departure"] = route_data_df["time"] - route_data_df["actual_route_time"]

    delay_avgs = []
    delay_stds = []
    num_departed = []

    for i in range(len(t_hours)-1):
        data_slice = route_data_df[route_data_df["departure"] > t_hours[i]]
        data_slice = data_slice[data_slice["departure"] < t_hours[i+1]]

        delay_avgs.append(np.mean(data_slice["delay"]))
        delay_stds.append(np.std(data_slice["delay"]))
        
        num_departed.append(len(data_slice))

    delay_avgs = np.array(delay_avgs) / 60
    delay_stds = np.array(delay_stds) / 60
    num_departed = np.array(num_departed)
    t_hours_for_plot = np.array(t_hours)[:-1] / 3600 - 47.5

    plt.plot(t_hours_for_plot[48*2:], delay_avgs[48*2:], label=fr"{filename[0]}\%", linewidth=1)
    
xticks = [i*4 for i in range(7)]
xtick_labels = [f"{t}:00" for t in xticks]
plt.xticks(xticks, labels=xtick_labels)

plt.title("Average delay every hour")
plt.ylabel("Delay (min)")
plt.xlabel("Time of day")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
