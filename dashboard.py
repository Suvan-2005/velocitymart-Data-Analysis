import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------
# LOAD DATA (CORRECTED PATHS)
# ----------------------------------------

sku = pd.read_csv(r"C:\Users\Suvan\Downloads\sku_after_forensics.csv")
orders = pd.read_excel(r"C:\Users\Suvan\Downloads\order_transactions.xlsx")   # has order_hour
movement = pd.read_excel(r"C:\Users\Suvan\Downloads\picker_movement.xlsx")    # has hour
warehouse = pd.read_excel(r"C:\Users\Suvan\Downloads\warehouse_constraints.xlsx")

st.title("VelocityMart – Decision Support Dashboard")

# =====================================================
# 1️⃣ PROVE PEAK TRAFFIC (ORDER VOLUME BY HOUR)
# =====================================================

st.header("Order Traffic by Hour (Peak Window Identification)")

orders_per_hour = (
    orders.groupby("order_hour")
    .size()
    .reset_index(name="order_count")
)

plt.figure(figsize=(8,4))
sns.lineplot(
    data=orders_per_hour,
    x="order_hour",
    y="order_count",
    marker="o"
)
plt.xlabel("Hour of Day")
plt.ylabel("Number of Orders")
plt.title("Order Volume by Hour")

st.pyplot(plt)

st.write(
    "Order volume peaks between 19:00 and 20:00, "
    "defining the operational stress window."
)

# =====================================================
# 2️⃣ HIGH-COLLISION AISLES @ 19:00
# =====================================================

st.header("High-Collision Aisles at 19:00 (Peak Hour Deep Dive)")

peak_movement = movement[movement["hour"] == 19]

aisle_congestion = (
    peak_movement.groupby("aisle_id")
    .size()
    .reset_index(name="movement_count")
)

plt.figure(figsize=(8,4))
sns.barplot(
    data=aisle_congestion,
    x="aisle_id",
    y="movement_count",
    palette="Reds"
)
plt.xlabel("Aisle")
plt.ylabel("Picker Movements")
plt.title("Picker Congestion by Aisle (19:00)")

st.pyplot(plt)

st.write(
    "Aisle B shows the highest picker density during the peak hour, "
    "indicating elevated collision risk."
)

# =====================================================
# 3️⃣ SPOILAGE RISK – TEMPERATURE VIOLATIONS
# =====================================================

st.header("Spoilage Risk – Temperature Constraint Violations")

temp_violations = sku[sku["temp_violation"] == True]

st.metric(
    label="SKUs at Spoilage Risk",
    value=len(temp_violations)
)

st.write("Example SKUs violating temperature constraints:")
st.dataframe(
    temp_violations[["sku_id", "temp_req", "temp_zone"]].head(10)
)

# =====================================================
# 4️⃣ FORKLIFT DEAD-ZONE – UNSPOKEN PHYSICS
# =====================================================

st.header("Forklift Dead-Zone – Aisle B (Unspoken Physics)")

aisle_b_peak = peak_movement[
    peak_movement["aisle_id"] == "B"
]

picker_count_b = aisle_b_peak["picker_id"].nunique()

if picker_count_b > 2:
    st.error(
        f"Forklift BLOCKED in Aisle B "
        f"(Pickers present: {picker_count_b})"
    )
else:
    st.success(
        "Forklift can safely operate in Aisle B"
    )

st.write(
    "Operational rule: Forklifts cannot enter Aisle B "
    "if more than two pickers are present. "
    "Peak-hour congestion frequently violates this rule."
)
