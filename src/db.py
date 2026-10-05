# db.py

import pandas as pd
from sqlalchemy import DateTime, Numeric, create_engine

from settings.config import database_url


def load_to_db(deals_clean, transaction_clean):
    # -------------------
    # LOAD CLEAN DATA
    # -------------------
    deals_df = pd.read_csv(deals_clean)
    transaction_df = pd.read_csv(transaction_clean)

    # -------------------
    # CONVERT DATA TYPES
    # -------------------
    deals_df["date"] = pd.to_datetime(
        deals_df["date"],
        errors="coerce"
    )

    transaction_df["date"] = pd.to_datetime(
        transaction_df["date"],
        errors="coerce"
    )

    # -------------------
    # VALIDATE DATES
    # -------------------
    # Summary rows are allowed to have no date.
    invalid_deal_dates = deals_df[
        deals_df["row_type"].eq("trade")
        & deals_df["date"].isna()
    ]

    if not invalid_deal_dates.empty:
        raise ValueError(
            f"Found {len(invalid_deal_dates)} trade row(s) "
            "with an invalid or missing date."
        )

    invalid_transaction_dates = transaction_df[
        transaction_df["date"].isna()
    ]

    if not invalid_transaction_dates.empty:
        raise ValueError(
            f"Found {len(invalid_transaction_dates)} transaction row(s) "
            "with an invalid or missing date."
        )

    # -------------------
    # CREATE DB ENGINE
    # -------------------
    engine = create_engine(database_url())

    # -------------------
    # LOAD DEALS TABLE
    # -------------------
    deals_df.to_sql(
        name="deals",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={
            "date": DateTime(),
            "entry_price": Numeric(18, 5),
            "exit_price": Numeric(18, 5),
            "lot_size": Numeric(18, 5),
            "pnl": Numeric(12, 2),
            "balance": Numeric(12, 2),
        },
    )

    # -------------------
    # LOAD TRANSACTIONS TABLE
    # -------------------
    transaction_df.to_sql(
        name="transactions",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={
            "date": DateTime(),
            "gross_usd": Numeric(12, 2),
        },
    )

    return engine