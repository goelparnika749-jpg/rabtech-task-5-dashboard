
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Business KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interactive Business KPI Dashboard")
st.caption("Rabtech Academy | Task 5 | Simulated Sales Data")

df = pd.read_csv("sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("Dashboard Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

start_date = st.sidebar.date_input(
    "Start Date", df["Date"].min().date()
)
end_date = st.sidebar.date_input(
    "End Date", df["Date"].max().date()
)

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

filtered = df[
    df["Category"].isin(categories)
    & df["Region"].isin(regions)
    & (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
]

if filtered.empty:
    st.warning("No data found. Change your filters.")
    st.stop()

revenue = filtered["Revenue"].sum()
orders = filtered["Order_ID"].nunique()
customers = filtered["Customer_ID"].nunique()
marketing = filtered["Marketing_Cost"].sum()
cac = marketing / customers if customers else 0
aov = revenue / orders if orders else 0

customer_status = (
    filtered[["Customer_ID", "Churned"]]
    .drop_duplicates("Customer_ID")
)
churn_rate = (
    customer_status["Churned"].mean() * 100
    if len(customer_status) else 0
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Customer Acquisition Cost", f"₹{cac:,.2f}")
c3.metric("Customer Churn Rate", f"{churn_rate:.1f}%")
c4.metric("Average Order Value", f"₹{aov:,.2f}")

st.divider()

st.subheader("Revenue Trend Over Time")
trend = (
    filtered.groupby("Date", as_index=False)["Revenue"]
    .sum()
    .sort_values("Date")
)
fig = px.area(
    trend, x="Date", y="Revenue",
    title="Daily Revenue Trend"
)
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    cat = filtered.groupby(
        "Category", as_index=False
    )["Revenue"].sum()
    fig2 = px.bar(
        cat, x="Category", y="Revenue",
        color="Category"
    )
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.subheader("Regional Sales")
    reg = filtered.groupby(
        "Region", as_index=False
    )["Revenue"].sum()
    fig3 = px.bar(
        reg, x="Region", y="Revenue",
        color="Region"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Sales Data Table")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Filtered Data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.caption(
    "Note: This dashboard uses simulated data for educational purposes."
)
