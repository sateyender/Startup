import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io

# ───────────────────────────────────────────────
#  PAGE CONFIG
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="StartupPulse · Enterprise",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────────────────────────────
#  DESIGN TOKENS
# ───────────────────────────────────────────────
C = {
    "bg"          : "#f8fafc",
    "card"        : "#ffffff",
    "border"      : "#f1f5f9",
    "indigo"      : "#4f46e5",
    "indigo_lt"   : "#eef2ff",
    "emerald"     : "#10b981",
    "emerald_lt"  : "#ecfdf5",
    "amber"       : "#f59e0b",
    "amber_lt"    : "#fffbeb",
    "rose"        : "#f43f5e",
    "rose_lt"     : "#fff1f2",
    "sky"         : "#0ea5e9",
    "sky_lt"      : "#f0f9ff",
    "slate_900"   : "#1e293b",
    "slate_600"   : "#64748b",
    "slate_400"   : "#94a3b8",
    "slate_100"   : "#f1f5f9",
    "slate_50"    : "#f8fafc",
}

PALETTE   = [C["indigo"], C["emerald"], C["amber"], C["rose"], C["sky"],
             "#8b5cf6", "#06b6d4", "#f97316", "#84cc16", "#ec4899"]
INDIGO_SEQ = ["#eef2ff", "#c7d2fe", "#a5b4fc", "#818cf8", "#6366f1", "#4f46e5", "#4338ca", "#3730a3"]

# ───────────────────────────────────────────────
#  GLOBAL CSS
# ───────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"], .stMarkdown, .stText {{
    font-family: 'Inter', sans-serif !important;
}}
.stApp {{
    background-color: {C["bg"]};
}}
.main .block-container {{
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1400px;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {C["card"]} !important;
    border-right: 1px solid {C["border"]};
}}
[data-testid="stSidebar"] * {{
    color: {C["slate_900"]} !important;
}}
[data-testid="stSidebar"] .stRadio label {{
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: {C["slate_600"]} !important;
    padding: 0.45rem 0.75rem;
    border-radius: 8px;
    display: block;
    transition: background .15s;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: {C["indigo_lt"]};
    color: {C["indigo"]} !important;
}}
[data-testid="stSidebar"] .stExpander {{
    border: 1px solid {C["border"]} !important;
    border-radius: 10px !important;
    background: {C["slate_50"]} !important;
}}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
    background-color: {C["indigo_lt"]} !important;
    color: {C["indigo"]} !important;
    border: 1px solid #c7d2fe !important;
}}

/* ── Page header band ── */
.page-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1.5rem 1.75rem;
    background: {C["card"]};
    border: 1px solid {C["border"]};
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.ph-left h1 {{
    font-size: 1.5rem;
    font-weight: 800;
    color: {C["slate_900"]};
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.02em;
    line-height: 1.2;
}}
.ph-left p {{
    font-size: 0.875rem;
    color: {C["slate_600"]};
    margin: 0;
}}
.ph-right {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.35rem;
}}
.ph-timestamp {{
    font-size: 0.78rem;
    color: {C["slate_400"]};
    font-weight: 500;
}}
.ph-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: {C["emerald"]};
    background: {C["emerald_lt"]};
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    border: 1px solid #a7f3d0;
}}

/* ── KPI Card ── */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}}
.kpi-card {{
    background: {C["card"]};
    border: 1px solid {C["border"]};
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    transition: transform .18s ease, box-shadow .18s ease;
    position: relative;
    overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}}
.kpi-card.indigo::before  {{ background: {C["indigo"]}; }}
.kpi-card.emerald::before {{ background: {C["emerald"]}; }}
.kpi-card.amber::before   {{ background: {C["amber"]}; }}
.kpi-card.sky::before     {{ background: {C["sky"]}; }}
.kpi-card.rose::before    {{ background: {C["rose"]}; }}
.kpi-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(79,70,229,0.10);
}}
.kpi-icon {{
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    margin-bottom: 0.85rem;
}}
.kpi-icon.indigo  {{ background: {C["indigo_lt"]}; }}
.kpi-icon.emerald {{ background: {C["emerald_lt"]}; }}
.kpi-icon.amber   {{ background: {C["amber_lt"]}; }}
.kpi-icon.sky     {{ background: {C["sky_lt"]}; }}
.kpi-icon.rose    {{ background: {C["rose_lt"]}; }}
.kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: {C["slate_400"]};
    margin-bottom: 0.3rem;
}}
.kpi-value {{
    font-size: 1.9rem;
    font-weight: 800;
    color: {C["slate_900"]};
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 0.45rem;
}}
.kpi-footer {{
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    color: {C["slate_600"]};
}}
.trend-up   {{ color: {C["emerald"]}; font-weight: 700; }}
.trend-down {{ color: {C["rose"]};    font-weight: 700; }}
.trend-dot  {{ color: {C["sky"]};     font-weight: 700; }}

