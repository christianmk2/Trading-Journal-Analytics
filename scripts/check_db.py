from sqlalchemy import create_engine  
import pandas as pd  
  
engine = create_engine("sqlite:///trading_journal.db")  
  
"""# check deals table  
deals_query = "SELECT * FROM deals LIMIT 5"  
deals_df = pd.read_sql(deals_query, engine)  
  
print("\nDEALS TABLE")  
print(deals_df)  
  
# check transactions table  
transactions_query = "SELECT * FROM transactions LIMIT 5"  
transactions_df = pd.read_sql(transactions_query, engine)  
  
print("\nTRANSACTIONS TABLE")  
print(transactions_df)

#check all tables
all_tables = "SELECT name FROM sqlite_master WHERE type='table'"
all_tables_df = pd.read_sql(all_tables, engine)
print(all_tables_df)
"""
all_tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    engine
)
for table in all_tables["name"]:
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1", engine)

    print(f"\nTable: {table}")
    print("Columns:")
    print(df.columns.tolist())