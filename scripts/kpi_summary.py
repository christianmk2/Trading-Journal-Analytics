import pandas as pd

# Total Trades
counts = pd.read_csv("output/trade_counts.csv")
total_trades = (
    counts["winning_trades"].iloc[0]
    + counts["losing_trades"].iloc[0]
    + counts["breakeven_trades"].iloc[0]
)

# Total PnL
total_pnl = pd.read_csv(
    "output/total_pnl.csv"
)["total_pnl"].iloc[0]

# Win Rate
win_rate = pd.read_csv("output/win_rate.csv")["win_rate"].iloc[0]

# Profit Factor
profit_factor = pd.read_csv(
    "output/profit_factor.csv"
)["profit_factor"].iloc[0]

# Symbols
symbols = pd.read_csv("output/pnl_by_symbol.csv")

best_symbol = symbols.loc[
    symbols["total_pnl"].idxmax(),
    "symbol"
]

worst_symbol = symbols.loc[
    symbols["total_pnl"].idxmin(),
    "symbol"
]

# Average win/loss
avg = pd.read_csv("output/avg_win_loss.csv")

avg_win = avg["average_win"].iloc[0]
avg_loss = avg["average_loss"].iloc[0]

# Drawdown
dd = pd.read_csv("output/drawdown_analysis.csv")

max_drawdown = dd["drawdown"].min()

summary = pd.DataFrame({
    "Metric": [
        "Total Trades",
        "Total PnL",
        "Win Rate",
        "Profit Factor",
        "Best Symbol",
        "Worst Symbol",
        "Avg Win",
        "Avg Loss",
        "Max Drawdown"
    ],
    "Value": [
        total_trades,
        total_pnl,
        win_rate,
        profit_factor,
        best_symbol,
        worst_symbol,
        avg_win,
        avg_loss,
        max_drawdown
    ]
})

summary.to_csv(
    "output/kpi_summary.csv",
    index=False
)

print("Created output/kpi_summary.csv")
