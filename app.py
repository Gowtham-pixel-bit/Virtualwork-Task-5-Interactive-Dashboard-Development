import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("data/business_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Dashboard Title
st.title("📊 Business Analytics Dashboard")
st.markdown("### Interactive Business Performance Analysis")

st.divider()

# Sidebar Filters
st.sidebar.title("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

departments = st.sidebar.multiselect(
    "Select Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

products = st.sidebar.multiselect(
    "Select Product",
    df["Product"].unique(),
    default=df["Product"].unique()
)

# Filter Data
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Department"].isin(departments)) &
    (df["Product"].isin(products))
]

# KPI Metrics
st.subheader("Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Orders"].sum()

average_sales = (
    filtered_df["Sales"].mean()
    if not filtered_df.empty else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Average Sales", f"₹{average_sales:,.0f}")

st.divider()

# Monthly Sales
st.subheader("📈 Monthly Sales Trends")

if not filtered_df.empty:
    monthly_sales = (
        filtered_df.groupby(filtered_df["Date"].dt.month)["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Month"] = monthly_sales["Date"].map(
        lambda x: pd.Timestamp(2026, int(x), 1).strftime("%B")
    ) if "Date" in monthly_sales.columns else monthly_sales.iloc[:, 0].map(
        lambda x: pd.Timestamp(2026, int(x), 1).strftime("%B")
    )

    fig1 = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Revenue"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Regional and Department Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Regional Performance")

    if not filtered_df.empty:
        regional = filtered_df.groupby("Region")["Sales"].sum().reset_index()

        fig2 = px.bar(
            regional,
            x="Region",
            y="Sales",
            color="Region",
            title="Sales by Region"
        )

        st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("🏢 Department Performance")

    if not filtered_df.empty:
        department = filtered_df.groupby(
            "Department"
        )["Sales"].sum().reset_index()

        fig3 = px.pie(
            department,
            names="Department",
            values="Sales",
            title="Department-wise Sales"
        )

        st.plotly_chart(fig3, use_container_width=True)

# Product Analysis
st.subheader("📦 Product Performance")

if not filtered_df.empty:
    product = filtered_df.groupby("Product")["Sales"].sum().reset_index()

    fig4 = px.bar(
        product,
        x="Product",
        y="Sales",
        color="Product",
        title="Product-wise Sales"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Data Table
st.subheader("📋 Business Sales Records")

st.dataframe(filtered_df, use_container_width=True)

# Download Button
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.success("Dashboard Loaded Successfully!")