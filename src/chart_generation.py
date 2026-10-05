from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from settings.paths import CHARTS_DIR, POSTGRES_SQL_DIR, SQLITE_SQL_DIR


# ====================================
# PATH SETTINGS
# ====================================

def sql_path(engine):
    if engine.dialect.name == "postgresql":
        print("Using PostgreSQL queries")
        return POSTGRES_SQL_DIR
    print("Using SQLite queries")
    return SQLITE_SQL_DIR


# ====================================
# GLOBAL STYLING
# ====================================

plt.style.use("seaborn-v0_8-whitegrid")

FIG_SIZE = (10, 5)

COLORS = {
    "profit": "#2E8B57",
    "loss": "#C00000",
    "equity": "#4472C4",
    "drawdown": "#C00000",
}


# ====================================
# FOLDER CREATION
# ====================================

def generate_folder():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# ====================================
# ALL CHART CALL
# ====================================

def generate_all_charts(engine):
    path = sql_path(engine)
    generate_equity_curve(engine, path)
    generate_drawdown_chart(engine, path)
    generate_daily_pnl_chart(engine, path)
    generate_monthly_pnl_chart(engine, path)
    generate_pnl_by_symbol_chart(engine, path)
    generate_session_analysis(engine, path)
    generate_weekday_analysis(engine, path)
# ====================================
# EQUITY CURVE
# ====================================

