import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

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


for filename in include:
    
    data_df = pd.read_csv(f"data/sim_data/{filename}/data.csv")
    
    t = data_df["time"][48*3600*10:-1] / 3600 - 48 # Skip first 48 h and convert to hours
    stopped_vehicles = data_df["stopped"][48*3600*10:-1]
    num_vehicles = data_df["num_vehicles"][48*3600*10:-1]
    
    congestion = stopped_vehicles/num_vehicles

    # stopped_smoothed = savgol_filter(stopped_vehicles, window_length=int(len(t)/100), polyorder=3)
    # num_smoothed = savgol_filter(num_vehicles, window_length=int(len(t)/100), polyorder=3)
    
    congestion_smoothed = savgol_filter(congestion, window_length=int(len(t)/100), polyorder=3)
    
    plt.plot(t, congestion_smoothed, label=fr"{filename[0]}\%", linewidth=1)

xticks = [i*4 for i in range(7)]
xtick_labels = [f"{t}:00" for t in xticks]
plt.xticks(xticks, labels=xtick_labels)

plt.title("Congestion coeff")
plt.ylabel("Coeff")
plt.xlabel("Time of day")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
