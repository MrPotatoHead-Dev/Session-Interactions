import pandas as pd
from datetime import datetime
import datetime as dt
import time
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
df = pd.read_csv("GBP_USD_5MIN_22-23.csv")

df["date"] = pd.to_datetime(df["date"])

# data formatting
df["date"] = pd.to_datetime(df["date"], format="%Y%m/%d")
df["time"] = pd.to_datetime(df["time"], format="%H:%M").dt.time

# session times
# NOTE these will change when the code is finished
asian_session_finish = datetime.strptime("07:00:00", "%H:%M:%f").time()

london_session_start = datetime.strptime("08:00:00", "%H:%M:%f").time()
london_session_finish = datetime.strptime("14:00:00", "%H:%M:%f").time()

ny_session_start = datetime.strptime("15:00:00", "%H:%M:%f").time()
ny_session_finish = datetime.strptime("19:00:00", "%H:%M:%f").time()

# create a bunch of empy arrays to store true or false data
lh_takes_ah = []
ll_takes_al = []
london_takes_both = []
nyh_takes_ah = []
nyl_takes_al = []
ny_takes_both_asia = []
nyh_takes_lh = []
nyl_takes_ll = []
ny_takes_both_london = []
# create dataframes used to store date and time
# asia
df_london_high = pd.DataFrame()
df_london_low = pd.DataFrame()
df_london_high["date"] = df["date"][:2]
df_london_high["time"] = df["time"][:2]
df_london_low["date"] = df["date"][:2]
df_london_low["time"] = df["time"][:2]

# ny - asia
df_ny_asia_high = pd.DataFrame()
df_ny_asia_low = pd.DataFrame()
df_ny_asia_high["date"] = df["date"][:2]
df_ny_asia_high["time"] = df["time"][:2]
df_ny_asia_low["date"] = df["date"][:2]
df_ny_asia_low["time"] = df["time"][:2]
# ny - london
df_ny_london_high = pd.DataFrame()
df_ny_london_low = pd.DataFrame()
df_ny_london_high["date"] = df["date"][:2]
df_ny_london_high["time"] = df["time"][:2]
df_ny_london_low["date"] = df["date"][:2]
df_ny_london_low["time"] = df["time"][:2]

# reset high, low, range
asian_high = 0
asian_low = 0
asian_range = 0
london_high = 0
london_low = 0
london_range = 0
ny_high = 0
ny_low = 0
ny_range = 0
session_counter = []
# loop dataframe row
for i in range(1, len(df) - 1):
    # ----------------------------------------------------Asia----------------------------------------------------#
    # get the session high and low
    if df.iloc[i]["time"] == asian_session_finish:
        asian_high = max(
            df["high"].iloc[i - 96 : i], default=2
        )  # the defult value is 2 so on the first pass no value can be greater than 2
        asian_low = min(
            df["low"].iloc[i - 96 : i], default=0
        )  # the defult value is 2 so on the first pass no value can be less than 0
        asian_range = (asian_high - asian_low) * 10000
    # check when asia range is taken
    # ----------------------------------------------------London----------------------------------------------------#
    if (
        df.iloc[i]["time"] >= london_session_start
        and df.iloc[i]["time"] <= london_session_finish
    ):
        # store time and date high was taken
        if (df.iloc[i]["close"] > asian_high) and (
            df.iloc[i]["date"] != df_london_high.iloc[-1]["date"]
        ):
            new_row_high = pd.DataFrame(
                {"date": [df.iloc[i]["date"]], "time": [df.iloc[i]["time"]]}
            )
            df_london_high = pd.concat(
                [df_london_high, new_row_high], ignore_index=True
            )
        # store time and date low was taken
        if (df.iloc[i]["close"] < asian_low) and (
            df.iloc[i]["date"] != df_london_low.iloc[-1]["date"]
        ):
            new_row_low = pd.DataFrame(
                {"date": [df.iloc[i]["date"]], "time": [df.iloc[i]["time"]]}
            )
            df_london_low = pd.concat([df_london_low, new_row_low], ignore_index=True)

    # get the session high and low
    if df.iloc[i]["time"] == london_session_finish:
        london_high = max(df["high"].iloc[i - 60 : i])
        london_low = min(df["low"].iloc[i - 60 : i])
        london_range = (london_high - london_low) * 10000

    # ----------------------------------------------------New York----------------------------------------------------#
    # check when asia range is taken
    if (
        df.iloc[i]["time"] >= ny_session_start
        and df.iloc[i]["time"] <= ny_session_finish
    ):
        # store time and date high was taken
        if (df.iloc[i]["close"] > asian_high) and (
            df.iloc[i]["date"] != df_ny_asia_high.iloc[-1]["date"]
        ):
            new_row_high2 = pd.DataFrame(
                {"date": [df.iloc[i]["date"]], "time": [df.iloc[i]["time"]]}
            )
            df_ny_asia_high = pd.concat(
                [df_ny_asia_high, new_row_high2], ignore_index=True
            )
        # store time and date low was taken
        if (df.iloc[i]["close"] < asian_low) and (
            df.iloc[i]["date"] != df_ny_asia_low.iloc[-1]["date"]
        ):
            new_row_low1 = pd.DataFrame(
                {"date": [df.iloc[i]["date"]], "time": [df.iloc[i]["time"]]}
            )
            df_ny_asia_low = pd.concat(
                [df_ny_asia_low, new_row_low1], ignore_index=True
            )
        # store time and date high was taken
        if (df.iloc[i]["close"] > london_high) and (
            df.iloc[i]["date"] != df_ny_london_high.iloc[-1]["date"]
        ):
            new_row_high3 = pd.DataFrame(
                {"date": [df.iloc[i]["date"]], "time": [df.iloc[i]["time"]]}
            )
            df_ny_london_high = pd.concat(
                [df_ny_london_high, new_row_high3], ignore_index=True
            )
        # store time and date low was taken
        if (df.iloc[i]["close"] < london_low) and (
            df.iloc[i]["date"] != df_ny_london_low.iloc[-1]["date"]
        ):
            new_row_low4 = pd.DataFrame(
                {"date": [df.iloc[i]["date"]], "time": [df.iloc[i]["time"]]}
            )
            df_ny_london_low = pd.concat(
                [df_ny_london_low, new_row_low4], ignore_index=True
            )

