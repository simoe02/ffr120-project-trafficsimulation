import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

data_0 = pd.read_csv("data/sim_data/0.00/data.csv")
data_1 = pd.read_csv("data/sim_data/0.01/data.csv")
data_2 = pd.read_csv("data/sim_data/0.02/data.csv")
data_3 = pd.read_csv("data/sim_data/0.03/data.csv")
data_4 = pd.read_csv("data/sim_data/0.04/data.csv")
data_5 = pd.read_csv("data/sim_data/0.05/data.csv")
data_6 = pd.read_csv("data/sim_data/0.06/data.csv")
data_7 = pd.read_csv("data/sim_data/0.07/data.csv")
data_8 = pd.read_csv("data/sim_data/0.08/data.csv")
data_9 = pd.read_csv("data/sim_data/0.09/data.csv")
data_10 = pd.read_csv("data/sim_data/0.10/data.csv")

labels = ["0%", "1%", "2%", "3%", "4%", "5%", "6%", "7%", "8%", "9%", "10%"]
data_list = [data_0, data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, data_9, data_10]

fig, ax = plt.subplots(2, 2)

for data, l in zip(data_list, labels):
    t = data["time"][:-1]
    num_vehicles = data["num_vehicles"][:-1]
    avg_speed = data["avg_speed"][:-1]
    stopped_vehicles = data["stopped"][:-1]
    completed_routes = data["completed_routes"][:-1]

    smoothed_avg_speed = savgol_filter(avg_speed, window_length=1000, polyorder=3)

    smoothed_stopped = savgol_filter(stopped_vehicles, window_length=1000, polyorder=3)

    ax[0, 0].plot(t/3600, num_vehicles, label=l)
    ax[0, 1].plot(t/3600, completed_routes, label=l)
    ax[1, 0].plot(t/3600, smoothed_avg_speed, label=l)
    ax[1, 1].plot(t/3600, smoothed_stopped, label=l)
    
    
ax[0, 0].set_title("Number of vehicles")
ax[0, 0].grid()
ax[0, 1].set_title("Number of completed routes")
ax[0, 1].legend()
ax[0, 1].grid()
ax[1, 0].set_title("Average speed")
ax[1, 0].set_ylabel("Speed [m/s]")
ax[1, 0].grid()
ax[1, 1].set_title("Stopped vehicles")
ax[1, 1].grid()

plt.show()
