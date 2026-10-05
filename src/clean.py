#clean.py
import pandas as pd  
from pathlib import Path

from settings.paths import PROCESSED_DATA_DIR

def run_clean(deals_raw, transaction_raw):
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # -------------------  
    # LOAD  
    # -------------------  
    deals_df = pd.read_csv(deals_raw)  
    transactions_df = pd.read_csv(transaction_raw)  
    # -------------------  
    # REMOVE FULLY EMPTY ROWS  
    # -------------------  
    deals_df = deals_df.dropna(how="all")  
    # -------------------  
    # CLEAN COLUMN NAMES  
    # -------------------  
    deals_df.columns = deals_df.columns.str.strip()  
    # -------------------  
    # DATETIME CONVERSION  
    # -------------------  
    deals_df["Closing Time (UTC+8)"] = pd.to_datetime(  
        deals_df["Closing Time (UTC+8)"],  
        format="%d %b %Y %H:%M:%S.%f",  
        errors="coerce"  
    )  
    # -------------------  
    # EXTRACT NUMERIC LOT SIZE  
    # -------------------  
    
    deals_df["Closing Quantity"] = (  
        deals_df["Closing Quantity"]  
        .astype(str)  
        .str.extract(r"([\d.]+)")  
    )  
    
    deals_df["Closing Quantity"] = pd.to_numeric(  
        deals_df["Closing Quantity"],  
        errors="coerce"  
    )  

    # -------------------  
    # NUMERIC CONVERSION  
    # -------------------  
    
    cols = ["Net USD", "Balance USD"]  
    
    deals_df[cols] = (  
        deals_df[cols]  
        .astype(str)  
        .replace(r"\s+", "", regex=True)  
        .apply(pd.to_numeric, errors="coerce")  
    )  

    # -------------------  
    # CLASSIFY ROW TYPES  
    # -------------------  
    
    deals_df["row_type"] = "trade"  
    
    deals_df.loc[  
        deals_df["Symbol"].isna(),  
        "row_type"  
    ] = "summary"  

    deals_df.columns = (  
        deals_df.columns  
        .str.strip()  
        .str.lower()  
        .str.replace(" ", "_")  
        .str.replace(r"[()]", "", regex=True)  
    ) 

    # -------------------  
    # CLEAN TRANSACTIONS  
    # -------------------  
    
    transactions_df.columns = (  
        transactions_df.columns.str.strip()  
    )  
    
    transactions_df["Time (UTC+8)"] = pd.to_datetime(  
        transactions_df["Time (UTC+8)"],  
        format="%d %b %Y %H:%M:%S.%f",  
        errors="coerce"  
    )  

    transactions_df.columns = (  
        transactions_df.columns  
        .str.strip()  
        .str.lower()  
        .str.replace(" ", "_")  
        .str.replace(r"[()]", "", regex=True)  
    )  

    # -------------------  
    # CHANGE COLUMN NAMES
    # -------------------  

    deals_df = deals_df.rename(
        columns={  
            "opening_direction": "direction",  
            "closing_time_utc+8": "date",  
            "closing_price": "exit_price",  
            "closing_quantity": "lot_size",  
            "net_usd": "pnl",  
            "balance_usd": "balance"  
        }
    )  

    transactions_df = transactions_df.rename(
        columns={
            "time_utc+8": "date"
        }
    )

    # -------------------  
    # SAVE CLEANED DATA  
    # -------------------  

    deals_df.to_csv(  
        PROCESSED_DATA_DIR / "deals_clean.csv",  
        index=False  
    )  
    
    transactions_df.to_csv(  
        PROCESSED_DATA_DIR / "transactions_clean.csv",  
        index=False  
    )  

    deals_clean = Path(PROCESSED_DATA_DIR / "deals_clean.csv")  
    transactions_clean = Path(PROCESSED_DATA_DIR / "transactions_clean.csv")

    return deals_clean, transactions_clean
#EOF