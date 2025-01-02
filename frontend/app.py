import streamlit as st
import requests
import pandas as pd

st.title("eCommerce Dashboard")

response = requests.get("http://127.0.0.1:8000/kpi/orders-per-customer")
if response.status_code == 200:
    data = response.json()["data"]
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("_id")["total_orders"])
else:
    st.error("Error loading data")
