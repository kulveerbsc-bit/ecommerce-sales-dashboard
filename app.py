import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Load data
df = pd.read_csv("data/ecommerce_sales (2).csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# -----------------------------
# Title
# -----------------------------
st.title("🛒 E-Commerce Sales & Profit Dashboard")
st.caption("Interactive sales, profit and customer insights")

# -----------------------------
# Category Filter
# -----------------------------
category = st.selectbox(
    "Category",
    ["All Categories"] + sorted(df["Category"].unique().tolist())
)

if category != "All Categories":
    filtered_df = df[df["Category"] == category]
else:
    filtered_df = df.copy()

# -----------------------------
# KPI Calculations
# -----------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "🧾 Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "💹 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

# -----------------------------
# Monthly Sales & Profit
# -----------------------------
st.subheader("📊 Monthly Sales & Profit Trend")

monthly = (
    filtered_df
    .groupby(filtered_df["Order_Date"].dt.to_period("M"))
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

monthly["Order_Date"] = monthly["Order_Date"].astype(str)

st.line_chart(
    monthly.set_index("Order_Date")[["Sales", "Profit"]]
)

# -----------------------------
# Category Profit
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏷️ Profit by Category")

    category_profit = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_profit)

# -----------------------------
# City Sales
# -----------------------------
with col2:
    st.subheader("🏙️ Sales by City")

    city_sales = (
        filtered_df
        .groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(city_sales)

# -----------------------------
# Payment Method
# -----------------------------
st.subheader("💳 Sales by Payment Method")

payment_sales = (
    filtered_df
    .groupby("Payment_Mode")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(payment_sales)

# -----------------------------
# Top 10 Products
# -----------------------------
st.subheader("🏆 Top 10 Products by Profit")

top_products = (
    filtered_df
    .groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# -----------------------------
# Data Table
# -----------------------------
with st.expander("📋 View Sales Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

st.caption("E-Commerce Sales & Profit Analyzer | Built with Python + Streamlit")