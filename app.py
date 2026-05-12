import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Weather Analytics",
    layout="wide",
    page_icon="🌤️"
)

# ── Dark Theme CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* ───────────────── MAIN APP ───────────────── */
.stApp {
    background: linear-gradient(135deg, #0b1120, #111827, #0f172a);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
/* ───────────── SIDEBAR MAIN ───────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #07111f 0%,
        #0b1d33 50%,
        #102845 100%
    );
    
    border-right: 2px solid rgba(0,212,255,0.25);
}

/* All sidebar text */
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #00d4ff !important;
    font-weight: 700;
}

/* Dropdown box */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background-color: #162235 !important;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    color: white !important;
}

/* Dropdown selected text */
section[data-testid="stSidebar"] .stSelectbox span {
    color: white !important;
}

/* Dropdown hover */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div:hover {
    border: 1px solid #00d4ff;
    box-shadow: 0 0 10px rgba(0,212,255,0.3);
}

/* Sidebar button */
section[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white !important;
    border-radius: 12px;
    border: none;
    font-weight: bold;
}

/* Button hover */
section[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(90deg, #00ffaa, #00d4ff);
}

/* Fix expander text */
section[data-testid="stSidebar"] details {
    color: white !important;
}

/* ───────────────── METRIC CARDS ───────────────── */
.metric-card {
    background: rgba(30, 33, 48, 0.65);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    margin: 5px;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

/* Card hover animation */
.metric-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(0,212,255,0.4);
    box-shadow: 0 12px 35px rgba(0,212,255,0.15);
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #00d4ff;
}

.metric-label {
    font-size: 13px;
    color: #b0b7c3;
    margin-top: 5px;
}

/* ───────────────── SECTION HEADERS ───────────────── */
.section-header {
    background: linear-gradient(
        90deg,
        rgba(0,212,255,0.15),
        rgba(255,255,255,0)
    );
    border-left: 4px solid #00d4ff;
    padding: 12px 18px;
    border-radius: 10px;
    margin: 24px 0 12px 0;
    font-size: 20px;
    font-weight: 700;
    color: white;
    backdrop-filter: blur(10px);
}

/* ───────────────── TITLE ───────────────── */
.main-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #00d4ff,
        #3b82f6,
        #00ffaa
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.subtitle {
    color: #94a3b8;
    font-size: 15px;
    margin-top: 2px;
}

/* ───────────────── CHART CONTAINERS ───────────────── */
[data-testid="stPlotlyChart"] {
    background: rgba(30, 33, 48, 0.5);
    border-radius: 18px;
    padding: 10px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

/* ───────────────── LABELS ───────────────── */
.stSelectbox label,
.stSlider label {
    color: #d1d5db !important;
    font-weight: 500;
}

/* ───────────────── FOOTER ───────────────── */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 24px;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin-top: 35px;
}

/* ───────────────── SCROLLBAR ───────────────── */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #111827;
}

::-webkit-scrollbar-thumb {
    background: #00d4ff;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #00ffaa;
}

</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("GlobalWeatherRepository.csv")
    return df

df = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 11])
with col_logo:
    st.markdown("# 🌤️")
with col_title:
    st.markdown('<p class="main-title">Global Weather Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">World Weather Station Data Visualization Dashboard</p>', unsafe_allow_html=True)

st.markdown("---")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("### 🔧 Filters & Controls")
st.sidebar.markdown("---")

country_list = ["All Countries"] + sorted(df["country"].dropna().unique().tolist())
country = st.sidebar.selectbox("🌍 Select Country", country_list)

