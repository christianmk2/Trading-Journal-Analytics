#main.py
import argparse
from pathlib import Path

from sqlalchemy import create_engine

from settings.config import database_url
from settings.paths import POSTGRES_SQL_DIR, SQLITE_SQL_DIR
from src.analysis import run_query
from src.chart_generation import generate_all_charts
from src.clean import run_clean
from src.db import load_to_db
from src.ingest import run_ingest
from src.sql_to_excel_dashboard import excel_dashboard
from src.validate import run_validation
db_url = database_url()

def get_sql_folder(engine):
    if engine.dialect.name == "postgresql":
        return POSTGRES_SQL_DIR

    return SQLITE_SQL_DIR

def main():  
    engine = None

    # -------------------  
    # ARGUMENT PARSER  
    # -------------------  
  
    parser = argparse.ArgumentParser(  
        description="Trading Journal Analytics Pipeline"  
    )  
  
    parser.add_argument(  
        "--mode",  
        choices=["etl", "analysis", "dashboard", "chart", "full"],  
        default="full",  
        help="Choose pipeline mode"  
    )  
    parser.add_argument(
        "--file",
        type=str,
        help="Path to cTrader statement CSV file"
    )

    args = parser.parse_args()  

    if args.mode in ["etl", "full"]:

        if args.file:
            raw_file = Path(args.file)

        else:
            from tkinter import Tk, filedialog
            
            root = Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            selected_file = filedialog.askopenfilename(
                title="Select cTrader Statement CSV",
                filetypes=[("CSV Files", "*.csv")]
            )

            if not selected_file:
                print("No file selected.")
                return

            raw_file = Path(selected_file)
    else:
        raw_file = None
  
    # -------------------  
    # ETL PHASE  
    # -------------------  
    if (args.mode in ["etl", "full"]):  
  
        try:  
            deals_raw, transactions_raw = run_ingest(raw_file)  
            deals_clean, transactions_clean = run_clean(deals_raw,transactions_raw)  
            validation_passed = run_validation(deals_clean,transactions_clean)  
  
            if validation_passed:  
  
                engine = load_to_db(deals_clean,transactions_clean)  
  
                print("\n--------------------")  
                print("ETL Phase Complete")  
                print("--------------------\n")  

            else:  
                print("Validation failed.")  
                return
  
        except Exception as e:  
            print(f"ETL Failed: {e}")  
            return
  
    # -------------------  
    # ANALYSIS PHASE  
    # -------------------  
  
    if (args.mode in ["analysis", "full"]):  
        engine = create_engine(db_url)
        sql_folder = get_sql_folder(engine)
        try:  
            for sql_file in sql_folder.glob("*.sql"):  
                run_query(sql_file, engine)  
  
            print("\n--------------------")  
            print("Analysis Phase Complete")  
            print("--------------------\n")  
  
        except Exception as e:  
            print(f"Analysis Failed: {e}")  
            return
    # -------------------  
    # CHART PHASE
    # ------------------- 
    if (args.mode in ["chart", "full"]):
        engine = create_engine(db_url)
        try:
            if engine is not None:
                generate_all_charts(engine)
                print("\n--------------------")  
                print("Charting Phase Complete")  
                print("--------------------\n")  
            else:
                print("Chart generation skipped: no database engine available.")
                return
            
        except Exception as e:  
            print(f"Chart Generation Failed: {e}")  
            return
    # -------------------  
    # DASHBOARD PHASE
    # ------------------- 
    if (args.mode in ["dashboard", "full"]): 
        engine = create_engine(db_url)
        try:
            if engine is not None:
                excel_dashboard(engine)
            print("\n--------------------")  
            print("Dashboard Phase Complete")  
            print("--------------------\n")  
        except Exception as e:
            print(f"Dashboard Phase Failed: {e}")  
            return

if __name__ == "__main__":  
    main()  
#EOF