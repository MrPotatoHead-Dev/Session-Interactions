# Session-Interactions-GU
A script that looks at how time influences a sweep on a previous sessions high / low

The session interaction script creates a .csv file that has the time and date that the session range was broken for further analysis.
The purpose of these scripts is to find if there are specific times the market likes to run a range high or low.

When the London.py and NewYork.py scripts are run you have to understand that the first time interval has a large number which can be ignored
Ignore the thursday 00:00 and 00:05 as to bypass an error I had to add 2 rows into the dataframe to allow it to run in the script. 
