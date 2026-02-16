import pandas as pd

# =====================================================
# LOAD DATASETS (CORRECTED PATHS)
# =====================================================

sku = pd.read_csv(r"C:\Users\Suvan\Downloads\sku_master.csv")
warehouse = pd.read_excel(r"C:\Users\Suvan\Downloads\warehouse_constraints.xlsx")
movement = pd.read_csv(r"C:\Users\Suvan\Downloads\picker_movement.csv")
orders = pd.read_csv(r"C:\Users\Suvan\Downloads\order_transactions.csv")

# =====================================================
# 1️⃣ DECIMAL DRIFT DETECTION & HANDLING
# =====================================================

# Step 1: Compute normal (median) weight per category
category_median = sku.groupby("category")["weight_kg"].median()
sku["category_median"] = sku["category"].map(category_median)

# Step 2: Compare SKU weight to category normal
sku["weight_ratio"] = sku["weight_kg"] / sku["category_median"]

# Step 3: Detect SAFE 10x unit-scale errors
sku["decimal_drift_flag"] = sku["weight_ratio"].between(8, 12)

# Step 4: Detect EXTREME corruption (unsafe to guess)
sku["corrupt_weight_flag"] = sku["weight_ratio"] > 20

# Step 5: Correct only the safe decimal drift cases
sku.loc[sku["decimal_drift_flag"], "weight_kg"] = (
    sku.loc[sku["decimal_drift_flag"], "weight_kg"] / 10
)

# =====================================================
# 2️⃣ SHORTCUT PARADOX — PICKER BEHAVIOR FORENSICS
# =====================================================

avg_picker_distance = (
    movement.groupby("picker_id")["travel_distance_m"]
    .mean()
)

median_picker_distance = avg_picker_distance.median()
picker_distance_ratio = avg_picker_distance / median_picker_distance

shortcut_picker_flag = picker_distance_ratio < 0.6
suspicious_pickers = avg_picker_distance[shortcut_picker_flag]

# =====================================================
# 3️⃣ GHOST INVENTORY DETECTION
# =====================================================

sku["ghost_inventory_flag"] = ~sku["current_slot"].isin(
    warehouse["slot_id"]
)

ghost_inventory = sku[sku["ghost_inventory_flag"]]

# =====================================================
# OUTPUT SUMMARY
# =====================================================

print("========== DATA FORENSICS SUMMARY ==========")
print("Decimal Drift (10x) SKUs corrected:", sku["decimal_drift_flag"].sum())
print("Corrupt Weight SKUs flagged:", sku["corrupt_weight_flag"].sum())
print("Ghost Inventory SKUs:", sku["ghost_inventory_flag"].sum())

print("\nSuspicious Shortcut Pickers:")
print(suspicious_pickers)

# =====================================================
# SAVE OUTPUT FILES
# =====================================================

sku.to_csv(r"C:\Users\Suvan\Downloads\sku_after_forensics.csv", index=False)
suspicious_pickers.to_csv(r"C:\Users\Suvan\Downloads\suspicious_pickers.csv")
ghost_inventory.to_csv(r"C:\Users\Suvan\Downloads\ghost_inventory.csv", index=False)
