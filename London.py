import pandas as pd
from datetime import datetime
import datetime as dt
import time


df_high = pd.read_csv("london-asia-high.csv")
df_low = pd.read_csv("london-asia-low.csv")
df_high = df_high.drop(columns=["date"])
df_low = df_low.drop(columns=["date"])
print(df_high)
day_counts_high = df_high.groupby("day").count()
print(day_counts_high)
day_counts_low = df_low.groupby("day").count()
print(day_counts_low)

time_counts_high = df_high.groupby("time").count()
time_counts_high = time_counts_high[time_counts_high["day"] > 2]
print(time_counts_high)
time_counts_low = df_low.groupby("time").count()
time_counts_low = time_counts_low[time_counts_low["day"] > 2]
print(time_counts_low)
