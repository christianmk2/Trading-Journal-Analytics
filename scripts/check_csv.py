import pandas as pd
from pathlib import Path

file_path = "output/total_pnl.csv"
df1 = pd.read_csv(file_path)
print("\n",file_path)
print(df1.head())

file_path = "output/win_rate.csv"
df1 = pd.read_csv(file_path)
print("\n",file_path)
print(df1.head())

file_path = "output/profit_factor.csv"
df1 = pd.read_csv(file_path)
print("\n",file_path)
print(df1.head())

file_path = "output/trade_counts.csv"
df1 = pd.read_csv(file_path)
print("\n",file_path)
print(df1.head())

file_path = r"data\raw\statement-07_09actual.csv"
df1 = pd.read_csv(file_path)
print("\nTail of ",file_path)
print(df1.tail(10))