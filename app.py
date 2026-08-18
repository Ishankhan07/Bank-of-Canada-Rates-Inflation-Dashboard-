import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import html


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bank of Canada Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM DARK THEME
# =========================================================

st.markdown(
    """
    <style>

    /* ==============================
       MAIN APPLICATION
       ============================== */

    .stApp {
        background-color: #0E1117;
        color: #E6E6E6;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {
        background-color: #151922;
        min-width: 300px;
        max-width: 300px;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    section[data-testid="stSidebar"] h1 {
        color: #F3F4F6;
        font-size: 25px;
    }

    section[data-testid="stSidebar"] p {
        color: #9CA3AF;
        line-height: 1.6;
    }


    /* ==============================
       HEADER
       ============================== */

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        font-size: 16px;
        color: #9CA3AF;
        margin-bottom: 28px;
    }


    /* ==============================
       KPI CARDS
       ============================== */

    .kpi-card {
        background-color: #171B26;
        border: 1px solid #2A3040;
        border-radius: 14px;
        padding: 20px 18px;
        min-height: 110px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }

    .kpi-title {
        color: #9CA3AF;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        color: #F5F5F5;
        font-size: 28px;
        font-weight: 700;
    }


    /* ==============================
       SECTION HEADINGS
       ============================== */

    .section-title {
        font-size: 23px;
        font-weight: 600;
        color: #F5F5F5;
        margin-top: 35px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #8F96A3;
        font-size: 14px;
        margin-bottom: 12px;
    }


    /* ==============================
       INSIGHT CARDS
       ============================== */

    .insight-card {
        background-color: #171B26;
        border: 1px solid #2A3040;
        border-left: 4px solid #6C8AE4;
        border-radius: 10px;
        padding: 15px 18px;
        margin-bottom: 10px;
        color: #D1D5DB;
        font-size: 15px;
        line-height: 1.6;
    }


    /* ==============================
       FOOTER
       ============================== */

    .footer {
        text-align: center;
        color: #6B7280;
        font-size: 13px;
        margin-top: 35px;
        padding-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "data/processed/analysis_dataset.csv"
)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 Dashboard Controls")

st.sidebar.write(
    "Use the controls below to explore Canadian "
    "economic indicators and policy trends."
)

st.sidebar.markdown("---")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    f"Data period: {min_date} to {max_date}"
)

st.sidebar.caption(
    f"Monthly observations: {len(df)}"
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["date"].dt.date >= date_range[0]) &
    (df["date"].dt.date <= date_range[1])
].copy()

filtered_df = filtered_df.sort_values("date")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    'Bank of Canada Rates & Inflation Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive analysis of policy rates, inflation, '
    'exchange rates and monetary policy cycles'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

latest = filtered_df.iloc[-1]

latest_policy = latest["policy_rate"]
latest_inflation = latest["inflation"]
latest_usd = latest["usd_cad"]
latest_cycle = latest["rate_cycle"]


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Policy Rate</div>
            <div class="kpi-value">{latest_policy:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Inflation</div>
            <div class="kpi-value">{latest_inflation:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">USD / CAD</div>
            <div class="kpi-value">{latest_usd:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Rate Cycle</div>
            <div class="kpi-value">{latest_cycle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 1. POLICY RATE VS INFLATION
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📈 Policy Rate vs Inflation'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Comparison of monetary policy rates and inflation over time.'
    '</div>',
    unsafe_allow_html=True
)

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=filtered_df["date"],
        y=filtered_df["policy_rate"],
        name="Policy Rate",
        mode="lines",
        line=dict(width=2.5)
    )
)

fig1.add_trace(
    go.Scatter(
        x=filtered_df["date"],
        y=filtered_df["inflation"],
        name="Inflation",
        mode="lines",
        yaxis="y2",
        line=dict(width=2.5)
    )
)

fig1.update_layout(
    template="plotly_dark",
    height=500,
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis_title="Date",
    yaxis=dict(
        title="Policy Rate (%)"
    ),
    yaxis2=dict(
        title="Inflation (%)",
        overlaying="y",
        side="right"
    ),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        y=1.08,
        x=0
    )
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# =========================================================
# 2. USD/CAD TREND
# =========================================================

st.markdown(
    '<div class="section-title">'
    '💱 USD/CAD Exchange Rate'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Historical movement of the Canadian dollar against the US dollar.'
    '</div>',
    unsafe_allow_html=True
)

fig2 = px.line(
    filtered_df,
    x="date",
    y="usd_cad",
    title="USD/CAD Trend"
)

fig2.update_traces(
    line=dict(width=2.5)
)

fig2.update_layout(
    template="plotly_dark",
    height=450,
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis_title="Date",
    yaxis_title="USD/CAD",
    hovermode="x unified"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# =========================================================
# 3. RATE CYCLE ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '🔄 Policy Rate Cycle Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Identification of hiking and cutting periods based on '
    'monthly policy-rate changes.'
    '</div>',
    unsafe_allow_html=True
)

fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=filtered_df["date"],
        y=filtered_df["policy_rate"],
        name="Policy Rate",
        mode="lines",
        line=dict(width=2.5)
    )
)

hiking = filtered_df[
    filtered_df["rate_cycle"] == "Hiking"
]

cutting = filtered_df[
    filtered_df["rate_cycle"] == "Cutting"
]

if not hiking.empty:

    fig3.add_trace(
        go.Scatter(
            x=hiking["date"],
            y=hiking["policy_rate"],
            name="Hiking",
            mode="markers",
            marker=dict(size=9)
        )
    )


if not cutting.empty:

    fig3.add_trace(
        go.Scatter(
            x=cutting["date"],
            y=cutting["policy_rate"],
            name="Cutting",
            mode="markers",
            marker=dict(size=9)
        )
    )


fig3.update_layout(
    template="plotly_dark",
    height=450,
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis_title="Date",
    yaxis_title="Policy Rate (%)",
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# =========================================================
# 4. CORRELATION ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '🔗 Correlation Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Correlation between policy rate, inflation and USD/CAD.'
    '</div>',
    unsafe_allow_html=True
)

correlation = filtered_df[
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
        zmax=1,
        hovertemplate=(
            "%{y} vs %{x}"
            "<br>Correlation: %{z:.3f}"
            "<extra></extra>"
        )
    )
)

fig4.update_layout(
    template="plotly_dark",
    height=450,
    margin=dict(l=20, r=20, t=60, b=20),
    title="Economic Indicator Correlation"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


# =========================================================
# 5. LAG ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '⏱️ Policy Rate Lag Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Examining the relationship between previous policy rates '
    'and current inflation at selected time lags.'
    '</div>',
    unsafe_allow_html=True
)

lags = [1, 3, 6, 12]

lag_correlations = []

for lag in lags:

    value = (
        filtered_df["policy_rate"]
        .shift(lag)
        .corr(filtered_df["inflation"])
    )

    lag_correlations.append(value)


lag_df = pd.DataFrame(
    {
        "Lag": lags,
        "Correlation": lag_correlations
    }
)

fig5 = px.bar(
    lag_df,
    x="Lag",
    y="Correlation",
    text="Correlation",
    title="Policy Rate Lag vs Inflation"
)

fig5.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)

fig5.update_layout(
    template="plotly_dark",
    height=450,
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis_title="Policy Rate Lag (Months)",
    yaxis_title="Correlation",
    xaxis=dict(
        tickmode="array",
        tickvals=lags
    )
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# =========================================================
# 6. 2022–2023 HIKING CYCLE
# =========================================================

st.markdown(
    '<div class="section-title">'
    '🎯 2022–2023 Hiking Cycle'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Focused analysis of the major Canadian monetary-policy '
    'tightening period.'
    '</div>',
    unsafe_allow_html=True
)

cycle = df[
    (df["date"] >= "2022-01-01") &
    (df["date"] <= "2023-12-31")
].copy()


fig6 = go.Figure()

fig6.add_trace(
    go.Scatter(
        x=cycle["date"],
        y=cycle["policy_rate"],
        name="Policy Rate",
        mode="lines",
        line=dict(width=2.5)
    )
)

fig6.add_trace(
    go.Scatter(
        x=cycle["date"],
        y=cycle["inflation"],
        name="Inflation",
        mode="lines",
        yaxis="y2",
        line=dict(width=2.5)
    )
)

fig6.update_layout(
    template="plotly_dark",
    height=500,
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis_title="Date",
    yaxis=dict(
        title="Policy Rate (%)"
    ),
    yaxis2=dict(
        title="Inflation (%)",
        overlaying="y",
        side="right"
    ),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        y=1.08,
        x=0
    )
)

st.plotly_chart(
    fig6,
    use_container_width=True
)


# =========================================================
# 2022–2023 KPI SUMMARY
# =========================================================

cycle_start_rate = cycle["policy_rate"].iloc[0]
cycle_peak_rate = cycle["policy_rate"].max()

cycle_rate_increase = (
    cycle_peak_rate - cycle_start_rate
)

peak_inflation = cycle["inflation"].max()

peak_inflation_date = cycle.loc[
    cycle["inflation"].idxmax(),
    "date"
]

hiking_months = (
    cycle["rate_cycle"] == "Hiking"
).sum()

holding_months = (
    cycle["rate_cycle"] == "Holding"
).sum()


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Starting Rate",
        f"{cycle_start_rate:.2f}%"
    )

with col2:

    st.metric(
        "Peak Rate",
        f"{cycle_peak_rate:.2f}%"
    )

with col3:

    st.metric(
        "Rate Increase",
        f"+{cycle_rate_increase:.2f} pp"
    )

with col4:

    st.metric(
        "Peak Inflation",
        f"{peak_inflation:.2f}%"
    )


# =========================================================
# KEY ANALYTICAL INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '💡 Key Analytical Insights'
    '</div>',
    unsafe_allow_html=True
)

# Find strongest lag
strongest_lag_row = lag_df.loc[
    lag_df["Correlation"].abs().idxmax()
]

strongest_lag = int(
    strongest_lag_row["Lag"]
)

strongest_lag_corr = (
    strongest_lag_row["Correlation"]
)


insights = [

    (
        f"The policy rate increased from "
        f"{cycle_start_rate:.2f}% to {cycle_peak_rate:.2f}% "
        f"during the 2022–2023 tightening period."
    ),

    (
        f"Inflation reached a peak of "
        f"{peak_inflation:.2f}% in "
        f"{peak_inflation_date.strftime('%B %Y')}."
    ),

    (
        f"The strongest tested lag relationship occurred "
        f"at {strongest_lag} months, with a correlation "
        f"of approximately {strongest_lag_corr:.3f}."
    ),

    (
        f"The 2022–2023 period contained "
        f"{hiking_months} hiking months and "
        f"{holding_months} holding months "
        f"in the selected dataset."
    )
]


for insight in insights:

    # Escape HTML so that the insight text
    # can never break the custom card.
    safe_insight = html.escape(insight)

    st.markdown(
        f"""
        <div class="insight-card">
            {safe_insight}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DATA SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📋 Dataset Summary'
    '</div>',
    unsafe_allow_html=True
)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:

    st.metric(
        "Total Observations",
        len(df)
    )

with summary_col2:

    st.metric(
        "Analysis Period",
        f"{df['date'].min().year}–{df['date'].max().year}"
    )

with summary_col3:

    st.metric(
        "Indicators",
        3
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Bank of Canada Rates & Inflation Dashboard
        <br>
        Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)