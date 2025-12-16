import pandas as pd


data = [
    {"time": 0, "delay": 10},
    {"time": 1, "delay": 1},
    {"time": 2, "delay": 6},
    {"time": 3, "delay": 9},
    {"time": 4, "delay": 1}
]

data_df = pd.DataFrame(data)

print(data_df.head())