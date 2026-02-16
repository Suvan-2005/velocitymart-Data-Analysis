# VelocityMart Chaos Rescue 🚀  - A Data Analysis Project


# 📌 Problem Overview

VelocityMart’s Bangalore dark stores are experiencing severe operational degradation:

- ⏱️ Fulfillment time increased from **3.8 → 6.2 minutes**
- ⚠️ Safety incidents rising (picker collisions, product damage)
- ❄️ Spoilage risk due to temperature misallocation
- 🚧 Hidden physical constraints affecting operations

My mission was to:

1. Perform deep **Data Forensics & Integrity validation**
2. Build an **Interactive Decision-Support Dashboard**
3. Design a mathematically optimized **Strategic Slotting Plan (Week 91)**

---

# 🧠 Project Structure

```
velocitymart-Data-Analysis/
│
├── Data_Forensics.py          # Cleaning & anomaly detection
├── dashboard.py               # Tableau dashboard
├── slotting_plan.py           # Optimization logic
├── final_slotting_plan.csv    # Week 91 optimized bin assignments
├── Report.pdf                 # Detailed strategic memo
├── tableau_dashboard.twbx     # Tableau interactive dashboard
├── dashboard_preview.pdf      # Dashboard screenshots
└── README.md
```

---

# 🔍 A. Data Forensics & Integrity

We treated data errors as **system failures**, not random noise.

### 1️⃣ Decimal Drift Detection
- Identified SKUs whose weights were inflated ~10× due to unit errors.
- Corrected using category-level median ratio logic.
- Preserved data integrity instead of deleting rows.

### 2️⃣ Shortcut Paradox
- Compared actual picker travel distance vs. expected path distance.
- Flagged pickers whose efficiency was artificially inflated.
- Identified suspicious behavior (e.g., PICKER-07).

### 3️⃣ Ghost Inventory
- Cross-validated SKU current_slot against warehouse topology.
- Ensured no SKU assigned to non-existent bins.

---

# 📊 B. Decision-Support Dashboard

Built using **Streamlit + Tableau**.

### Visualizations Included:

## 📈 1. Order Traffic by Hour
- Identified peak window (19:00–20:00).
- Established operational stress window.

## 🔥 2. High-Collision Aisles
- Aisle B showed highest picker density at 19:00.
- Indicates collision and congestion risk.

## ❄️ 3. Spoilage Risk
- Flagged SKUs violating temperature constraints.
- Quantified inventory at risk.

## 🚧 4. Forklift Dead-Zone (Unspoken Physics)
Rule implemented:
> Forklift cannot enter Aisle B if >2 pickers present.

Simulation shows peak-hour blockage, causing cascading delays.

---

# 📦 C. Strategic Slotting Plan (Week 91)

Optimization goals:

- Reduce picker travel distance
- Minimize Aisle B congestion
- Respect temperature & weight constraints
- Stay within relocation labor budget

### Hard Constraints Enforced:
- No temperature mismatches
- No shelf weight violations
- No invalid bin assignments

Final output:
```
final_slotting_plan.csv
```
Contains:
```
SKU_ID, Bin_ID
```

---

# 📐 Chaos Score (Custom Metric)

We designed a weighted warehouse health metric:

Chaos Score =
- 40% Congestion Density
- 25% Spoilage Risk
- 20% Travel Inefficiency
- 15% Constraint Violations

This quantifies operational entropy into a single KPI.

---

# 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Streamlit
- Seaborn / Matplotlib
- Tableau
- Git / GitHub

---

# 📌 Key Insights

- Peak stress begins at 19:00.
- Aisle B is the primary collision hotspot.
- Forklift dead-zone significantly amplifies congestion.
- Temperature violations create hidden financial loss.
- Targeted SKU relocation yields higher ROI than full reshuffling.

---

# 📈 Strategic Outcome

Our intervention reduces:
- Picker congestion
- Travel distance
- Temperature violations
- Forklift blockage frequency

Result:  
**Stabilized operations and improved fulfillment performance.**

---