parameter = st.sidebar.selectbox("📊 Select Parameter", [
    "Temperature (°C)", "Humidity", "Wind Speed (kph)", "UV Index", "Precipitation (mm)"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗺️ Map Options")
map_style = st.sidebar.selectbox("Map Style", [
    "carto-darkmatter", "open-street-map", "stamen-terrain"
])
color_scale = st.sidebar.selectbox("Color Scale", [
    "Viridis", "Plasma", "Inferno", "RdYlBu", "Turbo"
])

st.sidebar.markdown("---")
apply = st.sidebar.button("✅ Apply Filters", use_container_width=True)

if country != "All Countries":
    filtered = df[df["country"] == country]
else:
    filtered = df.copy()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Key Statistics</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">📍 {len(df):,}</div>
        <div class="metric-label">Total Records</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">🌍 {df['country'].nunique()}</div>
        <div class="metric-label">Countries</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">🌡️ {df['temperature_celsius'].mean():.1f}°C</div>
        <div class="metric-label">Avg Temperature</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">💧 {df['humidity'].mean():.1f}%</div>
        <div class="metric-label">Avg Humidity</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">💨 {df['wind_kph'].mean():.1f}</div>
        <div class="metric-label">Avg Wind (kph)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── World Map ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗺️ Global Weather Station Density Map</div>', unsafe_allow_html=True)

fig_map = px.density_mapbox(
    filtered,
    lat="latitude",
    lon="longitude",
    z="temperature_celsius",
    radius=8,
    zoom=1,
    center={"lat": 20, "lon": 0},
    mapbox_style=map_style,
    color_continuous_scale=color_scale,
    title="",
    height=500
)
fig_map.update_layout(
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="white",
    margin=dict(l=0, r=0, t=10, b=0),

    coloraxis_colorbar=dict(
        title=dict(
            text="Temp °C",
            font=dict(
                color="white",
                size=14
            )
        ),
        tickfont=dict(
            color="white"
        )
    )
)
st.plotly_chart(fig_map, use_container_width=True)

# ── Row 2 Charts ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Temperature & Distribution Analysis</div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)

with col_a:
    fig_hist = px.histogram(
        filtered, x="temperature_celsius", nbins=50,
        color_discrete_sequence=["#00d4ff"],
        labels={"temperature_celsius": "Temperature (°C)"},
        title="Temperature Distribution"
    )
    fig_hist.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="white", title_font_color="white",
        bargap=0.05, height=300,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_b:
    fig_scatter = px.scatter(
        filtered.sample(min(2000, len(filtered))),
        x="temperature_celsius", y="humidity",
        color="temperature_celsius",
        color_continuous_scale="Turbo",
        opacity=0.6,
        labels={"temperature_celsius": "Temp (°C)", "humidity": "Humidity"},
        title="Humidity vs Temperature"
    )
    fig_scatter.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="white", title_font_color="white",
        showlegend=False, height=300,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_c:
    top10 = (
        df.groupby("country")["temperature_celsius"]
        .mean().sort_values(ascending=True)
        .tail(10).reset_index()
    )
    fig_bar = px.bar(
        top10, x="temperature_celsius", y="country",
        orientation="h",
        color="temperature_celsius",
        color_continuous_scale="Reds",
        title="Top 10 Hottest Countries",
        labels={"temperature_celsius": "Avg Temp (°C)", "country": ""}
    )
    fig_bar.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="white", title_font_color="white",
        height=300, margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Row 3 Charts ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🌬️ Wind & Air Quality</div>', unsafe_allow_html=True)

col_d, col_e, col_f = st.columns(3)

with col_d:
    fig_wind = px.histogram(
        filtered, x="wind_kph", nbins=40,
        color_discrete_sequence=["#00ffaa"],
        title="Wind Speed Distribution (kph)"
    )
    fig_wind.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="white", title_font_color="white",
        height=300, margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_wind, use_container_width=True)

with col_e:
    fig_uv = px.box(
        df.groupby("country")["uv_index"]
        .mean().sort_values(ascending=False)
        .head(15).reset_index(),
        x="uv_index", y="country",
        color_discrete_sequence=["#ffaa00"],
        title="UV Index by Country (Top 15)",
        orientation="h"
    )
    fig_uv.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="white", title_font_color="white",
        height=300, margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_uv, use_container_width=True)

with col_f:
    co_data = (
        df.groupby("country")["air_quality_Carbon_Monoxide"]
        .mean().sort_values(ascending=False)
        .head(10).reset_index()
    )
    fig_co = px.bar(
        co_data, x="country",
        y="air_quality_Carbon_Monoxide",
        color="air_quality_Carbon_Monoxide",
        color_continuous_scale="Reds",
        title="Top 10 CO Levels by Country",
        labels={"air_quality_Carbon_Monoxide": "CO Level"}
    )
    fig_co.update_layout(
        paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
        font_color="white", title_font_color="white",
        height=300, margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_co, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌤️ Global Weather Analytics Dashboard &nbsp;|&nbsp;
    Data Source: Global Weather Repository, Kaggle &nbsp;|&nbsp;
    Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)