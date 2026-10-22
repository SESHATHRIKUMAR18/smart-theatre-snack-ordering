
import streamlit as st
import uuid
import csv
import os
import pandas as pd
st.set_page_config(
    page_title="Smart Theatre",
    page_icon="🍿"
)
orders_file="orders.csv"

st.title("🍿 Smart Theatre Snack Ordering")
st.write("Order your favourite snacks before the movie interval!")

st.subheader("🍟 Snack Menu")

snacks = {
    "Popcorn": 150,
    "Burger": 120,
    "Pizza": 180,
    "Soft Drink": 80,
    "French Fries": 100
}

total = 0

for snack, price in snacks.items():
    quantity = st.number_input(
        f"{snack} - ₹{price}",
        min_value=0,
        max_value=10,
        value=0,
        key=snack
    )
    total += (quantity * price)

st.divider()

st.subheader(f"Total Amount: ₹{total}")

seat = st.text_input("Enter your seat number")

if st.button("Confirm Order"):
    if total == 0:
        st.warning("Please select at least one snack.")
    elif not seat.strip():
        st.warning("Please enter your seat number.")
    else:
        #importing order id
        order_id = "ORD-" + uuid.uuid4().hex[:8].upper()
        ordered_snacks = []

        for snack, price in snacks.items():
            quantity = st.session_state[snack]
            if quantity > 0:
                ordered_snacks.append(f"{snack} x {quantity}")

        order_data = {
    "Order ID": order_id,
    "Seat Number": seat,
    "Amount": total,
    "Snacks": ", ".join(ordered_snacks),
    "Status": "Pending"
}
        
        # Read existing orders and update the CSV columns safely
        if os.path.isfile(orders_file):
            old_orders = pd.read_csv(orders_file)
        else:
            old_orders = pd.DataFrame()

        new_order = pd.DataFrame([order_data])

        all_orders = pd.concat(
            [old_orders, new_order],
            ignore_index=True
        )

        all_orders.to_csv(orders_file, index=False)
        st.success("Your order has been confirmed!")
        st.subheader(f"Order ID: {order_id}")
        st.write(f"Seat Number: {seat}")
        st.write(f"Amount: ₹{total}")
        st.info("Demo only — no real payment has been made.")
