import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO


order_payment_df = pd.read_csv(r'C:\Users\WINDOWS 11\Documents\submission\data\order_payments_dataset.csv')
products_df = pd.read_csv(r'C:\Users\WINDOWS 11\Documents\submission\data\products_dataset.csv')

def create_payment_value_df(df):
    # Assuming order_id uniquely identifies each order
    payment_value_df = df.groupby('order_id').agg({
        "payment_value": "sum",  # Calculate total payment value per order
        "payment_type": "nunique"  # Assuming you want the number of unique payment types per order
    })
    payment_value_df = payment_value_df.reset_index()
    payment_value_df.rename(columns={
        "payment_value": "revenue",
        "payment_type": "unique_payment_types"  # Adjust column names as needed
    }, inplace=True)

    # Calculate total revenue across all orders
    total_revenue = payment_value_df['revenue'].sum()

    return payment_value_df, total_revenue  # Return both the DataFrame and total revenue

# Call the function with order_payment_df
payment_value_df, total_revenue = create_payment_value_df(order_payment_df)

# Display the total revenue
st.metric(label=" Total Revenue : ", value=total_revenue)

# Create separate charts for each dataset
st.title("Order Payment")
st.subheader("Grafik Payment type")

# Payment chart
payment_chart = sns.countplot(x='payment_type', data=order_payment_df)
image_stream = BytesIO()
payment_chart.figure.savefig(image_stream, format='png', bbox_inches='tight')
st.image(image_stream, width=800)

st.title("Product")
st.subheader("Grafik Product category")

# Product chart
fig, ax = plt.subplots(figsize=(16, 6))
product_chart = sns.countplot(x='product_category_name', hue='product_category_name', data=products_df, palette='viridis', order=products_df['product_category_name'].value_counts().index, legend=False, ax=ax)
plt.xticks(rotation=70, ha='right')
plt.title('Distribusi Penjualan Berdasarkan Kategori Produk')
plt.xlabel('Kategori Produk')
plt.ylabel('Jumlah Penjualan')

image_stream = BytesIO()
fig.savefig(image_stream, format='png', bbox_inches='tight')
st.image(image_stream, width=1000)


