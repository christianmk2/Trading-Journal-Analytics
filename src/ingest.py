#ingest.py
import pandas as pd  
from io import StringIO  
from pathlib import Path

from settings.paths import PROCESSED_DATA_DIR

def run_ingest(file_path):
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    transact_rows, deals_rows = [], []
    transact,deals = False, False

    with open(file_path, "r", encoding="utf-8-sig") as file:  
        for line in file:  
    
            if line.startswith("Deals"):  
                deals = True  
                transact = False
                continue  
    
            elif line.startswith("Transactions"):  
                deals = False
                transact = True
                continue 

            elif line.startswith("Summary"):  
                break
    
            if deals:  
                deals_rows.append(line)
            elif transact:
                transact_rows.append(line)
    
    csv_data_Deals = "".join(deals_rows)  
    csv_data_Transaction = "".join(transact_rows)  

    deals_df = pd.read_csv(StringIO(csv_data_Deals))  
    transact_df = pd.read_csv(StringIO(csv_data_Transaction))  

    deals_df.to_csv(  
        PROCESSED_DATA_DIR / "deals_raw.csv",  
        index=False  
    )  
    
    transact_df.to_csv(  
        PROCESSED_DATA_DIR / "transactions_raw.csv",  
        index=False  
    )  

    deals_path = Path(PROCESSED_DATA_DIR / "deals_raw.csv")
    transactions_path = Path(PROCESSED_DATA_DIR / "transactions_raw.csv")

    return deals_path, transactions_path
#EOF