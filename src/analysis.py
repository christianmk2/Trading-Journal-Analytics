#analysis.py
import pandas as pd  
from sqlalchemy import create_engine  
from pathlib import Path

from settings.paths import OUTPUT_DIR
   
def run_query(sql_file, engine):  
    OUTPUT_DIR.mkdir(exist_ok=True)  
    # -------------------  
    # LOAD SQL QUERY  
    # -------------------  
    with open(sql_file, "r", encoding="utf-8") as file:  
        query = file.read()
    # -------------------  
    # EXECUTE QUERY  
    # -------------------  
    result_df = pd.read_sql(  
        query,  
        engine  
    )  
    # -------------------  
    # SAVE RESULT  
    # -------------------  

    query_name = Path(sql_file).stem.lower()
    csv_file = OUTPUT_DIR / (query_name + ".csv")
    #csv
    print(csv_file)
    result_df.to_csv(  
        csv_file,  
        index=False,
        encoding="utf-8"  
    ) 
    #sqlite db
    result_df.to_sql(
        query_name,
        engine,
        if_exists='replace',
        index=False
    )
#EOF
