import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="NovaRetail Dashboard", layout="wide")

st.title("📊 NovaRetail Customer Intelligence Dashboard")
st.markdown("Interactive decision-support dashboard for revenue optimization and customer retention.")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("NR_dataset.xlsx")
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filter Data")

segments = st.sidebar.multiselect("Customer Segment", df['label'].unique(), default=df['label'].unique())
regions = st.sidebar.multiselect("Region", df['CustomerRegion'].unique(), default=df['CustomerRegion'].unique())
categories = st.sidebar.multiselect("Product Category", df['ProductCategory'].unique(), default=df['ProductCategory'].unique())
channels = st.sidebar.multiselect("Retail Channel", df['RetailChannel'].unique(), default=df['RetailChannel'].unique())

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['TransactionDate'].min(), df['TransactionDate'].max()]
)

# Apply filters
filtered_df = df[
    (df['label'].isin(segments)) &
    (df['CustomerRegion'].isin(regions)) &
    (df['ProductCategory'].isin(categories)) &
    (df['RetailChannel'].isin(channels)) &
    (df['TransactionDate'] >= pd.to_datetime(date_range[0])) &
    (df['TransactionDate'] <= pd.to_datetime(date_range[1]))
]

# -----------------------------
# KPIs
# -----------------------------
total_revenue = filtered_df['PurchaseAmount'].sum()
total_customers = filtered_df['CustomerID'].nunique()
avg_purchase = filtered_df['PurchaseAmount'].mean()
avg_satisfaction = filtered_df['CustomerSatisfaction'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Unique Customers", total_customers)
col3.metric("Avg Purchase Value", f"${avg_purchase:,.2f}")
col4.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}")

# -----------------------------
# Revenue by Segment
# -----------------------------
st.subheader("Revenue by Customer Segment")
seg_rev = filtered_df.groupby('label')['PurchaseAmount'].sum().reset_index()
fig1 = px.bar(seg_rev, x='label', y='PurchaseAmount', color='label')
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Revenue Trend
# -----------------------------
st.subheader("Revenue Trend Over Time")
trend = filtered_df.groupby(['TransactionDate','label'])['PurchaseAmount'].sum().reset_index()
fig2 = px.line(trend, x='TransactionDate', y='PurchaseAmount', color='label')
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Growth Opportunities
# -----------------------------
st.header("🚀 Growth Opportunities")

cat_rev = filtered_df.groupby('ProductCategory')['PurchaseAmount'].sum().reset_index()
fig3 = px.bar(cat_rev, x='ProductCategory', y='PurchaseAmount')
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Early Warning Signals
# -----------------------------
st.header("⚠ Early Warning Signals")

decline_df = filtered_df[filtered_df['label'] == 'Decline']
decline_trend = decline_df.groupby('TransactionDate')['PurchaseAmount'].sum().reset_index()
fig4 = px.line(decline_trend, x='TransactionDate', y='PurchaseAmount')
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.scatter(filtered_df, x='CustomerSatisfaction', y='PurchaseAmount', color='label')
st.plotly_chart(fig5, use_container_width=True)
