import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///trading_journal.db"
)

daily = pd.read_sql(
    "SELECT * FROM daily_pnl",
    engine
)

st.line_chart(
    daily.set_index("trade_day")["daily_pnl"]
)