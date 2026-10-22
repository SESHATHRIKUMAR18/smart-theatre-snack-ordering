
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Smart Theatre Dashboard",
    page_icon="🍿"
)

st.title("🍿 Smart Theatre Order Dashboard")

if os.path.exists("orders.csv"):
    orders = pd.read_csv("orders.csv")

    # Fix old or missing columns
    for column in ["Order ID", "Seat Number", "Snacks", "Amount", "Status"]:
        if column not in orders.columns:
            orders[column] = ""

    # Remove empty rows and fill missing values
    orders = orders.dropna(how="all")
    orders["Snacks"] = orders["Snacks"].fillna("Details unavailable")
    orders["Status"] = orders["Status"].fillna("Pending")
    orders["Status"] = orders["Status"].replace("", "Pending")

    # Display columns in the correct order
    orders = orders[
        ["Order ID", "Seat Number", "Snacks", "Amount", "Status"]
    ]
    
    # Dashboard summary cards
    total_orders = len(orders)
    total_revenue = pd.to_numeric(
        orders["Amount"], errors="coerce"
    ).sum()

    pending_orders = (orders["Status"] == "Pending").sum()
    prepared_orders = (orders["Status"] == "Prepared").sum()

    col1, col2 = st.columns(2)

    col1.metric("🛍️ Total Orders", total_orders)
    col2.metric("💰 Total Revenue", f"₹{total_revenue:.0f}")

    col3, col4 = st.columns(2)

    col3.metric("⏳ Pending Orders", pending_orders)
    col4.metric("✅ Prepared Orders", prepared_orders)

    st.subheader("All Orders")
    st.dataframe(orders, use_container_width=True)

    st.subheader("Update Order Status")

    if not orders.empty:
        order_ids = orders["Order ID"].dropna().astype(str).unique().tolist()

        selected_order = st.selectbox(
            "Select Order ID",
            order_ids
        )

        status = st.selectbox(
            "Choose Status",
            ["Pending", "Preparing", "Prepared"]
        )

        if st.button("Save Status"):
            orders.loc[
                orders["Order ID"].astype(str) == selected_order,
                "Status"
            ] = status

            orders.to_csv("orders.csv", index=False)
            st.success("Order status saved!")
            st.rerun()
else:
    st.info("No orders have been placed yet.")
