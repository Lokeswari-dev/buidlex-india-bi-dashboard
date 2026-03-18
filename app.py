import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Buildex India Analytics",
    page_icon="🏗️",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data():
    if not os.path.exists('buildex_data.csv'):
        return None
    df = pd.read_csv('buildex_data.csv')
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    return df

df = load_data()

if df is None:
    st.error("⚠️ Data file `buildex_data.csv` not found. Please run `generate_data.py` first.")
    st.stop()

# --- Application Header ---
st.title("🏗️ Buildex India - Data Analytics Dashboard")
st.markdown("Overview of construction material sales, revenue operations, and order tracking.")
st.divider()

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")

# Location Filter
locations = ['All'] + list(df['Location'].unique())
selected_location = st.sidebar.selectbox("Select Location", locations)

# Material Filter
materials = ['All'] + list(df['MaterialName'].unique())
selected_material = st.sidebar.selectbox("Select Material Name", materials)

# Apply Filters
filtered_df = df.copy()
if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['Location'] == selected_location]
if selected_material != 'All':
    filtered_df = filtered_df[filtered_df['MaterialName'] == selected_material]

# --- KPI Cards ---
total_revenue = filtered_df['TotalRevenue'].sum()
total_pending = filtered_df[filtered_df['PaymentStatus'] == 'Pending']['TotalRevenue'].sum()
total_orders = len(filtered_df)
average_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"₹ {total_revenue / 1000000:.1f}M")
with col2:
    st.metric("Total Pending Revenue", f"₹ {total_pending / 1000000:.1f}M")
with col3:
    st.metric("Total Orders", f"{total_orders:,}")
with col4:
    st.metric("Average Order Value (AOV)", f"₹ {average_order_value:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# --- Visualizations ---
col_charts1, col_charts2 = st.columns(2)

with col_charts1:
    # Bar Chart: Revenue by Material
    st.subheader("Revenue by Material")
    rev_by_material = filtered_df.groupby(['MaterialName', 'PaymentStatus'])['TotalRevenue'].sum().reset_index()
    fig_bar = px.bar(
        rev_by_material, 
        x='MaterialName', 
        y='TotalRevenue',
        color='PaymentStatus',
        text_auto='.2s',
        title="Total Revenue per Material Type",
        color_discrete_map={
            'Paid': '#2ecc71', 
            'Pending': '#e74c3c', 
            'Partial': '#f1c40f'
        }
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_charts2:
    # Donut Chart: Payment Status
    st.subheader("Payment Status Distribution")
    payment_counts = filtered_df['PaymentStatus'].value_counts().reset_index()
    payment_counts.columns = ['PaymentStatus', 'Count']
    
    fig_donut = px.pie(
        payment_counts, 
        names='PaymentStatus', 
        values='Count',
        hole=0.4,
        color='PaymentStatus',
        color_discrete_map={
            'Paid': '#2ecc71', 
            'Pending': '#e74c3c', 
            'Partial': '#f1c40f'
        },
        title="Paid vs Pending vs Partial statuses"
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# Map/City-wise Bar Chart: Sales by Location
st.subheader("Sales by Location (City-wise Revenue)")
sales_by_loc = filtered_df.groupby('Location')['TotalRevenue'].sum().reset_index()
sales_by_loc = sales_by_loc.sort_values(by='TotalRevenue', ascending=False)
fig_loc = px.bar(
    sales_by_loc,
    x='Location',
    y='TotalRevenue',
    color='Location',
    text_auto='.2s',
    title="City-wise Sales Performance"
)
st.plotly_chart(fig_loc, use_container_width=True)

# --- Raw Data ---
with st.expander("View Raw Data"):
    st.dataframe(filtered_df.style.format({
        "UnitPrice": "₹{:,.2f}",
        "TotalRevenue": "₹{:,.2f}"
    }), use_container_width=True)
