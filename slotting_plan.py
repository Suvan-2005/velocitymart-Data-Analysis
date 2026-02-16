import pandas as pd

# =====================================================
# LOAD DATA
# =====================================================

sku = pd.read_csv(r"C:\Users\Suvan\Downloads\sku_after_forensics.csv")
warehouse = pd.read_excel(r"C:\Users\Suvan\Downloads\warehouse_constraints.xlsx")

# =====================================================
# MERGE SKU WITH CURRENT SLOT DETAILS
# =====================================================
# Adds slot temperature and weight capacity info
# to each SKU

sku = sku.merge(
    warehouse,
    left_on="current_slot",
    right_on="slot_id",
    how="left",
    suffixes=("", "_slot")
)

# =====================================================
# IDENTIFY DATA-DRIVEN HEAVY SKUs
# =====================================================
# Heavy is defined relative to the dataset

heavy_weight_cutoff = sku["weight_kg"].quantile(0.9)

# =====================================================
# IDENTIFY SKUs THAT NEED TO MOVE
# =====================================================
# A SKU is moved if:
# 1. Temperature mismatch (hard violation)
# 2. It is unusually heavy (top-end weight)

sku["needs_move"] = (
    (sku["temp_req"] != sku["temp_zone"]) |
    (sku["weight_kg"] >= heavy_weight_cutoff)
)

candidates = sku[sku["needs_move"]].copy()

# =====================================================
# FIND SAFE TARGET SLOTS
# =====================================================

moves = []

for _, row in candidates.iterrows():

    # Slot must satisfy HARD constraints
    valid_slots = warehouse[
        (warehouse["temp_zone"] == row["temp_req"]) &
        (warehouse["max_weight_kg"] >= row["weight_kg"])
    ]

    # If no safe slot exists, do not move
    if valid_slots.empty:
        continue

    # Pick the first valid safe slot
    new_slot = valid_slots.iloc[0]["slot_id"]

    moves.append({
        "sku_id": row["sku_id"],
        "new_slot": new_slot
    })

moves_df = pd.DataFrame(moves)

# =====================================================
# BUILD FINAL SLOT MAP
# =====================================================
# SKUs not in moves_df stay in their current slot

final_plan = sku[["sku_id", "current_slot"]].merge(
    moves_df,
    on="sku_id",
    how="left"
)

final_plan["Bin_ID"] = final_plan["new_slot"].fillna(
    final_plan["current_slot"]
)

# =====================================================
# OUTPUT
# =====================================================

final_plan = final_plan.rename(
    columns={"sku_id": "SKU_ID"}
)

final_plan = final_plan[["SKU_ID", "Bin_ID"]]

# =====================================================
# SAVE FINAL CSV
# =====================================================

final_plan.to_csv(
    r"C:\Users\Suvan\Downloads\final_slotting_plan.csv",
    index=False
)

print("✅ final_slotting_plan.csv generated successfully")
print("Total SKUs moved:", len(moves_df))


print("final_slotting_plan.csv generated successfully")
print("Total SKUs moved:", len(moves_df))                   