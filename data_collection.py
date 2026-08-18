import requests
import pandas as pd
import os

# =========================================================
# 1. Create data folder
# =========================================================

os.makedirs("data", exist_ok=True)


# =========================================================
# 2. Function to get Bank of Canada Valet data
# =========================================================

def get_boc_data(series_code, column_name, start_date="2016-01-01"):
    
    url = (
        f"https://www.bankofcanada.ca/valet/observations/"
        f"{series_code}/json"
        f"?start_date={start_date}"
    )

    print(f"\nDownloading {column_name}...")

    response = requests.get(url, timeout=30)

    print("Status Code:", response.status_code)

    response.raise_for_status()

    data = response.json()

    observations = data["observations"]

    rows = []

    for item in observations:

        date = item["d"]

        # The series code contains the value
        value = item[series_code]["v"]

        rows.append({
            "date": date,
            column_name: value
        })

    df = pd.DataFrame(rows)

    df["date"] = pd.to_datetime(df["date"])

    df[column_name] = pd.to_numeric(
        df[column_name],
        errors="coerce"
    )

    df = df.sort_values("date")

    return df


# =========================================================
# 3. Policy Rate
# =========================================================

policy_rate = get_boc_data(
    "V39079",
    "policy_rate"
)

policy_rate.to_csv(
    "data/policy_rate.csv",
    index=False
)

print(
    "Policy rate saved:",
    len(policy_rate),
    "rows"
)


# =========================================================
# 4. USD/CAD Exchange Rate
# =========================================================

usd_cad = get_boc_data(
    "FXUSDCAD",
    "usd_cad"
)

usd_cad.to_csv(
    "data/usd_cad.csv",
    index=False
)

print(
    "USD/CAD saved:",
    len(usd_cad),
    "rows"
)


# =========================================================
# 5. Monthly USD/CAD
# =========================================================

usd_cad_monthly = (
    usd_cad
    .set_index("date")
    .resample("MS")
    .mean()
    .reset_index()
)

usd_cad_monthly.to_csv(
    "data/usd_cad_monthly.csv",
    index=False
)

print(
    "Monthly USD/CAD saved:",
    len(usd_cad_monthly),
    "rows"
)


# =========================================================
# 6. Display basic information
# =========================================================

print("\n--- Policy Rate ---")
print(policy_rate.head())

print("\n--- USD/CAD Monthly ---")
print(usd_cad_monthly.head())

print("\nData collection completed successfully!")