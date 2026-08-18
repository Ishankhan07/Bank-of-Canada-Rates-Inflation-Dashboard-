import pandas as pd
import os

# --------------------------------------------------
# 1. Load CPI data
# --------------------------------------------------

file_path = "data/cpi_raw/18100004.csv"

df = pd.read_csv(
    file_path,
    low_memory=False
)

print("Original rows:", len(df))


# --------------------------------------------------
# 2. Filter Canada + All-items
# --------------------------------------------------

cpi = df[
    (df["GEO"] == "Canada") &
    (df["Products and product groups"] == "All-items")
].copy()

print("Rows after filtering:", len(cpi))


# --------------------------------------------------
# 3. Keep required columns
# --------------------------------------------------

cpi = cpi[
    ["REF_DATE", "VALUE"]
].copy()


# --------------------------------------------------
# 4. Rename columns
# --------------------------------------------------

cpi.rename(
    columns={
        "REF_DATE": "date",
        "VALUE": "cpi"
    },
    inplace=True
)


# --------------------------------------------------
# 5. Convert data types
# --------------------------------------------------

cpi["date"] = pd.to_datetime(cpi["date"])

cpi["cpi"] = pd.to_numeric(
    cpi["cpi"],
    errors="coerce"
)


# --------------------------------------------------
# 6. Keep data from 2016 onwards
# --------------------------------------------------

cpi = cpi[
    cpi["date"] >= "2016-01-01"
].copy()


# --------------------------------------------------
# 7. Sort by date
# --------------------------------------------------

cpi = cpi.sort_values("date")


# --------------------------------------------------
# 8. Calculate Year-over-Year inflation
# --------------------------------------------------

cpi["inflation"] = (
    cpi["cpi"].pct_change(periods=12) * 100
)


# --------------------------------------------------
# 9. Remove missing inflation values
# --------------------------------------------------

cpi = cpi.dropna(
    subset=["inflation"]
)


# --------------------------------------------------
# 10. Save processed CPI data
# --------------------------------------------------

os.makedirs("data", exist_ok=True)

cpi.to_csv(
    "data/cpi_monthly.csv",
    index=False
)


# --------------------------------------------------
# 11. Display results
# --------------------------------------------------

print("\nCPI processing completed!")

print("Final CPI rows:", len(cpi))

print("\nFirst 5 rows:")
print(cpi.head())

print("\nLast 5 rows:")
print(cpi.tail())

print("\nSaved to: data/cpi_monthly.csv")