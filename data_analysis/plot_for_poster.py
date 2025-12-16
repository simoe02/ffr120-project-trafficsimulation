import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

data_0 = pd.read_csv("data/sim_data/0.00/data.csv")
data_3 = pd.read_csv("data/sim_data/0.03/data.csv")
data_6 = pd.read_csv("data/sim_data/0.06/data.csv")
data_10 = pd.read_csv("data/sim_data/0.10/data.csv")

route_data_0 = pd.read_csv("data/sim_data/0.00/route_data.csv")
route_data_3 = pd.read_csv("data/sim_data/0.03/route_data.csv")
route_data_6 = pd.read_csv("data/sim_data/0.06/route_data.csv")
route_data_10 = pd.read_csv("data/sim_data/0.10/route_data.csv")

labels = ["0%", "3%",  "7%", "10%"]
data_list = [data_0, data_3, data_6, data_10]
route_data_list = [route_data_0, route_data_3, route_data_6, route_data_10]


time_step = 600 # 10 min
T = 24*3600

ts = np.array([i * time_step for i in range(int(T/time_step))])

plt.figure(figsize=(3, 3))

for data, route_data, l in zip(data_list, route_data_list, labels):
    t = data["time"][:-1] / 3600
    
    num_vehicles = data["num_vehicles"][:-1]
    avg_speed = data["avg_speed"][:-1]
    stopped_vehicles = data["stopped"][:-1]
    
    avg_delay_arr = []
    avg_reroute_list = []

    for t_i in ts:
        t_low = t_i
        t_high = t_i + time_step
        
        data_slice = route_data[route_data["time"] > t_low]
        data_slice = data_slice[data_slice["time"] < t_high]
        
        avg_delay = np.mean(data_slice["delay"])
        
        avg_delay_arr.append(avg_delay)
        
    avg_delay_arr = np.array(avg_delay_arr) / 60 # to min

    smoothed_avg_speed = savgol_filter(avg_speed, window_length=1000, polyorder=3)
    smoothed_stopped = savgol_filter(stopped_vehicles, window_length=1000, polyorder=3)

    plt.plot(ts/3600, avg_delay_arr, label=l)
    
plt.title("Average delay time")
plt.ylabel(r"$t_{delay}$ [min]")
plt.xlabel("t [h]")
plt.xlim(0, 24)
ticks = [0, 6, 12, 18, 24]
plt.xticks(ticks, labels=[f"{int(h):02d}:00" for h in ticks])
# plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("data/images/delay_wo_legend.pdf", transparent=True)
plt.show()