def generate_equity_curve(engine, sql_path):
    generate_folder()
    
    
    df = pd.read_sql_query(
        Path(sql_path, "equity_curve.sql").read_text(),
        engine
    )

    df["date"] = pd.to_datetime(df["date"])
    df["cumulative_pnl"] = pd.to_numeric(df["cumulative_pnl"])

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    ax.plot(
        df["date"],
        df["cumulative_pnl"],
        color=COLORS["equity"],
        linewidth=2.5
    )

    ax.fill_between(
        df["date"],
        df["cumulative_pnl"],
        alpha=0.25,
        color=COLORS["equity"]
    )

    ax.set_title(
        "Equity Curve",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Cumulative PnL (USD)")

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()

    fig.savefig(
        CHARTS_DIR / "equity_curve.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved charts/equity_curve.png")

# ====================================
# DRAWDOWN
# ====================================

def generate_drawdown_chart(engine, sql_path):

    generate_folder()

    df = pd.read_sql_query(
        Path(sql_path, "drawdown_analysis.sql").read_text(),
        engine
    )

    df["date"] = pd.to_datetime(df["date"])
    df["drawdown"] = pd.to_numeric(df["drawdown"])

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    ax.fill_between(
        df["date"],
        df["drawdown"],
        0,
        color=COLORS["drawdown"],
        alpha=0.40
    )

    ax.plot(
        df["date"],
        df["drawdown"],
        color=COLORS["drawdown"],
        linewidth=2
    )

    ax.set_title(
        "Drawdown Analysis",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Trade Date")
    ax.set_ylabel("Drawdown (USD)")

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()

    fig.savefig(
        CHARTS_DIR / "drawdown.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved charts/drawdown.png")


# ====================================
# DAILY PNL
# ====================================

def generate_daily_pnl_chart(engine, sql_path):

    generate_folder()

    df = pd.read_sql_query(
        Path(sql_path, "daily_pnl.sql").read_text(), 
        engine
    )

    df["trade_day"] = pd.to_datetime(df["trade_day"])
    df["daily_pnl"] = pd.to_numeric(df["daily_pnl"])

    df = df.sort_values("trade_day")

    colors = [
        COLORS["profit"]
        if pnl >= 0
        else COLORS["loss"]
        for pnl in df["daily_pnl"]
    ]

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    ax.bar(
        df["trade_day"],
        df["daily_pnl"],
        color=colors
    )

    ax.axhline(
        0,
        color="black",
        linewidth=1
    )

    ax.set_title(
        "Daily PnL",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("PnL (USD)")

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()

    fig.savefig(
        CHARTS_DIR / "daily_pnl.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved charts/daily_pnl.png")


# ====================================
# MONTHLY PNL
# ====================================

def generate_monthly_pnl_chart(engine, sql_path):

    generate_folder()

    df = pd.read_sql_query(
        Path(sql_path, "monthly_pnl.sql").read_text(),
        engine
        )
    
    df["month"] = pd.to_datetime(df["month"])
    df["pnl"] = pd.to_numeric(df["pnl"])

    colors = [
        COLORS["profit"]
        if pnl >= 0
        else COLORS["loss"]
        for pnl in df["pnl"]
    ]

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    bars = ax.bar(
        df["month"],
        df["pnl"],
        color=colors
    )

    ax.axhline(
        0,
        color="black",
        linewidth=1
    )

    for bar in bars:

        value = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    ax.set_title(
        "Monthly PnL",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("PnL (USD)")
    plt.xticks(rotation=45)

    plt.tight_layout()

    fig.savefig(
        CHARTS_DIR / "monthly_pnl.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved charts/monthly_pnl.png")

# ====================================
# PNL BY SYMBOL
# ====================================

def generate_pnl_by_symbol_chart(engine, sql_path):



    generate_folder()

    df = pd.read_sql_query(
        Path(sql_path, "pnl_by_symbol.sql").read_text(),
        engine
    )

    df["symbol"] = df["symbol"].astype(str)
    df["total_pnl"] = pd.to_numeric(df["total_pnl"])

    df = df.sort_values("total_pnl")

    colors = [
        COLORS["profit"]
        if pnl >= 0
        else COLORS["loss"]
        for pnl in df["total_pnl"]
    ]

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    bars = ax.barh(
        df["symbol"],
        df["total_pnl"],
        color=colors
    )

    ax.axvline(
        0,
        color="black",
        linewidth=1
    )

    for bar in bars:

        value = bar.get_width()

        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.2f}",
            va="center",
            fontsize=8
        )

    ax.set_title(
        "PnL by Symbol",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Total PnL (USD)")
    ax.set_ylabel("Symbol")

    plt.tight_layout()

    fig.savefig(
        CHARTS_DIR / "pnl_by_symbol.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved charts/pnl_by_symbol.png")

# ====================================
# SESSION ANALYSIS
# ====================================


def generate_session_analysis(engine, sql_path):
    generate_folder()

    df = pd.read_sql_query(
        Path(sql_path, "session_analysis.sql").read_text(),
        engine
    )

    df["session"] = df["session"].astype(str)
    df["total_pnl"] = pd.to_numeric(df["total_pnl"])

    df = df.sort_values("total_pnl")

    colors = [
        COLORS["profit"]
        if pnl >= 0
        else COLORS["loss"]
        for pnl in df["total_pnl"]
    ]

    fig, ax = plt.subplots(figsize=FIG_SIZE)

    bars = ax.barh(
        df["session"],
        df["total_pnl"],
        color=colors
    )

    ax.axvline(
        0,
        color="black",
        linewidth=1
    )

    for bar in bars:

        value = bar.get_width()

        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.2f}",
            va="center",
            fontsize=8
        )

    ax.set_title(
        "Session Performance",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Total PnL (USD)")
    ax.set_ylabel("Session")

    plt.tight_layout()

    fig.savefig(
        CHARTS_DIR / "session_analysis.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved charts/session_analysis.png")

# ====================================
# WEEKDAY ANALYSIS
# ====================================

def generate_weekday_analysis(engine, sql_path):

    generate_folder()

    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path

    df = pd.read_sql_query(
        Path(sql_path, "weekday_analysis.sql").read_text(),
        engine
    )

    if df.empty:
        print("No weekday data found.")
        return

    # Ensure correct data types
    df["weekday"] = df["weekday"].astype(str)

    df["total_pnl"] = pd.to_numeric(
        df["total_pnl"],
        errors="coerce"
    )

    # Remove invalid rows
    df = df.dropna(
        subset=["weekday", "total_pnl"]
    )

    # Include all days found in your DB
    weekday_order = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    df["weekday"] = pd.Categorical(
        df["weekday"],
        categories=weekday_order,
        ordered=True
    )

    df = df.sort_values("weekday")

    colors = [
        COLORS["profit"]
        if pnl >= 0
        else COLORS["loss"]
        for pnl in df["total_pnl"]
    ]

    fig, ax = plt.subplots(
        figsize=FIG_SIZE
    )

    bars = ax.bar(
        df["weekday"],
        df["total_pnl"],
        color=colors
    )

    ax.axhline(
        y=0,
        color="black",
        linewidth=1
    )

    # Add values on bars
    for bar in bars:

        value = float(bar.get_height())

        offset = 5 if value >= 0 else -15

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"{value:.2f}",
            ha="center",
            fontsize=9
        )

    ax.set_title(
        "PnL by Weekday",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Weekday")
    ax.set_ylabel("Total PnL (USD)")

    plt.xticks(rotation=0)
    plt.tight_layout()

    output_file = (
        CHARTS_DIR / "weekday_analysis.png"
    )

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("Saved charts/weekday_analysis.png")
#EOF