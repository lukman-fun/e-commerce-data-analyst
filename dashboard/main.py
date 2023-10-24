import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from geobr import read_state
import geopandas as gpd
from transaction_func import TransactionFunc

# OPTIONS
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# LOAD TRANSACTION DATASETS
datetime_columns = ['order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date', 'order_purchase_timestamp', 'shipping_limit_date']
all_df = pd.read_csv('../data/all_data.csv')
all_df.sort_values(by='order_approved_at', inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# LOAD GEOLOCATION DATASETS
geolocations_df = pd.read_csv('../data/customer_geo.csv')
geolocations_df.drop_duplicates(subset='customer_unique_id')

# MIN & MAX DATE
min_date = all_df['order_approved_at'].min()
max_date = all_df['order_approved_at'].max()


# SIDEBAR STREAMLIT
with st.sidebar:
    st.image('logo.png')

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# MAIN DATA
main_df = all_df[(all_df['order_approved_at'] >= str(start_date)) & (all_df['order_approved_at'] <= str(end_date))]

# CALL FUNCTION TRANSACTION
transaction = TransactionFunc(main_df)

daily_order_and_revenue_df = transaction.create_daily_order_and_revenue_df()
product_best_and_worst_df = transaction.create_product_best_and_worst_df()
customer_demographic_bystate_df = transaction.create_customer_demographic_bystate_df()
customer_demographic_bycity_df = transaction.create_customer_demographic_bycity_df()
customer_order_status_df = transaction.create_customer_order_status_df()
customer_spend_money_df = transaction.create_customer_spend_money_df()
review_score_df = transaction.create_review_score_df()

# HEADER
st.header('Brasil E-Commerce Dashboard :sparkles:')
st.caption('Copyright © Moh.Lukman Hakim')

# DAILY ORDERS 
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_order_and_revenue_df.order_count.sum()
    st.metric('Total Orders', value=total_orders)

with col2:
    total_revenue = format_currency(daily_order_and_revenue_df.revenue.sum(), 'BRL', locale='pt_BR')
    st.metric('Total Revenue', value=total_revenue)

tab1, tab2 = st.tabs(['Orders Chart', 'Revenue Chart'])

with tab1:
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.plot(
        daily_order_and_revenue_df['order_approved_at'],
        daily_order_and_revenue_df['order_count'],
        marker='o', 
        linewidth=2,
        color='#90CAF9'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.plot(
        daily_order_and_revenue_df['order_approved_at'],
        daily_order_and_revenue_df['revenue'],
        marker='o', 
        linewidth=2,
        color='#90CAF9'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    
    st.pyplot(fig)

# BEST & WORST PRODUCTS
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(
    x="total_quantity", 
    y="category_name", 
    data=product_best_and_worst_df.head(5), 
    palette=colors, ax=ax[0]
    )
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(
    x="total_quantity", 
    y="category_name", 
    data=product_best_and_worst_df.sort_values(by="total_quantity", ascending=True).head(5), 
    palette=colors, 
    ax=ax[1]
    )
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

# CUSTOMER DEMOGRAPHIC
st.subheader("Customer Demographics")

tab1, tab2 = st.tabs(['State', 'City'])

with tab1:
    colors = ["#72BCD4" if state == customer_demographic_bystate_df['customer_state'][0] else "#D3D3D3" for state in customer_demographic_bystate_df['customer_state']]
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        data=customer_demographic_bystate_df,
        x='customer_state',
        y='customer_count',
        palette=colors
    )
    plt.title("Number customers from State", fontsize=15)
    plt.xlabel("State")
    plt.ylabel("Number of Customers")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

with tab2:
    colors = ["#72BCD4" if city == customer_demographic_bycity_df['customer_city'][0] else "#D3D3D3" for city in customer_demographic_bycity_df['customer_city']]
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        data=customer_demographic_bycity_df.head(5),
        x='customer_city',
        y='customer_count',
        palette=colors
    )
    plt.title("Number customers by City", fontsize=15)
    plt.xlabel("City")
    plt.ylabel("Number of Customers")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

# CUSTOMER SPEND MONEY
st.subheader("Customer Spend Money")

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data = customer_spend_money_df.head(5),
    x='price',
    y='customer_id',
    palette=colors
)

plt.ylabel(None)
plt.xlabel(None)
plt.title("Total customer spend money", loc="center", fontsize=18)
plt.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# CUSTOMER REVIEW SCORE & STATUS ORDER
st.subheader("Customer Happy Level")

tab1, tab2 = st.tabs(['Review Score', 'Status Order'])

with tab1:
    colors = ["#72BCD4" if revscore == review_score_df['review_score'][0] else "#D3D3D3" for revscore in review_score_df['review_score']]
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        data=review_score_df,
        x='review_score',
        y='customer_count',
        order=review_score_df.review_score,
        palette=colors
    )
    plt.title("Rating by customers", fontsize=15)
    plt.xlabel("Rating")
    plt.ylabel("Number Customers")
    plt.xticks(fontsize=10)

    st.pyplot(fig)

with tab2:
    colors = ["#72BCD4" if orderstatus == customer_order_status_df['order_status'][0] else "#D3D3D3" for orderstatus in customer_order_status_df['order_status']]
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        data=customer_order_status_df,
        x='order_status',
        y='customer_count',
        palette=colors
    )
    plt.title("Number customers by Order Status", fontsize=15)
    plt.xlabel("Order Status")
    plt.ylabel("Number Customers")
    plt.xticks(fontsize=10)

    st.pyplot(fig)

# GEOLOCATION
st.subheader("Customer Geolocation")

fig, ax = plt.subplots(figsize=(10, 10))

mun = read_state(year=2020)
mun.plot(ax=ax, color='white', edgecolor='black')

gdf = gpd.GeoDataFrame(
    geolocations_df,
    geometry=gpd.points_from_xy(geolocations_df['geolocation_lng'], geolocations_df['geolocation_lat'])
    )
gdf.plot(ax=ax, color='red', marker='o', markersize=5)

st.pyplot(fig)