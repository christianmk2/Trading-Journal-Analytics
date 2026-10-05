#validate.py
import pandas as pd  

def run_validation(deals_clean, transaction_clean):
    deals_df = pd.read_csv(deals_clean)  
    transaction_df = pd.read_csv(transaction_clean)  
 
    print("\nTotal Deals rows:",len(deals_df))  
    print("\nTotal Transaction rows:",len(transaction_df)) 

    print("\nDeals Row type counts:")
    print(deals_df["row_type"].value_counts())

    print("\nDeals Missing values:")
    print(deals_df.isna().sum())

    print("\nTransactions Missing values:")
    print(transaction_df.isna().sum())

    print("\nDeals Duplicate rows:",deals_df.duplicated().sum())  
    print("\nTransactions Duplicate rows:",transaction_df.duplicated().sum() )  

    if (deals_df.duplicated().sum()) > 0 or (transaction_df.duplicated().sum()) > 0:  
        print("\nValidation failed:")  
        print("There are Duplicated Rows") 
        return False  

    invalid_trade_rows = deals_df[  
        (deals_df["row_type"] == "trade")  
        &  
        (  
            deals_df["symbol"].isna()  
            |  
            deals_df["date"].isna()  
            |  
            deals_df["pnl"].isna()  
        )  
    ]  
    
    if len(invalid_trade_rows) > 0:  
        print("\nValidation failed:")  
        print("Trade rows missing required fields.")
        return False  
    
    # -------------------  
    # SUMMARY ROW  
    # -------------------  

    if ((((deals_df["row_type"] == "summary").all()) 
         & (deals_df["pnl"].notna()).all())):  
        return False  
    
    return True
#EOF