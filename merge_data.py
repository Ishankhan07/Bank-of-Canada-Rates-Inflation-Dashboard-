import pandas as pd
import os

# =========================================================
# 1. Load datasets
# =========================================================

policy = pd.read_csv("data/policy_rate.csv")
usd_cad = pd.read_csv("data/usd_cad.csv")
cpi = pd.read_csv("data/cpi_monthly.csv")

print("Policy rows:", len(policy))
print("USD/CAD rows:", len(usd_cad))
print("CPI rows:", len(cpi))


# =========================================================
# 2. Convert dates
# =========================================================

policy["date"] = pd.to_datetime(policy["date"])
usd_cad["date"] = pd.to_datetime(usd_cad["date"])
cpi["date"] = pd.to_datetime(cpi["date"])


# =========================================================
# 3. Convert daily Policy Rate to monthly
# =========================================================

policy_monthly = (
    policy
    .set_index("date")
    .resample("MS")["policy_rate"]
    .last()
    .reset_index()
)

print("\nPolicy monthly rows:", len(policy_monthly))


# =========================================================
# 4. Convert daily USD/CAD to monthly average
# =========================================================

usd_cad_monthly = (
    usd_cad
    .set_index("date")
    .resample("MS")["usd_cad"]
    .mean()
    .reset_index()
)

print("USD/CAD monthly rows:", len(usd_cad_monthly))


# =========================================================
# 5. Merge Policy Rate + CPI
# =========================================================

master = pd.merge(
    policy_monthly,
    cpi[["date", "cpi", "inflation"]],
    on="date",
    how="inner"
)


# =========================================================
# 6. Merge USD/CAD
# =========================================================

master = pd.merge(
    master,
    usd_cad_monthly,
    on="date",
    how="inner"
)


# =========================================================
# 7. Sort by date
# =========================================================

master = master.sort_values("date")


# =========================================================
# 8. Remove missing values
# =========================================================

master = master.dropna()


# =========================================================
# 9. Save final master dataset
# =========================================================

os.makedirs("data/processed", exist_ok=True)

master.to_csv(
    "data/processed/master_dataset.csv",
    index=False
)


# =========================================================
# 10. Display final result
# =========================================================

print("\n===================================")
print("MASTER DATASET CREATED")
print("===================================")

print("\nRows:", len(master))
print("Columns:", len(master.columns))

print("\nDate range:")
print(master["date"].min(), "to", master["date"].max())

print("\nColumns:")
print(master.columns.tolist())

print("\nFirst 5 rows:")
print(master.head())

print("\nLast 5 rows:")
print(master.tail())

print("\nSaved to:")
print("data/processed/master_dataset.csv")