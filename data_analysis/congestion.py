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

include = ["0_0_72h_real_time", "1_0_72h_real_time", "3_0_72h_real_time", "5_0_72h_real_time", "7_0_72h_real_time", "0.1_0_72h_real_time"]
labels = [r"0\%", r"1\%", r"3\%", r"5\%", r"7\%", r"10\%"]

fig = plt.figure(figsize=(3.4, 2.2))


for filename, l in zip(include, labels):
    
    data_df = pd.read_csv(f"data/sim_data/{filename}/data.csv")
    
    t = data_df["time"][24*3600*10:48*3600*10] / 3600 - 24 # Skip first 24 h and convert to hours
    stopped_vehicles = data_df["stopped"][24*3600*10:48*3600*10]
    num_vehicles = data_df["num_vehicles"][24*3600*10:48*3600*10]
    
    congestion = stopped_vehicles/num_vehicles * 100 # Change to percent
    
    congestion_smoothed = savgol_filter(congestion, window_length=int(len(t)/100), polyorder=3)
    
    plt.plot(t, congestion_smoothed, label=l, linewidth=1)

xticks = [i*4 for i in range(7)]
xtick_labels = [f"{t}:00" for t in xticks]
plt.xticks(xticks, labels=xtick_labels)

# plt.title("Congestion over a day")
plt.ylabel(r"Congestion (\%)")
plt.xlabel("Time of day")
plt.legend(title=r"$p$", bbox_to_anchor=(1, 1))
plt.grid()

plt.tight_layout()
plt.savefig("data/images/report/congestion22.pdf")
plt.show()
