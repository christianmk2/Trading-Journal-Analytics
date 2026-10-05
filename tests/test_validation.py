#test_validation
import pandas as pd  
from pathlib import Path
from sqlalchemy import create_engine

from settings.config import database_url
from settings.paths import CHARTS_DIR, OUTPUT_DIR, PROCESSED_DATA_DIR, SQLITE_SQL_DIR

def test_database_trade_count_matches_clean_csv():
    engine = create_engine(database_url())
    deals_df = pd.read_csv(PROCESSED_DATA_DIR / "deals_clean.csv", encoding="utf-8")

    csv_trade_count = len(deals_df[deals_df["row_type"] == "trade"])
    db_trade_count_df = pd.read_sql_query(
        """
        SELECT COUNT(*) AS trade_count
        FROM deals
        WHERE row_type = 'trade'
        """,
        engine
    )
    db_trade_count = db_trade_count_df.loc[0, "trade_count"]

    assert db_trade_count == csv_trade_count


def test_database_total_pnl_matches_clean_csv():
    engine = create_engine(database_url())
    deals_df = pd.read_csv(PROCESSED_DATA_DIR / "deals_clean.csv", encoding="utf-8")

    csv_trade_rows = deals_df[deals_df["row_type"] == "trade"]
    csv_total_pnl = round(csv_trade_rows["pnl"].sum(), 2)

    db_total_pnl_df = pd.read_sql_query(
        """
        SELECT ROUND(SUM(pnl), 2) AS total_pnl
        FROM deals
        WHERE row_type = 'trade'
        """,
        engine
    )
    db_total_pnl = round(db_total_pnl_df.loc[0, "total_pnl"], 2)

    assert db_total_pnl == csv_total_pnl


def test_trade_counts_match_pnl_signs():
    deals_df = pd.read_csv(PROCESSED_DATA_DIR / "deals_clean.csv", encoding="utf-8")
    counts_df = pd.read_csv(OUTPUT_DIR / "trade_counts.csv", encoding="utf-8")

    trade_rows = deals_df[deals_df["row_type"] == "trade"]

    winning_trades = len(trade_rows[trade_rows["pnl"] > 0])
    losing_trades = len(trade_rows[trade_rows["pnl"] < 0])
    breakeven_trades = len(trade_rows[trade_rows["pnl"] == 0])

    assert winning_trades == counts_df.loc[0, "winning_trades"]
    assert losing_trades == counts_df.loc[0, "losing_trades"]
    assert breakeven_trades == counts_df.loc[0, "breakeven_trades"]


def test_core_sql_files_filter_trade_rows():
    sql_files = [
        SQLITE_SQL_DIR / "trade_counts.sql",
        SQLITE_SQL_DIR / "total_pnl.sql",
        SQLITE_SQL_DIR / "win_rate.sql",
        SQLITE_SQL_DIR / "profit_factor.sql",
    ]

    for sql_file in sql_files:
        with open(sql_file, "r", encoding="utf-8") as file:
            query = file.read().lower()

        assert "where row_type = 'trade'" in query


def test_win_rate_matches_trade_rows():
    deals_df = pd.read_csv(PROCESSED_DATA_DIR / "deals_clean.csv", encoding="utf-8")
    win_rate_df = pd.read_csv(OUTPUT_DIR / "win_rate.csv", encoding="utf-8")

    trade_rows = deals_df[deals_df["row_type"] == "trade"]

    total_trades = len(trade_rows)
    winning_trades = len(trade_rows[trade_rows["pnl"] > 0])

    win_rate = round((winning_trades / total_trades) * 100, 2)

    assert total_trades == win_rate_df.loc[0, "total_trades"]
    assert winning_trades == win_rate_df.loc[0, "winning_trades"]
    assert win_rate == win_rate_df.loc[0, "win_rate"]


def test_profit_factor_matches_trade_rows():
    deals_df = pd.read_csv(PROCESSED_DATA_DIR / "deals_clean.csv", encoding="utf-8")
    profit_factor_df = pd.read_csv(OUTPUT_DIR / "profit_factor.csv", encoding="utf-8")

    trade_rows = deals_df[deals_df["row_type"] == "trade"]

    gross_profit = round(trade_rows[trade_rows["pnl"] > 0]["pnl"].sum(), 2)
    gross_loss = round(abs(trade_rows[trade_rows["pnl"] < 0]["pnl"].sum()), 2)
    profit_factor = round(gross_profit / gross_loss, 2)

    assert gross_profit == profit_factor_df.loc[0, "gross_profit"]
    assert gross_loss == profit_factor_df.loc[0, "gross_loss"]
    assert profit_factor == profit_factor_df.loc[0, "profit_factor"]

def test_daily_pnl_total_matches_trade_rows():
    deals_df = pd.read_csv(PROCESSED_DATA_DIR / "deals_clean.csv", encoding="utf-8")
    daily_df = pd.read_csv(OUTPUT_DIR / "daily_pnl.csv", encoding="utf-8")

    trade_rows = deals_df[deals_df["row_type"] == "trade"]

    source_total = round(trade_rows["pnl"].sum(), 2)
    daily_total = round(daily_df["daily_pnl"].sum(), 2)

    assert daily_total == source_total


def test_equity_curve_chart_exists():
    chart_path = CHARTS_DIR / "equity_curve.png"
    assert chart_path.exists()
    assert chart_path.stat().st_size > 0

def test_daily_pnl_chart_exists():
    chart_path = CHARTS_DIR / "daily_pnl.png"
    assert chart_path.exists()
    assert chart_path.stat().st_size > 0


def test_pnl_by_symbol_chart_exists():
    chart_path = CHARTS_DIR / "pnl_by_symbol.png"
    assert chart_path.exists()
    assert chart_path.stat().st_size > 0
#EOF