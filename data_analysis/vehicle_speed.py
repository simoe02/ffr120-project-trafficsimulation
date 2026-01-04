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
    avg_speed = data_df["avg_speed"][48*3600*10:-1] * 3.6 # Skip first 48 h and convert to km/h

    avg_speed_smoothed = savgol_filter(avg_speed, window_length=int(len(t)/100), polyorder=3)
    
    plt.plot(t, avg_speed_smoothed, label=fr"{filename[0]}\%", linewidth=1)

xticks = [i*4 for i in range(7)]
xtick_labels = [f"{t}:00" for t in xticks]
plt.xticks(xticks, labels=xtick_labels)

plt.title("Average vehicle speed")
plt.ylabel("Avg speed (km/h)")
plt.xlabel("Time of day")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("data/images/report/avg_speed.pdf")
plt.show()
