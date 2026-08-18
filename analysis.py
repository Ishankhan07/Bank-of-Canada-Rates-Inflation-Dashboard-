import pandas as pd

# Load master dataset
df = pd.read_csv("data/processed/master_dataset.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Compare current policy rate with previous month
df["rate_change"] = df["policy_rate"].diff()

# Classify rate cycle
df["rate_cycle"] = df["rate_change"].apply(
    lambda x:
        "Hiking" if x > 0
        else "Cutting" if x < 0
        else "Holding"
)

# First row has no previous month
df.loc[df.index[0], "rate_cycle"] = "N/A"

# Display results
print("\nRate Cycle Classification:")
print(
    df[
        ["date", "policy_rate", "rate_change", "rate_cycle"]
    ].head(20)
)

# Count each cycle
print("\nCycle Counts:")
print(df["rate_cycle"].value_counts())

# Save analysis dataset
df.to_csv(
    "data/processed/analysis_dataset.csv",
    index=False
)

print("\nAnalysis dataset saved successfully!")

# =========================================================
# TREND ANALYSIS
# =========================================================

print("\n===== TREND ANALYSIS =====")

# Overall change from first to last observation
for column in ["policy_rate", "inflation", "usd_cad"]:
    first_value = df[column].iloc[0]
    last_value = df[column].iloc[-1]
    change = last_value - first_value

    print(f"\n{column}")
    print(f"Starting value: {first_value:.2f}")
    print(f"Latest value:   {last_value:.2f}")
    print(f"Overall change: {change:.2f}")


# Highest and lowest inflation
highest_inflation = df.loc[df["inflation"].idxmax()]
lowest_inflation = df.loc[df["inflation"].idxmin()]

print("\nHighest Inflation:")
print(highest_inflation[["date", "inflation"]])

print("\nLowest Inflation:")
print(lowest_inflation[["date", "inflation"]])


# Highest and lowest policy rate
highest_rate = df.loc[df["policy_rate"].idxmax()]
lowest_rate = df.loc[df["policy_rate"].idxmin()]

print("\nHighest Policy Rate:")
print(highest_rate[["date", "policy_rate"]])

print("\nLowest Policy Rate:")
print(lowest_rate[["date", "policy_rate"]])

# =========================================================
# CORRELATION ANALYSIS
# =========================================================

print("\n===== CORRELATION ANALYSIS =====")

correlation = df[
    ["policy_rate", "inflation", "usd_cad"]
].corr()

print("\nCorrelation Matrix:")
print(correlation)

# =========================================================
# LAG ANALYSIS
# =========================================================

print("\n===== LAG ANALYSIS =====")

lags = [1, 3, 6, 12]

for lag in lags:

    lag_correlation = (
        df["policy_rate"]
        .shift(lag)
        .corr(df["inflation"])
    )

    print(
        f"Policy Rate Lag {lag} months "
        f"vs Inflation: {lag_correlation:.3f}"
    )

# =========================================================
# 2022–2023 HIKING CYCLE ANALYSIS
# =========================================================

print("\n===== 2022–2023 HIKING CYCLE =====")

# Filter 2022-2023 period
cycle = df[
    (df["date"] >= "2022-01-01") &
    (df["date"] <= "2023-12-31")
].copy()

print("\nPeriod:")
print(cycle["date"].min(), "to", cycle["date"].max())


# ---------------------------------------------------------
# Policy rate analysis
# ---------------------------------------------------------

starting_rate = cycle["policy_rate"].iloc[0]
peak_rate = cycle["policy_rate"].max()

rate_increase = peak_rate - starting_rate

print("\nPolicy Rate:")
print(f"Starting rate: {starting_rate:.2f}%")
print(f"Peak rate:     {peak_rate:.2f}%")
print(f"Total increase: {rate_increase:.2f} percentage points")


# ---------------------------------------------------------
# Inflation analysis
# ---------------------------------------------------------

peak_inflation = cycle.loc[
    cycle["inflation"].idxmax()
]

print("\nInflation:")
print(
    f"Peak inflation: "
    f"{peak_inflation['inflation']:.2f}%"
)

print(
    f"Inflation peak date: "
    f"{peak_inflation['date'].strftime('%Y-%m')}"
)


# ---------------------------------------------------------
# USD/CAD analysis
# ---------------------------------------------------------

starting_usd = cycle["usd_cad"].iloc[0]
ending_usd = cycle["usd_cad"].iloc[-1]

usd_change = ending_usd - starting_usd

print("\nUSD/CAD:")
print(f"Starting USD/CAD: {starting_usd:.2f}")
print(f"Ending USD/CAD:   {ending_usd:.2f}")
print(f"Change:           {usd_change:.2f}")


# ---------------------------------------------------------
# Rate-cycle counts
# ---------------------------------------------------------

cycle_counts = cycle["rate_cycle"].value_counts()

print("\nRate Cycle Counts:")
print(cycle_counts)