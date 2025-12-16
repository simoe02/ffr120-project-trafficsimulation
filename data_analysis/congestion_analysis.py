import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

data_0 = pd.read_csv("data/sim_data/0.00/data.csv")
data_001 = pd.read_csv("data/sim_data/0.01/data.csv")
data_002 = pd.read_csv("data/sim_data/0.02/data.csv")
data_003 = pd.read_csv("data/sim_data/0.03/data.csv")
data_004 = pd.read_csv("data/sim_data/0.04/data.csv")
data_005 = pd.read_csv("data/sim_data/0.05/data.csv")
data_006 = pd.read_csv("data/sim_data/0.06/data.csv")

labels = ["0", "0.01", "0.02", "0.03", "0.04", "0.05", "0.06"]
data_list = [data_0, data_001, data_002, data_003, data_004, data_005, data_006]

fig, ax = plt.subplots(1, 2)

for data, l in zip(data_list, labels):
    t = data["time"][:-1]
    num_vehicles = data["num_vehicles"][:-1]
    stopped_vehicles = data["stopped"][:-1]
    
    smoothed_stopped = savgol_filter(stopped_vehicles, window_length=1000, polyorder=3)
    
    congestion = smoothed_stopped / num_vehicles
    
    ax[0].plot(t/3600, congestion, label=l)
    
plt.show()