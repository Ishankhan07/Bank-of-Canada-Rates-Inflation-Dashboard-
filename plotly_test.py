import pandas as pd
import plotly.graph_objects as go

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("data/processed/analysis_dataset.csv")

df["date"] = pd.to_datetime(df["date"])

print("Data loaded successfully!")
print(f"Rows: {len(df)}")


# =========================================================
# 1. POLICY RATE VS INFLATION
# =========================================================

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["policy_rate"],
        name="Policy Rate",
        mode="lines"
    )
)

fig1.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["inflation"],
        name="Inflation",
        mode="lines",
        yaxis="y2"
    )
)

fig1.update_layout(
    title="Bank of Canada Policy Rate vs Inflation",
    xaxis_title="Date",
    yaxis=dict(
        title="Policy Rate (%)"
    ),
    yaxis2=dict(
        title="Inflation (%)",
        overlaying="y",
        side="right"
    ),
    hovermode="x unified"
)

fig1.write_html("policy_vs_inflation.html")

print("1. Policy vs Inflation chart created")


# =========================================================
# 2. USD/CAD TREND
# =========================================================

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["usd_cad"],
        name="USD/CAD",
        mode="lines"
    )
)

fig2.update_layout(
    title="USD/CAD Exchange Rate Trend",
    xaxis_title="Date",
    yaxis_title="USD/CAD",
    hovermode="x unified"
)

fig2.write_html("usd_cad_trend.html")

print("2. USD/CAD chart created")


# =========================================================
# 3. RATE CYCLE ANALYSIS
# =========================================================

fig3 = go.Figure()

# Policy rate line
fig3.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["policy_rate"],
        name="Policy Rate",
        mode="lines"
    )
)

# Hiking points
hiking = df[df["rate_cycle"] == "Hiking"]

fig3.add_trace(
    go.Scatter(
        x=hiking["date"],
        y=hiking["policy_rate"],
        name="Hiking",
        mode="markers"
    )
)

# Cutting points
cutting = df[df["rate_cycle"] == "Cutting"]

fig3.add_trace(
    go.Scatter(
        x=cutting["date"],
        y=cutting["policy_rate"],
        name="Cutting",
        mode="markers"
    )
)

fig3.update_layout(
    title="Bank of Canada Policy Rate Cycles",
    xaxis_title="Date",
    yaxis_title="Policy Rate (%)",
    hovermode="x unified"
)

fig3.write_html("rate_cycle_analysis.html")

print("3. Rate cycle chart created")


# =========================================================
# 4. CORRELATION HEATMAP
# =========================================================

correlation = df[
    ["policy_rate", "inflation", "usd_cad"]
].corr()

fig4 = go.Figure(
    data=go.Heatmap(
        z=correlation.values,
        x=correlation.columns,
        y=correlation.columns,
        text=correlation.round(2).values,
        texttemplate="%{text}",
        colorscale="RdBu",
        zmin=-1,
        zmax=1
    )
)

fig4.update_layout(
    title="Correlation Between Economic Indicators"
)

fig4.write_html("correlation_heatmap.html")

print("4. Correlation heatmap created")


# =========================================================
# 5. LAG ANALYSIS
# =========================================================

lags = [1, 3, 6, 12]

lag_correlations = []

for lag in lags:

    correlation_value = (
        df["policy_rate"]
        .shift(lag)
        .corr(df["inflation"])
    )

    lag_correlations.append(correlation_value)


lag_df = pd.DataFrame({
    "lag": lags,
    "correlation": lag_correlations
})


fig5 = go.Figure()

fig5.add_trace(
    go.Bar(
        x=lag_df["lag"],
        y=lag_df["correlation"],
        text=lag_df["correlation"].round(3),
        textposition="outside",
        name="Correlation"
    )
)

fig5.update_layout(
    title="Policy Rate Lag vs Inflation",
    xaxis_title="Policy Rate Lag (Months)",
    yaxis_title="Correlation",
    xaxis=dict(
        tickmode="array",
        tickvals=lags
    )
)

fig5.write_html("lag_analysis.html")

print("5. Lag analysis chart created")


# =========================================================
# 6. 2022–2023 HIKING CYCLE
# =========================================================

cycle = df[
    (df["date"] >= "2022-01-01") &
    (df["date"] <= "2023-12-31")
].copy()


fig6 = go.Figure()

# Policy rate
fig6.add_trace(
    go.Scatter(
        x=cycle["date"],
        y=cycle["policy_rate"],
        name="Policy Rate",
        mode="lines"
    )
)

# Inflation
fig6.add_trace(
    go.Scatter(
        x=cycle["date"],
        y=cycle["inflation"],
        name="Inflation",
        mode="lines",
        yaxis="y2"
    )
)

fig6.update_layout(
    title="2022–2023 Bank of Canada Hiking Cycle",
    xaxis_title="Date",

    yaxis=dict(
        title="Policy Rate (%)"
    ),

    yaxis2=dict(
        title="Inflation (%)",
        overlaying="y",
        side="right"
    ),

    hovermode="x unified"
)

fig6.write_html("hiking_cycle_2022_2023.html")

print("6. 2022–2023 hiking cycle chart created")


# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n===================================")
print("ALL PLOTLY CHARTS CREATED")
print("===================================")

print("""
1. policy_vs_inflation.html
2. usd_cad_trend.html
3. rate_cycle_analysis.html
4. correlation_heatmap.html
5. lag_analysis.html
6. hiking_cycle_2022_2023.html
""")
