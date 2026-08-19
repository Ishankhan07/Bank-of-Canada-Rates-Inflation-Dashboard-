import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bank of Canada Rates & Inflation Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
    "Data/processed/analysis_dataset.csv"
)

    df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("🇨🇦 Bank of Canada Rates & Inflation Dashboard")

st.markdown(
    "Interactive analysis of Canadian interest rates, "
    "inflation and USD/CAD exchange-rate movements."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")


# Date range
min_date = df["date"].min()
max_date = df["date"].max()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(
        min_date.to_pydatetime(),
        max_date.to_pydatetime()
    ),
    format="MMM YYYY"
)


# Indicator selector
selected_indicators = st.sidebar.multiselect(
    "Select Indicators",
    ["Policy Rate", "Inflation", "USD/CAD"],
    default=["Policy Rate", "Inflation"]
)


# Apply date filter
filtered_df = df[
    (df["date"] >= pd.Timestamp(date_range[0])) &
    (df["date"] <= pd.Timestamp(date_range[1]))
].copy()


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📌 Key Indicators")


# Latest available row within selected date range
latest = filtered_df.iloc[-1]


# Peak values within selected date range
peak_inflation = filtered_df["inflation"].max()
peak_policy_rate = filtered_df["policy_rate"].max()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Policy Rate",
        f"{latest['policy_rate']:.2f}%"
    )


with col2:

    st.metric(
        "Inflation",
        f"{latest['inflation']:.2f}%"
    )


with col3:

    st.metric(
        "USD/CAD",
        f"{latest['usd_cad']:.2f}"
    )


with col4:

    st.metric(
        "Peak Inflation",
        f"{peak_inflation:.2f}%"
    )


# =========================================================
# POLICY RATE VS INFLATION
# =========================================================

st.subheader("📈 Policy Rate vs Inflation")


fig = go.Figure()


if "Policy Rate" in selected_indicators:

    fig.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["policy_rate"],
            name="Policy Rate",
            mode="lines+markers"
        )
    )


if "Inflation" in selected_indicators:

    fig.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["inflation"],
            name="Inflation",
            mode="lines+markers"
        )
    )


if "USD/CAD" in selected_indicators:

    fig.add_trace(
        go.Scatter(
            x=filtered_df["date"],
            y=filtered_df["usd_cad"],
            name="USD/CAD",
            mode="lines+markers"
        )
    )


fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Value",
    hovermode="x unified",
    height=500
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# RATE CYCLE ANALYSIS
# =========================================================

st.subheader("🔄 Interest Rate Cycle")


cycle_counts = (
    filtered_df["rate_cycle"]
    .value_counts()
    .reset_index()
)

cycle_counts.columns = [
    "Rate Cycle",
    "Months"
]


fig_cycle = px.bar(
    cycle_counts,
    x="Rate Cycle",
    y="Months",
    title="Hiking, Holding and Cutting Periods",
    text="Months"
)


fig_cycle.update_layout(
    height=400
)


st.plotly_chart(
    fig_cycle,
    use_container_width=True
)


# =========================================================
# RATE CYCLE TIMELINE
# =========================================================

fig_timeline = px.scatter(
    filtered_df,
    x="date",
    y="policy_rate",
    color="rate_cycle",
    title="Policy Rate Cycle Timeline",
    hover_data=[
        "policy_rate",
        "inflation",
        "usd_cad"
    ]
)


fig_timeline.update_layout(
    xaxis_title="Date",
    yaxis_title="Policy Rate (%)",
    height=450
)


st.plotly_chart(
    fig_timeline,
    use_container_width=True
)


# =========================================================
# USD/CAD ANALYSIS
# =========================================================

st.subheader("💱 USD/CAD Exchange Rate")


fig_usd = px.line(
    filtered_df,
    x="date",
    y="usd_cad",
    markers=True,
    title="USD/CAD Exchange Rate Trend"
)


fig_usd.update_layout(
    xaxis_title="Date",
    yaxis_title="USD/CAD",
    height=450
)


st.plotly_chart(
    fig_usd,
    use_container_width=True
)


# =========================================================
# CORRELATION HEATMAP
# =========================================================

st.subheader("📊 Correlation Analysis")


correlation = filtered_df[
    ["policy_rate", "inflation", "usd_cad"]
].corr()


fig_corr = px.imshow(
    correlation,
    text_auto=".2f",
    aspect="auto",
    title="Correlation Heatmap"
)


fig_corr.update_layout(
    height=450
)


st.plotly_chart(
    fig_corr,
    use_container_width=True
)


# =========================================================
# LAG ANALYSIS
# =========================================================

st.subheader("⏱️ Lag Analysis")


lags = [1, 3, 6, 12]

lag_results = []


for lag in lags:

    correlation_value = (
        filtered_df["policy_rate"]
        .shift(lag)
        .corr(filtered_df["inflation"])
    )

    lag_results.append(
        {
            "Lag": f"{lag} Month",
            "Correlation": correlation_value
        }
    )


lag_df = pd.DataFrame(lag_results)


fig_lag = px.bar(
    lag_df,
    x="Lag",
    y="Correlation",
    text="Correlation",
    title="Policy Rate Lag vs Inflation"
)


fig_lag.update_traces(
    texttemplate="%{text:.3f}"
)


fig_lag.update_layout(
    height=400
)


st.plotly_chart(
    fig_lag,
    use_container_width=True
)


# =========================================================
# 2022–2023 HIKING CYCLE
# =========================================================

st.subheader("🎯 2022–2023 Rate Hiking Cycle")


hiking_df = df[
    (df["date"] >= "2022-01-01") &
    (df["date"] <= "2023-12-01")
].copy()


fig_hiking = go.Figure()


fig_hiking.add_trace(
    go.Scatter(
        x=hiking_df["date"],
        y=hiking_df["policy_rate"],
        name="Policy Rate",
        mode="lines+markers"
    )
)


fig_hiking.add_trace(
    go.Scatter(
        x=hiking_df["date"],
        y=hiking_df["inflation"],
        name="Inflation",
        mode="lines+markers"
    )
)


fig_hiking.update_layout(
    title="Policy Rate and Inflation During 2022–2023",
    xaxis_title="Date",
    yaxis_title="Percentage (%)",
    hovermode="x unified",
    height=500
)


st.plotly_chart(
    fig_hiking,
    use_container_width=True
)


# =========================================================
# KEY INSIGHTS
# =========================================================

st.subheader("💡 Key Insights")


# Peak inflation within selected range
peak_inflation_row = filtered_df.loc[
    filtered_df["inflation"].idxmax()
]


# Peak policy rate within selected range
peak_rate_row = filtered_df.loc[
    filtered_df["policy_rate"].idxmax()
]


st.write(
    f"• Inflation reached a peak of "
    f"**{peak_inflation_row['inflation']:.2f}%** "
    f"in **{peak_inflation_row['date'].strftime('%B %Y')}** "
    f"within the selected period."
)


st.write(
    f"• The policy rate reached a peak of "
    f"**{peak_rate_row['policy_rate']:.2f}%** "
    f"in **{peak_rate_row['date'].strftime('%B %Y')}** "
    f"within the selected period."
)


st.write(
    "• The dashboard compares inflation, interest rates "
    "and currency movements over time."
)


st.write(
    "• Lag analysis examines whether historical policy-rate "
    "movements show a delayed relationship with inflation."
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")


st.caption(
    "Bank of Canada Rates & Inflation Dashboard | "
    "Built with Python, Pandas, Plotly and Streamlit"
)