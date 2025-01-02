import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("eCommerce Dashboard")

# Display orders per customer
st.header("Orders per Customer")

# Fetch data from FastAPI endpoint
response = requests.get("http://127.0.0.1:8000/kpi/orders-per-customer")
if response.status_code == 200:
    data = response.json()["data"]
    df = pd.DataFrame(data)
    # Display the DataFrame
    st.dataframe(df)
    # Create a Plotly bar chart
    fig = px.bar(df, x="_id", y="total_orders",
                 labels={"_id": "Customer ID", "total_orders": "Total Orders"},
                 title="Total Orders per Customer",
                 color="total_orders",  # Color bars based on total orders
                 color_continuous_scale="Viridis")  # Choose a color scale
    # Display the Plotly chart
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Error loading Orders per Customer data.")