num_sessions = len(session_counter)

# ----------------------------------------------------Plot Results----------------------------------------------------#
# print(
#     f"london takes asia high: {len(lh_takes_ah)}, thats {round(((len(lh_takes_ah))/num_sessions)*100)}%"
# )
# print(
#     f"london takes asia low: {len(ll_takes_al)}, thats {round(((len(ll_takes_al))/num_sessions)*100)}%"
# )
# print(
#     f"london takes both high and low: {len(london_takes_both)}, thats {round(((len(london_takes_both))/num_sessions)*100)}%"
# )
# print(
#     f"ny takes asian high: {len(nyh_takes_ah)}, thats {round(((len(nyh_takes_ah))/num_sessions)*100)}%"
# )
# print(
#     f"ny takes asian low: {len(nyl_takes_al)}, thats {round(((len(nyl_takes_al))/num_sessions)*100)}%"
# )
# print(
#     f"ny takes both asia's high and low: {len(ny_takes_both_asia)}, thats {round(((len(ny_takes_both_asia))/num_sessions)*100)}%"
# )
# print(
#     f"ny takes london high: {len(nyh_takes_lh)}, thats {round(((len(nyh_takes_lh))/num_sessions)*100)}%"
# )
# print(
#     f"ny takes london low: {len(nyl_takes_ll)}, thats {round(((len(nyl_takes_ll))/num_sessions)*100)}%"
# )
# print(
#     f"ny takes both london's high and low: {len(ny_takes_both_london)}, thats {round(((len(ny_takes_both_london))/num_sessions)*100)}%"
# )
# print(f"total number of days is ~{num_sessions}")


df_london_high["day"] = df_london_high["date"].dt.day_name()
df_london_low["day"] = df_london_low["date"].dt.day_name()
df_ny_london_high["day"] = df_london_high["date"].dt.day_name()
df_ny_london_low["day"] = df_london_high["date"].dt.day_name()
df_ny_asia_high["day"] = df_london_high["date"].dt.day_name()
df_ny_asia_low["day"] = df_london_high["date"].dt.day_name()

# -----------------------------------------------------Export Results to .csv-----------------------------------------------------#
London_data_save = pd.concat([df_london_high, df_london_low], axis=1, ignore_index=True)
df_london_high.to_csv("london-asia-high.csv", index=False)
df_london_low.to_csv("london-asia-low.csv", index=False)
df_ny_london_high.to_csv("ny-london-high.csv", index=False)
df_ny_london_low.to_csv("ny-london-low.csv", index=False)
df_ny_asia_high.to_csv("ny-asia-high.csv", index=False)
df_ny_asia_low.to_csv("ny-asia-low.csv", index=False)
