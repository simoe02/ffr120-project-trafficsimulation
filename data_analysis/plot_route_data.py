import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

route_data_0 = pd.read_csv("data/sim_data/0.00/route_data.csv")
route_data_1 = pd.read_csv("data/sim_data/0.01/route_data.csv")
route_data_2 = pd.read_csv("data/sim_data/0.02/route_data.csv")
route_data_3 = pd.read_csv("data/sim_data/0.03/route_data.csv")
route_data_4 = pd.read_csv("data/sim_data/0.04/route_data.csv")
route_data_5 = pd.read_csv("data/sim_data/0.05/route_data.csv")
route_data_6 = pd.read_csv("data/sim_data/0.06/route_data.csv")
route_data_7 = pd.read_csv("data/sim_data/0.07/route_data.csv")
route_data_8 = pd.read_csv("data/sim_data/0.08/route_data.csv")
route_data_9 = pd.read_csv("data/sim_data/0.09/route_data.csv")
route_data_10 = pd.read_csv("data/sim_data/0.10/route_data.csv")

route_data_list = [route_data_0, route_data_1, route_data_2, route_data_3, route_data_4, route_data_5, route_data_6, route_data_7, route_data_8, route_data_9, route_data_10]
labels = ["0%", "1%", "2%", "3%", "4%", "5%", "6%", "7%", "8%", "9%", "10%"]

time_step = 600 # 10 min
T = 24*3600

ts = np.array([i * time_step for i in range(int(T/time_step))])

fig, ax = plt.subplots(1, 2)

for route_data, l in zip(route_data_list, labels):
    avg_delay_list = []
    avg_reroute_list = []

    for t_i in ts:
        t_low = t_i
        t_high = t_i + time_step
        
        data_slice = route_data[route_data["time"] > t_low]
        data_slice = data_slice[data_slice["time"] < t_high]
        
        avg_delay = np.mean(data_slice["delay"])
        avg_reroutes = np.mean(data_slice["route_replannings"])
        
        avg_delay_list.append(avg_delay)
        avg_reroute_list.append(avg_reroutes)
        
    avg_delay_list = np.array(avg_delay_list) / 60 # to min
    avg_reroute_list = np.array(avg_reroute_list)
    
    ax[0].plot(ts/3600, avg_delay_list, label=l)
    ax[1].plot(ts/3600, avg_reroute_list, label=l)
    
ax[0].set_title("Avg delay to dest")
ax[0].set_ylabel("min")
ax[0].legend()
ax[0].grid()
ax[1].set_title("Avg reroutes on way to dest")
ax[1].grid()

plt.show()