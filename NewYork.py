import pandas as pd
from datetime import datetime
import datetime as dt
import time

# ----------------------------------------------------Asia----------------------------------------------------#

# import .csv file
df_asia_high = pd.read_csv("ny-asia-high.csv")
df_asia_low = pd.read_csv("ny-asia-low.csv")

df_london_high = pd.read_csv("ny-london-high.csv")
df_london_low = pd.read_csv("ny-london-low.csv")

# remove unneeded column
df_asia_high = df_asia_high.drop(columns=["date"])
df_asia_low = df_asia_low.drop(columns=["date"])

df_london_high = df_london_high.drop(columns=["date"])
df_london_low = df_london_low.drop(columns=["date"])
# count the days where a high or low was taken
day_counts_asia_high = df_asia_high.groupby("day").count()
day_counts_asia_low = df_asia_low.groupby("day").count()

day_counts_london_high = df_london_high.groupby("day").count()
day_counts_london_low = df_london_low.groupby("day").count()
# count the time that each candle closed outside price range
time_counts_asia_high = df_asia_high.groupby("time").count()
time_counts_asia_high = time_counts_asia_high[time_counts_asia_high["day"] > 1]
time_counts_asia_low = df_asia_low.groupby("time").count()
time_counts_asia_low = time_counts_asia_low[time_counts_asia_low["day"] > 1]

time_counts_london_high = df_london_high.groupby("time").count()
time_counts_london_high = time_counts_london_high[time_counts_london_high["day"] > 1]
time_counts_london_low = df_london_low.groupby("time").count()
time_counts_london_low = time_counts_london_low[time_counts_london_low["day"] > 1]


# print results
print(day_counts_asia_high)
print(day_counts_asia_low)
print(time_counts_asia_high)
print(time_counts_asia_low)

print(day_counts_london_high)
print(day_counts_london_low)
print(time_counts_london_high)
print(time_counts_london_low)