/* ── Chart card ── */
.chart-card {{
    background: {C["card"]};
    border: 1px solid {C["border"]};
    border-radius: 14px;
    padding: 1.25rem 1.25rem 0.75rem 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}}
.chart-title {{
    font-size: 0.875rem;
    font-weight: 700;
    color: {C["slate_900"]};
    margin-bottom: 0.1rem;
}}
.chart-sub {{
    font-size: 0.78rem;
    color: {C["slate_400"]};
    margin-bottom: 0.8rem;
}}

/* ── Insight box ── */
.insight-box {{
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    background: {C["indigo_lt"]};
    border: 1px solid #c7d2fe;
    border-radius: 10px;
    padding: 0.65rem 0.9rem;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
}}
.insight-icon {{ font-size: 0.95rem; flex-shrink: 0; margin-top: 1px; }}
.insight-text {{
    font-size: 0.8rem;
    color: {C["indigo"]};
    font-weight: 500;
    line-height: 1.5;
}}

/* ── Section divider ── */
.section-rule {{
    border: none;
    border-top: 1px solid {C["border"]};
    margin: 1.25rem 0;
}}

/* ── Sidebar brand ── */
.brand-block {{
    padding: 0.5rem 0 1rem 0;
    border-bottom: 1px solid {C["border"]};
    margin-bottom: 1rem;
}}
.brand-name {{
    font-size: 1.1rem;
    font-weight: 800;
    color: {C["slate_900"]};
    letter-spacing: -0.02em;
}}
.brand-tag {{
    font-size: 0.72rem;
    color: {C["slate_400"]};
    font-weight: 500;
}}
.nav-label {{
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {C["slate_400"]};
    margin: 1rem 0 0.4rem 0;
    padding-left: 2px;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  DATA
# ───────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("startupPulse_Master_Data_Final.csv")
    return df

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("⚠️  `startupPulse_Master_Data_Final.csv` not found in the app directory.")
    st.stop()

ALL_INDUSTRIES = sorted(df_raw["Industry"].dropna().unique().tolist())
ALL_COUNTRIES  = sorted(df_raw["Country"].dropna().unique().tolist())
LAST_UPDATED   = datetime.now().strftime("%d %b %Y, %H:%M")

# ───────────────────────────────────────────────
#  SIDEBAR
# ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <div class="brand-name">📊 StartupPulse</div>
        <div class="brand-tag">Enterprise Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        "nav",
        ["🇮🇳   India Analysis", "🌍   World Analysis", "⚖️   Comparison"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="nav-label">Data Filters</div>', unsafe_allow_html=True)
    with st.expander("🎛️  Filter Data", expanded=False):
        sel_industries = st.multiselect(
            "Industry",
            options=ALL_INDUSTRIES,
            default=[],
            placeholder="All industries",
        )
        sel_countries = st.multiselect(
            "Country",
            options=ALL_COUNTRIES,
            default=[],
            placeholder="All countries",
        )

    # persist if expander collapsed (avoids losing state)
    if "sel_industries" not in st.session_state:
        st.session_state.sel_industries = []
    if "sel_countries" not in st.session_state:
        st.session_state.sel_countries = []

    if sel_industries: st.session_state.sel_industries = sel_industries
    if sel_countries:  st.session_state.sel_countries  = sel_countries

    # Show active filter pills
    active = (sel_industries or []) + (sel_countries or [])
    if active:
        pill_html = "".join(
            f"<span style='display:inline-block;background:{C['indigo_lt']};color:{C['indigo']};"
            f"font-size:0.7rem;font-weight:600;padding:2px 8px;border-radius:20px;"
            f"border:1px solid #c7d2fe;margin:2px 2px 0 0'>{a}</span>"
            for a in active[:6]
        )
        st.markdown(pill_html, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='margin-top:2rem;padding-top:1rem;border-top:1px solid {C["border"]}'>
        <div style='font-size:0.7rem;color:{C["slate_400"]};line-height:1.6'>
            <b>Dataset:</b> startupPulse_Master_Data_Final.csv<br>
            <b>Records:</b> {len(df_raw):,} startups<br>
            <b>Countries:</b> {df_raw['Country'].nunique()}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ───────────────────────────────────────────────
#  FILTER LOGIC (fallback to full data if empty)
# ───────────────────────────────────────────────
def apply_filters(df, industries, countries):
    out = df.copy()
    if industries:
        out = out[out["Industry"].isin(industries)]
    if countries:
        out = out[out["Country"].isin(countries)]
    return out if len(out) > 0 else df

df_filtered = apply_filters(df_raw, sel_industries, sel_countries)

# ───────────────────────────────────────────────
#  HELPER FUNCTIONS
# ───────────────────────────────────────────────
def kpi_card(label, value, sub, trend_html, accent="indigo", icon="📌"):
    return f"""
    <div class="kpi-card {accent}">
        <div class="kpi-icon {accent}">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-footer">{trend_html}<span>{sub}</span></div>
    </div>"""

def insight(text):
    return f"""
    <div class="insight-box">
        <span class="insight-icon">💡</span>
        <span class="insight-text">{text}</span>
    </div>"""

def chart_wrap(title, subtitle=""):
    sub_html = f'<div class="chart-sub">{subtitle}</div>' if subtitle else ""
    return f'<div class="chart-card"><div class="chart-title">{title}</div>{sub_html}'

def chart_cfg(fig, show_legend=True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=C["slate_600"], size=12),
        margin=dict(l=4, r=4, t=8, b=4),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left", x=0,
        ) if show_legend else dict(visible=False),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter",
            bordercolor=C["border"],
        ),
    )
    fig.update_xaxes(
        gridcolor=C["slate_100"],
        linecolor=C["border"],
        tickfont=dict(size=11),
        showline=False,
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor=C["slate_100"],
        linecolor=C["border"],
        tickfont=dict(size=11),
        showline=False,
        zeroline=False,
    )
    return fig

def download_csv(df, label="Download Report"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"⬇️  {label}",
        data=csv,
        file_name=f"startuppulse_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=False,
    )

def page_header(title, subtitle, df_for_download=None, download_label="Download Report"):
    ts_html = f'<div class="ph-timestamp">🕐 Last updated: {LAST_UPDATED}</div>'
    badge   = f'<div class="ph-badge"><span>●</span> Live Data</div>'
    st.markdown(f"""
    <div class="page-header">
        <div class="ph-left">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="ph-right">
            {ts_html}
            {badge}
        </div>
    </div>
    """, unsafe_allow_html=True)
    if df_for_download is not None:
        col_dl, _ = st.columns([1, 5])
        with col_dl:
            download_csv(df_for_download, download_label)

STAGE_ORDER = ["Pre-Seed", "Seed", "Series A", "Series B", "Series C", "IPO"]

# ═══════════════════════════════════════════════
#  PAGE 1 — INDIA ANALYSIS
# ═══════════════════════════════════════════════
if "India" in page:
    df_india_base = df_raw[df_raw["Country"] == "India"].copy()
    df_india = (
        df_india_base[df_india_base["Industry"].isin(sel_industries)]
        if sel_industries and len(df_india_base[df_india_base["Industry"].isin(sel_industries)]) > 0
        else df_india_base
    )

    page_header(
        "🇮🇳  India Startup Ecosystem",
        "Deep-dive into funding, growth trajectories and profitability of Indian startups.",
        df_india, "Download India Report",
    )

    # ── KPIs ──
    total_s   = len(df_india)
    total_f   = df_india["Total_Funding_MUSD"].sum()
    avg_g     = df_india["Revenue_Growth_Percent"].mean()
    prof_pct  = df_india["Is_Profitable"].mean() * 100
    global_share = total_s / len(df_raw) * 100

    kpi_html = f"""
    <div class="kpi-grid">
        {kpi_card("Total Startups", f"{total_s:,}",
                  f"{global_share:.1f}% of global dataset",
                  f'<span class="trend-dot">●</span>', "indigo", "🏢")}
        {kpi_card("Total Funding",  f"${total_f:,.0f}M",
                  f"Avg ${total_f/total_s:.1f}M per startup",
                  f'<span class="trend-up">↑</span>', "emerald", "💰")}
        {kpi_card("Avg Revenue Growth", f"{avg_g:.1f}%",
                  "Year-on-year average",
                  f'<span class="trend-up">↑</span>', "sky", "📈")}
    </div>"""
    st.markdown(kpi_html, unsafe_allow_html=True)

    st.markdown("<hr class='section-rule'>", unsafe_allow_html=True)

    # ── Charts row 1 ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(chart_wrap("Revenue Growth by Funding Stage",
                               "Average growth % at each investment milestone"), unsafe_allow_html=True)
        stage_g = (
            df_india.groupby("Funding_Stage")["Revenue_Growth_Percent"].mean()
            .reindex([s for s in STAGE_ORDER if s in df_india["Funding_Stage"].unique()])
            .reset_index()
        )
        fig = go.Figure()
        # Area-fill line chart with hollow markers
        fig.add_trace(go.Scatter(
            x=stage_g["Funding_Stage"], y=stage_g["Revenue_Growth_Percent"],
            mode="lines+markers", name="Avg Growth",
            line=dict(color=C["indigo"], width=4, shape="spline"),
            marker=dict(size=10, color="white", line=dict(width=2, color=C["indigo"])),
            fill="tozeroy",
            fillcolor="rgba(79,70,229,0.05)",
        ))
        fig.add_hline(
            y=stage_g["Revenue_Growth_Percent"].mean(),
            line_dash="dot", line_color=C["slate_400"], line_width=1,
            annotation_text=f"Mean {stage_g['Revenue_Growth_Percent'].mean():.1f}%",
            annotation_font=dict(size=10, color=C["slate_400"]),
        )
        chart_cfg(fig, show_legend=False)
        fig.update_xaxes(title_text="")
        fig.update_yaxes(title_text="Growth (%)", title_font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown(insight(
            f"Growth peaks at the <b>{stage_g.loc[stage_g['Revenue_Growth_Percent'].idxmax(), 'Funding_Stage']}</b> stage "
            f"({stage_g['Revenue_Growth_Percent'].max():.1f}%), suggesting capital influx accelerates revenue momentum."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(chart_wrap("Top Industries by Total Funding",
                               "Cumulative MUSD raised per sector"), unsafe_allow_html=True)
        top_ind = (
            df_india.groupby("Industry")["Total_Funding_MUSD"]
            .sum().nlargest(8).sort_values().reset_index()
        )
        fig = go.Figure(go.Bar(
            x=top_ind["Total_Funding_MUSD"],
            y=top_ind["Industry"],
            orientation="h",
            marker=dict(
                color=top_ind["Total_Funding_MUSD"],
                colorscale=[[0, C["indigo_lt"]], [1, C["indigo"]]],
                showscale=False,
                line=dict(width=0),
            ),
            text=[f"${v:,.0f}M" for v in top_ind["Total_Funding_MUSD"]],
            textposition="outside",
            textfont=dict(size=10, color=C["slate_600"]),
        ))
        chart_cfg(fig, show_legend=False)
        fig.update_xaxes(showgrid=False, showticklabels=False)
        fig.update_yaxes(tickfont=dict(size=11))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        top_sector = top_ind.iloc[-1]["Industry"]
        st.markdown(insight(
            f"<b>{top_sector}</b> leads Indian startup funding, capturing the largest share of total capital deployed."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Charts row 2 ──
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(chart_wrap("Profitability Breakdown",
                               "Share of profitable vs non-profitable startups"), unsafe_allow_html=True)
        pc = df_india["Is_Profitable"].value_counts().reset_index()
        pc.columns = ["Status", "Count"]
        pc["Status"] = pc["Status"].map({1: "Profitable", 0: "Not Profitable"})
        fig = go.Figure(go.Pie(
            labels=pc["Status"], values=pc["Count"],
            hole=0.60,
            marker=dict(
                colors=[C["emerald"], C["slate_100"]],
                line=dict(color="white", width=3),
            ),
            textinfo="percent",
            textfont=dict(size=13, color=C["slate_900"]),
            hoverinfo="label+percent+value",
        ))
        prof_val = pc.loc[pc["Status"] == "Profitable", "Count"].values
        p_pct    = (prof_val[0] / pc["Count"].sum() * 100) if len(prof_val) else 0
        fig.add_annotation(
            text=f"<b>{p_pct:.0f}%</b><br><span style='font-size:11px'>Profitable</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=C["slate_900"]),
            align="center",
        )
        chart_cfg(fig, show_legend=True)
        fig.update_layout(legend=dict(orientation="h", y=-0.05))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown(insight(
            f"<b>{p_pct:.0f}%</b> of Indian startups are profitable — "
            f"{'above' if p_pct > 50 else 'below'} the 50% threshold, indicating a "
            f"{'maturing' if p_pct > 50 else 'growth-focused, pre-profit'} ecosystem."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown(chart_wrap("Valuation vs Revenue",
                               "Bubble size = total funding raised"), unsafe_allow_html=True)
        samp = df_india.sample(min(350, len(df_india)), random_state=42)
        fig = px.scatter(
            samp,
            x="Annual_Revenue_MUSD", y="Valuation_MUSD",
            color="Industry", size="Total_Funding_MUSD",
            size_max=22, opacity=0.72,
            color_discrete_sequence=PALETTE,
            labels={"Annual_Revenue_MUSD": "Revenue (MUSD)", "Valuation_MUSD": "Valuation (MUSD)"},
        )
        chart_cfg(fig, show_legend=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        corr = samp[["Annual_Revenue_MUSD", "Valuation_MUSD"]].corr().iloc[0, 1]
        st.markdown(insight(
            f"Revenue and valuation show a <b>{'strong' if abs(corr) > 0.6 else 'moderate'} positive correlation "
            f"(r={corr:.2f})</b> — higher-revenue startups consistently attract premium valuations."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  PAGE 2 — WORLD ANALYSIS
# ═══════════════════════════════════════════════
elif "World" in page:
    df_world = df_filtered.copy()

    page_header(
        "🌍  Global Startup Landscape",
        "Worldwide overview of startup funding, valuations, and growth across all markets.",
        df_world, "Download Global Report",
    )

    # ── KPIs ──
    total_s  = len(df_world)
    total_f  = df_world["Total_Funding_MUSD"].sum()
    avg_g    = df_world["Revenue_Growth_Percent"].mean()

    kpi_html = f"""
    <div class="kpi-grid">
        {kpi_card("Global Startups", f"{total_s:,}",
                  f"Across {df_world['Country'].nunique()} countries",
                  f'<span class="trend-dot">●</span>', "indigo", "🌐")}
        {kpi_card("Total Capital Deployed", f"${total_f/1000:.2f}B",
                  f"Avg ${total_f/total_s:.1f}M per startup",
                  f'<span class="trend-up">↑</span>', "emerald", "💵")}
        {kpi_card("Avg Revenue Growth", f"{avg_g:.1f}%",
                  "Global mean across all sectors",
                  f'<span class="trend-up">↑</span>', "sky", "📊")}
    </div>"""
    st.markdown(kpi_html, unsafe_allow_html=True)

    st.markdown("<hr class='section-rule'>", unsafe_allow_html=True)

    # ── Chart 1 — Choropleth ──
    st.markdown(chart_wrap("Global Funding Distribution",
                           "Total MUSD raised by country — hover for details"), unsafe_allow_html=True)
    country_data = (
        df_world.groupby("Country")
        .agg(Startups=("Startup_ID", "count"), Funding=("Total_Funding_MUSD", "sum"),
             Avg_Valuation=("Valuation_MUSD", "mean"))
        .reset_index()
    )
    fig_map = px.choropleth(
        country_data, locations="Country", locationmode="country names",
        color="Funding", hover_name="Country",
        hover_data={"Startups": True, "Funding": ":.1f", "Avg_Valuation": ":.1f"},
        color_continuous_scale=[[0, "#eef2ff"], [0.3, "#a5b4fc"], [0.7, "#6366f1"], [1, "#3730a3"]],
        labels={"Funding": "Funding (MUSD)"},
    )
    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(248,250,252,0.5)", showframe=False,
                 showcoastlines=True, coastlinecolor=C["border"],
                 showland=True, landcolor=C["slate_50"],
                 showocean=True, oceancolor="#f0f9ff"),
        coloraxis_colorbar=dict(
            title="Funding (M)",
            thickness=12, len=0.6,
            tickfont=dict(size=10),
            title_font=dict(size=11),
        ),
        margin=dict(l=0, r=0, t=4, b=0),
        height=380,
    )
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
    top_country = country_data.nlargest(1, "Funding")["Country"].values[0]
    st.markdown(insight(
        f"<b>{top_country}</b> leads global startup funding, while emerging markets show increasing activity — "
        f"geographic diversification of capital is accelerating."
    ), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Charts row 2 ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(chart_wrap("Growth Trend by Funding Stage",
                               "How revenue growth evolves with investment maturity"), unsafe_allow_html=True)
        sg = (
            df_world.groupby("Funding_Stage")["Revenue_Growth_Percent"].mean()
            .reindex([s for s in STAGE_ORDER if s in df_world["Funding_Stage"].unique()])
            .reset_index()
        )
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sg["Funding_Stage"], y=sg["Revenue_Growth_Percent"],
            mode="lines+markers",
            line=dict(color=C["emerald"], width=3, shape="spline"),
            marker=dict(size=9, color=C["emerald"], line=dict(width=2, color="white")),
            fill="tozeroy", fillcolor="rgba(16,185,129,0.07)",
            name="Avg Growth",
        ))
        chart_cfg(fig, show_legend=False)
        fig.update_yaxes(title_text="Growth (%)", title_font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        peak_stage = sg.loc[sg["Revenue_Growth_Percent"].idxmax(), "Funding_Stage"]
        st.markdown(insight(
            f"Global startups peak at the <b>{peak_stage}</b> stage, mirroring the pattern where "
            f"institutional capital catalyses the strongest revenue acceleration."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(chart_wrap("Top 10 Countries by Average Valuation",
                               "Mean startup valuation (MUSD) per market"), unsafe_allow_html=True)
        top_c = (
            df_world.groupby("Country")["Valuation_MUSD"]
            .mean().nlargest(10).sort_values().reset_index()
        )
        fig = go.Figure(go.Bar(
            x=top_c["Valuation_MUSD"], y=top_c["Country"],
            orientation="h",
            marker=dict(
                color=top_c["Valuation_MUSD"],
                colorscale=[[0, C["emerald_lt"]], [1, C["emerald"]]],
                showscale=False, line=dict(width=0),
            ),
            text=[f"${v:,.0f}M" for v in top_c["Valuation_MUSD"]],
            textposition="outside",
            textfont=dict(size=10, color=C["slate_600"]),
        ))
        chart_cfg(fig, show_legend=False)
        fig.update_xaxes(showgrid=False, showticklabels=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        leader = top_c.iloc[-1]["Country"]
        st.markdown(insight(
            f"<b>{leader}</b> commands the highest average startup valuation globally, reflecting "
            f"either market maturity, sector concentration, or investor appetite in that region."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Chart 4 — Heatmap ──
    st.markdown(chart_wrap("Valuation Heatmap: Industry × Funding Stage",
                           "Average valuation (MUSD) — darker = higher"), unsafe_allow_html=True)
    ind_stage = (
        df_world.groupby(["Industry", "Funding_Stage"])["Valuation_MUSD"]
        .mean().unstack(fill_value=0)
    )
    ordered_cols = [c for c in STAGE_ORDER if c in ind_stage.columns]
    ind_stage    = ind_stage[ordered_cols]
    fig_heat = px.imshow(
        ind_stage,
        color_continuous_scale=[[0, "#f8fafc"], [0.3, "#c7d2fe"], [0.7, "#6366f1"], [1, "#3730a3"]],
        labels=dict(x="Stage", y="Industry", color="Avg Val."),
        aspect="auto",
        text_auto=".0f",
    )
    fig_heat.update_traces(textfont=dict(size=10))
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11),
        margin=dict(l=4, r=4, t=8, b=4),
        coloraxis_colorbar=dict(thickness=12, len=0.8, tickfont=dict(size=10)),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
    )
    fig_heat.update_xaxes(side="bottom", tickfont=dict(size=11), showline=False)
    fig_heat.update_yaxes(tickfont=dict(size=11), showline=False)
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})
    st.markdown(insight(
        "Late-stage (Series C / IPO) companies show dramatically higher valuations across all industries — "
        "compounding investor confidence as startups de-risk through successive funding rounds."
    ), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  PAGE 3 — COMPARISON
# ═══════════════════════════════════════════════
elif "Comparison" in page:
    df_cmp = df_filtered.copy()
    df_cmp["Region"] = df_cmp["Country"].apply(lambda x: "India" if x == "India" else "World")
    ind = df_cmp[df_cmp["Region"] == "India"]
    wld = df_cmp[df_cmp["Region"] == "World"]

    page_header(
        "⚖️  India vs World",
        "Head-to-head analysis of the Indian ecosystem against the global startup landscape.",
        df_cmp, "Download Comparison Report",
    )

    # ── KPIs ──
    ind_fund_delta = ((ind["Total_Funding_MUSD"].mean() - wld["Total_Funding_MUSD"].mean())
                      / wld["Total_Funding_MUSD"].mean() * 100)
    trend_fund = f'<span class="trend-up">↑</span>' if ind_fund_delta > 0 else f'<span class="trend-down">↓</span>'

    kpi_html = f"""
    <div class="kpi-grid">
        {kpi_card("India vs World Startups", f"{len(ind):,}",
                  f"World excl. India: {len(wld):,}",
                  f'<span class="trend-dot">●</span>', "indigo", "📍")}
        {kpi_card("India Avg Funding", f"${ind['Total_Funding_MUSD'].mean():.1f}M",
                  f"World avg: ${wld['Total_Funding_MUSD'].mean():.1f}M",
                  trend_fund, "emerald", "💰")}
        {kpi_card("India Profitable %", f"{ind['Is_Profitable'].mean()*100:.1f}%",
                  f"World: {wld['Is_Profitable'].mean()*100:.1f}%",
                  f'<span class="trend-up">↑</span>', "sky", "✅")}
    </div>"""
    st.markdown(kpi_html, unsafe_allow_html=True)

    st.markdown("<hr class='section-rule'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Chart 1 — Slim grouped bar
        st.markdown(chart_wrap("Key Metrics: India vs World",
                               "Average values in MUSD across core financial indicators"), unsafe_allow_html=True)
        metrics    = ["Total_Funding_MUSD", "Annual_Revenue_MUSD", "Valuation_MUSD", "Burn_Rate_MUSD"]
        met_labels = ["Funding", "Revenue", "Valuation", "Burn Rate"]
        india_vals = [ind[m].mean() for m in metrics]
        world_vals = [wld[m].mean() for m in metrics]
        fig = go.Figure(data=[
            go.Bar(
                name="India", x=met_labels, y=india_vals,
                marker=dict(color=C["indigo"], opacity=0.9, line=dict(width=0)),
                width=0.32,
                text=[f"${v:.0f}M" for v in india_vals],
                textposition="outside", textfont=dict(size=10),
            ),
            go.Bar(
                name="World", x=met_labels, y=world_vals,
                marker=dict(color=C["slate_400"], opacity=0.85, line=dict(width=0)),
                width=0.32,
                text=[f"${v:.0f}M" for v in world_vals],
                textposition="outside", textfont=dict(size=10),
            ),
        ])
        fig.update_layout(
            barmode="group", bargap=0.3, bargroupgap=0.08,
            uniformtext_minsize=9,
        )
        chart_cfg(fig)
        fig.update_yaxes(title_text="MUSD", title_font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        best_metric = met_labels[
            int(np.argmax([i - w for i, w in zip(india_vals, world_vals)]))]
        st.markdown(insight(
            f"India outperforms the world most notably in <b>{best_metric}</b> — "
            f"a signal of stronger unit economics or more targeted capital deployment in this dimension."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Chart 2 — Radar chart
        st.markdown(chart_wrap("Performance Radar",
                               "Normalised scores across 5 key dimensions (0–100 scale)"), unsafe_allow_html=True)
        radar_metrics = ["Total_Funding_MUSD", "Annual_Revenue_MUSD",
                         "Valuation_MUSD", "Revenue_Growth_Percent", "Is_Profitable"]
        radar_labels  = ["Funding", "Revenue", "Valuation", "Growth", "Profitability"]

        def norm_series(df_a, df_b, col):
            combined_max = max(df_a[col].mean(), df_b[col].mean())
            if combined_max == 0:
                return 50, 50
            return (df_a[col].mean() / combined_max * 100,
                    df_b[col].mean() / combined_max * 100)

        india_radar, world_radar = zip(*[norm_series(ind, wld, m) for m in radar_metrics])
        cats = radar_labels + [radar_labels[0]]
        iv   = list(india_radar) + [india_radar[0]]
        wv   = list(world_radar) + [world_radar[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=iv, theta=cats, name="India", fill="toself",
            line=dict(color=C["indigo"], width=2),
            fillcolor="rgba(79,70,229,0.12)",
            marker=dict(size=6, color=C["indigo"]),
        ))
        fig.add_trace(go.Scatterpolar(
            r=wv, theta=cats, name="World", fill="toself",
            line=dict(color=C["slate_400"], width=2),
            fillcolor="rgba(148,163,184,0.12)",
            marker=dict(size=6, color=C["slate_400"]),
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, range=[0, 110],
                    gridcolor=C["slate_100"], linecolor=C["border"],
                    tickfont=dict(size=9, color=C["slate_400"]),
                    showticklabels=True,
                ),
                angularaxis=dict(
                    linecolor=C["border"], gridcolor=C["slate_100"],
                    tickfont=dict(size=11, color=C["slate_600"]),
                ),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h", y=1.12, x=0.5, xanchor="center",
                bgcolor="rgba(0,0,0,0)", font=dict(size=11),
            ),
            margin=dict(l=30, r=30, t=30, b=10),
            hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        strongest_dim = radar_labels[int(np.argmax([i - w for i, w in zip(india_radar, world_radar)]))]
        st.markdown(insight(
            f"India's radar profile shows its strongest advantage in <b>{strongest_dim}</b> relative "
            f"to the global baseline — a key competitive differentiator for the ecosystem."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        # Chart 3 — Box plot
        st.markdown(chart_wrap("Valuation Distribution",
                               "Statistical spread — box shows IQR, whiskers show range"), unsafe_allow_html=True)
        fig = go.Figure()
        for region, color, lt in [("India", C["indigo"], C["indigo_lt"]),
                                   ("World", C["slate_400"], C["slate_100"])]:
            vals = df_cmp.loc[df_cmp["Region"] == region, "Valuation_MUSD"]
            fig.add_trace(go.Box(
                y=vals, name=region,
                marker=dict(color=color, opacity=0.8, size=4,
                            outliercolor=color, symbol="circle-open"),
                line=dict(color=color, width=2),
                fillcolor=lt,
                boxmean="sd",
                whiskerwidth=0.5,
            ))
        chart_cfg(fig)
        fig.update_yaxes(title_text="Valuation (MUSD)", title_font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        ind_med = ind["Valuation_MUSD"].median()
        wld_med = wld["Valuation_MUSD"].median()
        higher  = "India" if ind_med > wld_med else "World"
        st.markdown(insight(
            f"<b>{higher}</b> has the higher median valuation "
            f"(India ${ind_med:.0f}M vs World ${wld_med:.0f}M) — "
            f"though both distributions show significant high-value outliers."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        # Chart 4 — Profitability % by industry, slim grouped bars
        st.markdown(chart_wrap("Profitability Rate by Industry",
                               "% of profitable startups per sector: India vs World"), unsafe_allow_html=True)
        top_inds = df_cmp["Industry"].value_counts().nlargest(7).index.tolist()
        prof_df  = (
            df_cmp[df_cmp["Industry"].isin(top_inds)]
            .groupby(["Industry", "Region"])["Is_Profitable"]
            .mean().mul(100).reset_index()
        )
        fig = px.bar(
            prof_df, x="Industry", y="Is_Profitable",
            color="Region", barmode="group",
            color_discrete_map={"India": C["indigo"], "World": C["slate_400"]},
            labels={"Is_Profitable": "Profitable (%)", "Industry": ""},
            text_auto=".0f",
        )
        fig.update_traces(width=0.35, marker_line_width=0, textfont=dict(size=9),
                          textposition="outside")
        fig.update_layout(bargap=0.35, bargroupgap=0.1, uniformtext_minsize=9)
        chart_cfg(fig)
        fig.update_xaxes(tickangle=-28, tickfont=dict(size=10))
        fig.update_yaxes(title_text="Profitable (%)", title_font=dict(size=11), range=[0, 115])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        top_ind_india = (
            prof_df[prof_df["Region"] == "India"]
            .nlargest(1, "Is_Profitable")["Industry"].values[0]
            if not prof_df[prof_df["Region"] == "India"].empty else "N/A"
        )
        st.markdown(insight(
            f"<b>{top_ind_india}</b> leads Indian profitability rates sector-by-sector — "
            f"comparing sectors reveals where India's operational efficiency most exceeds the global norm."
        ), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)