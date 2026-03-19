import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="헬륨기밀검사 EDA",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# GLOBAL THEME
# ──────────────────────────────────────────────
ACCENT   = "#00D4FF"   # cyan
ACCENT2  = "#FF6B35"   # orange
WARN     = "#FFB703"   # amber
DANGER   = "#EF233C"   # red
BG_CARD  = "#0D1117"
BG_DEEP  = "#060A0F"
GRID     = "#1A2332"
TEXT_DIM = "#6B7A90"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'Noto Sans KR', sans-serif", color="#C9D1D9", size=12),
    margin=dict(l=16, r=16, t=36, b=16),
    xaxis=dict(showgrid=False, linecolor=GRID, tickcolor=GRID, zeroline=False),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, tickcolor=GRID, zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID, borderwidth=1),
    hoverlabel=dict(bgcolor="#1A2332", bordercolor=ACCENT, font_size=13),
)

# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

/* root */
html, body, [class*="css"] {
    background-color: #060A0F;
    color: #C9D1D9;
    font-family: 'Noto Sans KR', sans-serif;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem; max-width: 1400px; }

/* sidebar */
[data-testid="stSidebar"] {
    background: #0A0E16;
    border-right: 1px solid #1A2332;
}
[data-testid="stSidebar"] .stRadio > label { color: #6B7A90; font-size: 0.7rem; letter-spacing: .1em; text-transform: uppercase; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    color: #8B9BB4;
    font-size: 0.88rem;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    transition: all .18s;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { background: #111827; color: #C9D1D9; }

/* page title */
.page-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #E6EDF3;
    line-height: 1.2;
}
.page-sub {
    font-size: 0.82rem;
    color: #6B7A90;
    margin-top: .25rem;
    letter-spacing: .04em;
}

/* metric cards */
.metric-card {
    background: linear-gradient(135deg, #0D1117 0%, #111827 100%);
    border: 1px solid #1A2332;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent, #00D4FF);
}
.metric-label { font-size: 0.7rem; color: #6B7A90; letter-spacing: .1em; text-transform: uppercase; margin-bottom: .4rem; }
.metric-value { font-family: 'Space Mono', monospace; font-size: 1.8rem; color: #E6EDF3; font-weight: 700; line-height: 1; }
.metric-delta { font-size: 0.78rem; color: #00D4FF; margin-top: .35rem; }

/* info / warn / danger banner */
.banner {
    border-radius: 8px;
    padding: .75rem 1rem;
    font-size: 0.85rem;
    border-left: 3px solid;
    margin: .5rem 0;
}
.banner-info  { background: #0D1F2D; border-color: #00D4FF; color: #7DCFEE; }
.banner-warn  { background: #1F1A0D; border-color: #FFB703; color: #EEC96B; }
.banner-danger{ background: #1F0D10; border-color: #EF233C; color: #EE7B8A; }

/* table */
.stDataFrame { border: 1px solid #1A2332; border-radius: 8px; overflow: hidden; }
thead tr th { background: #0D1117 !important; color: #6B7A90 !important; font-size: .75rem; letter-spacing: .08em; }
tbody tr:hover td { background: #111827 !important; }

/* divider */
.divider { border: none; border-top: 1px solid #1A2332; margin: 1.5rem 0; }

/* insight pill */
.insight-item {
    display: flex; gap: .75rem; align-items: flex-start;
    background: #0D1117; border: 1px solid #1A2332;
    border-radius: 8px; padding: .75rem 1rem;
    margin-bottom: .5rem; font-size: 0.88rem; color: #C9D1D9;
    transition: border-color .18s;
}
.insight-item:hover { border-color: #00D4FF44; }
.insight-num {
    font-family: 'Space Mono', monospace;
    font-size: .65rem; color: #00D4FF;
    background: #00D4FF15; border-radius: 4px;
    padding: .1rem .4rem; flex-shrink: 0; margin-top: .1rem;
}

/* section label */
.section-label {
    font-size: .7rem; letter-spacing: .12em; text-transform: uppercase;
    color: #6B7A90; margin-bottom: .75rem;
    display: flex; align-items: center; gap: .5rem;
}
.section-label::after {
    content: ''; flex: 1; height: 1px; background: #1A2332;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────
monthly_df = pd.DataFrame({
    "month": ["2024-10","2024-11","2024-12","2025-01","2025-02","2025-03",
               "2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10"],
    "defect_count": [85, 92, 180, 230, 140, 120, 115, 165, 190, 135, 125, 118, 110]
})

product_df = pd.DataFrame({
    "product": ["P890","Q890","P880","Q880","기타"],
    "defect_count": [320, 280, 150, 120, 90]
})

pareto_df = pd.DataFrame({
    "defect_type": ["RH누설","LF누설","FLUX미도포","핀드랍","이물낙하","기타"],
    "count": [240, 180, 110, 95, 70, 55]
})
pareto_df["ratio"]    = pareto_df["count"] / pareto_df["count"].sum()
pareto_df["cum_ratio"] = pareto_df["ratio"].cumsum()

zone_temp_df = pd.DataFrame({
    "zone": ["Zone1","Zone2","Zone3","Zone4","Zone5","Zone6"],
    "avg_temp": [610, 625, 638, 645, 710, 650],
    "note": ["정상","정상","정상","정상","이상치 의심","정상"]
})

corr_df = pd.DataFrame({
    "variable": ["온도","압력","시간","속도"],
    "corr_with_defect": [0.18, 0.22, 0.15, -0.28]
})

insight_data = [
    "브레이징 공정은 전체 기간 중 가장 큰 변동성을 보임",
    "2024-12 ~ 2025-01 구간에서 1차 불량 피크가 확인됨",
    "2025-05 ~ 2025-06 구간에서 2차 상승 패턴이 나타남",
    "P890, Q890 계열 제품군에서 불량 집중도가 높음",
    "핵심 불량은 RH누설, LF누설, FLUX미도포, 핀드랍으로 요약 가능",
    "Zone5 온도는 다른 구간 대비 이상치 가능성이 있어 센서 점검 필요",
    "속도 변수는 불량과 음의 상관을 보여 저속 조건 재점검이 필요함",
]

improvement_data = [
    ("누설 불량 원인 세분화", "재현실험 및 원인 Tree 구성"),
    ("FLUX 도포 관리 강화",  "도포량·패턴 SPC 관리 적용"),
    ("Zone5 센서 점검",       "제어 기준값 재설정 검토"),
    ("저속 조건 최적화",       "P890 / Q890 계열 조건 실험"),
    ("분석 확장",              "RandomForest · SPC · 이상탐지 적용"),
]


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def card_metric(label, value, delta=None, accent=ACCENT):
    delta_html = f'<div class="metric-delta">▲ {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card" style="--accent:{accent}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>""", unsafe_allow_html=True)


def banner(text, kind="info"):
    icons = {"info": "ℹ", "warn": "⚠", "danger": "✕"}
    st.markdown(f'<div class="banner banner-{kind}">{icons[kind]}&nbsp; {text}</div>',
                unsafe_allow_html=True)


def section(label):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)


def apply_layout(fig, title=""):
    fig.update_layout(**PLOTLY_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=13, color="#6B7A90"), x=0))
    return fig


# ──────────────────────────────────────────────
# CHART BUILDERS
# ──────────────────────────────────────────────
def chart_monthly():
    fig = go.Figure()
    # area fill
    fig.add_trace(go.Scatter(
        x=monthly_df["month"], y=monthly_df["defect_count"],
        fill="tozeroy", fillcolor="rgba(0,212,255,0.06)",
        line=dict(color=ACCENT, width=2.5),
        mode="lines+markers",
        marker=dict(size=7, color=ACCENT, line=dict(width=2, color=BG_DEEP)),
        hovertemplate="<b>%{x}</b><br>불량: %{y}건<extra></extra>",
    ))
    # peak annotation
    peak_idx = monthly_df["defect_count"].idxmax()
    fig.add_annotation(
        x=monthly_df.loc[peak_idx, "month"],
        y=monthly_df.loc[peak_idx, "defect_count"],
        text=f"  PEAK {monthly_df.loc[peak_idx, 'defect_count']}건",
        showarrow=True, arrowhead=2, arrowcolor=DANGER,
        font=dict(color=DANGER, size=11), arrowwidth=1.5,
        ax=40, ay=-30,
    )
    apply_layout(fig, "월별 불량 추이")
    fig.update_xaxes(tickangle=-35, tickfont=dict(size=10))
    return fig


def chart_product():
    colors = [ACCENT if p in ("P890","Q890") else "#2E4057" for p in product_df["product"]]
    fig = go.Figure(go.Bar(
        x=product_df["product"], y=product_df["defect_count"],
        marker=dict(color=colors, line=dict(width=0), cornerradius=4),
        text=product_df["defect_count"],
        textposition="outside",
        textfont=dict(color="#C9D1D9", size=11),
        hovertemplate="<b>%{x}</b><br>불량: %{y}건<extra></extra>",
    ))
    apply_layout(fig, "제품별 불량 건수")
    fig.update_yaxes(range=[0, product_df["defect_count"].max() * 1.25])
    return fig


def chart_pareto():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    bar_colors = [DANGER if i < 4 else "#2E4057" for i in range(len(pareto_df))]
    fig.add_trace(go.Bar(
        x=pareto_df["defect_type"], y=pareto_df["count"],
        marker=dict(color=bar_colors, cornerradius=4, line=dict(width=0)),
        text=pareto_df["count"],
        textposition="outside", textfont=dict(color="#C9D1D9", size=11),
        hovertemplate="<b>%{x}</b><br>건수: %{y}<extra></extra>",
        name="불량 건수",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=pareto_df["defect_type"], y=pareto_df["cum_ratio"] * 100,
        mode="lines+markers",
        line=dict(color=WARN, width=2.5, dash="dot"),
        marker=dict(size=7, color=WARN, line=dict(width=2, color=BG_DEEP)),
        hovertemplate="<b>%{x}</b><br>누적: %{y:.1f}%<extra></extra>",
        name="누적 비율",
    ), secondary_y=True)
    # 80% line
    fig.add_hline(y=80, line=dict(color="#FFFFFF22", width=1, dash="dash"), secondary_y=True)
    fig.add_annotation(x=5.4, y=80, yref="y2", text="80%", showarrow=False,
                        font=dict(color=WARN, size=10))
    apply_layout(fig, "불량유형 Pareto Chart")
    fig.update_yaxes(secondary_y=True, range=[0, 115], ticksuffix="%", gridcolor="rgba(0,0,0,0)")
    return fig


def chart_zone():
    colors = [DANGER if n == "이상치 의심" else ACCENT for n in zone_temp_df["note"]]
    fig = go.Figure(go.Bar(
        x=zone_temp_df["zone"], y=zone_temp_df["avg_temp"],
        marker=dict(color=colors, cornerradius=4, line=dict(width=0)),
        text=zone_temp_df["avg_temp"].astype(str) + "°C",
        textposition="outside", textfont=dict(color="#C9D1D9", size=11),
        hovertemplate="<b>%{x}</b><br>온도: %{y}°C<extra></extra>",
    ))
    # reference line
    normal_mean = zone_temp_df.loc[zone_temp_df["note"]=="정상","avg_temp"].mean()
    fig.add_hline(y=normal_mean, line=dict(color=WARN, width=1.5, dash="dash"))
    fig.add_annotation(x=5.4, y=normal_mean + 5, text=f"정상 평균 {normal_mean:.0f}°C",
                        showarrow=False, font=dict(color=WARN, size=10))
    apply_layout(fig, "Zone별 평균 온도")
    fig.update_yaxes(range=[580, 750])
    return fig


def chart_corr():
    colors = [DANGER if v > 0 else ACCENT for v in corr_df["corr_with_defect"]]
    fig = go.Figure(go.Bar(
        x=corr_df["variable"], y=corr_df["corr_with_defect"],
        marker=dict(color=colors, cornerradius=4, line=dict(width=0)),
        text=[f"{v:+.2f}" for v in corr_df["corr_with_defect"]],
        textposition="outside", textfont=dict(color="#C9D1D9", size=12),
        hovertemplate="<b>%{x}</b><br>상관: %{y:+.2f}<extra></extra>",
    ))
    fig.add_hline(y=0, line=dict(color=GRID, width=1))
    apply_layout(fig, "공정변수 vs 불량 상관계수")
    fig.update_yaxes(range=[-0.42, 0.42])
    return fig


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:.75rem 0 1.25rem">
        <div style="font-family:'Space Mono',monospace;font-size:1rem;color:#E6EDF3;font-weight:700;letter-spacing:-.01em;">
            ⬡ HELIUM EDA
        </div>
        <div style="font-size:.7rem;color:#6B7A90;margin-top:.2rem;letter-spacing:.06em;">
            기밀검사 불량 분석 대시보드
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #1A2332;margin-bottom:1rem">
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        ["대시보드 개요", "월별 불량 추이", "제품별 불량", "불량유형 Pareto",
         "Zone 온도 점검", "공정변수 상관", "핵심 인사이트", "데이터 업로드"],
        label_visibility="visible",
    )

    st.markdown("""
    <hr style="border:none;border-top:1px solid #1A2332;margin:1.5rem 0 .75rem">
    <div style="font-size:.68rem;color:#3D4F63;line-height:1.6">
        보고서 기반 샘플 데이터<br>
        실데이터 적용 시 업로드 탭 이용
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGES
# ──────────────────────────────────────────────

# ── 1. 대시보드 개요 ──────────────────────────
if page == "대시보드 개요":
    st.markdown('<div class="page-title">대시보드 개요</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">헬륨기밀검사 불량 탐색적 데이터 분석 · Prototype v1</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    section("핵심 지표")
    c1, c2, c3, c4 = st.columns(4)
    with c1: card_metric("총 불량 건수", f"{int(monthly_df['defect_count'].sum()):,}", accent=ACCENT)
    with c2: card_metric("월 최대 불량", str(int(monthly_df['defect_count'].max())), accent=DANGER)
    with c3: card_metric("주요 제품군", "P890 / Q890", accent=ACCENT2)
    with c4: card_metric("점검 필요 Zone", "Zone 5", accent=WARN)

    st.markdown('<br>', unsafe_allow_html=True)
    section("월별 불량 추이 미리보기")
    st.plotly_chart(chart_monthly(), use_container_width=True, config={"displayModeBar": False})

    banner("분석 기간: 2024-10 ~ 2025-10 | 브레이징 공정 중심 불량 패턴", "info")


# ── 2. 월별 불량 추이 ─────────────────────────
elif page == "월별 불량 추이":
    st.markdown('<div class="page-title">월별 불량 추이</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    peak_month = monthly_df.loc[monthly_df["defect_count"].idxmax(), "month"]
    peak_value = int(monthly_df["defect_count"].max())
    section("트렌드 차트")
    st.plotly_chart(chart_monthly(), use_container_width=True, config={"displayModeBar": False})
    banner(f"최대 불량 시점: {peak_month} — {peak_value}건 | 1차 피크(2024-12 ~ 2025-01) 이후 2차 상승(2025-05~06) 패턴", "warn")

    st.markdown('<br>', unsafe_allow_html=True)
    section("원시 데이터")
    st.dataframe(monthly_df.rename(columns={"month":"월","defect_count":"불량 건수"}),
                 use_container_width=True, hide_index=True)


# ── 3. 제품별 불량 ────────────────────────────
elif page == "제품별 불량":
    st.markdown('<div class="page-title">제품별 불량 현황</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    top_product = product_df.loc[product_df["defect_count"].idxmax(), "product"]
    section("제품별 분포")
    st.plotly_chart(chart_product(), use_container_width=True, config={"displayModeBar": False})
    banner(f"최고 불량 제품: {top_product} — P890·Q890 계열이 전체의 약 63%를 차지", "info")

    st.markdown('<br>', unsafe_allow_html=True)
    section("원시 데이터")
    st.dataframe(product_df.rename(columns={"product":"제품","defect_count":"불량 건수"}),
                 use_container_width=True, hide_index=True)


# ── 4. 불량유형 Pareto ────────────────────────
elif page == "불량유형 Pareto":
    st.markdown('<div class="page-title">불량유형 Pareto 분석</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    top_defect = pareto_df.iloc[0]["defect_type"]
    top_ratio  = round(pareto_df.iloc[0]["ratio"] * 100, 1)
    section("Pareto Chart")
    st.plotly_chart(chart_pareto(), use_container_width=True, config={"displayModeBar": False})
    banner(f"최대 비중: {top_defect} ({top_ratio}%) | 상위 4개 유형이 전체 불량의 약 83%를 차지", "warn")

    st.markdown('<br>', unsafe_allow_html=True)
    section("원시 데이터")
    disp = pareto_df[["defect_type","count","ratio","cum_ratio"]].copy()
    disp.columns = ["불량유형","건수","비율","누적비율"]
    disp["비율"]   = disp["비율"].map("{:.1%}".format)
    disp["누적비율"] = disp["누적비율"].map("{:.1%}".format)
    st.dataframe(disp, use_container_width=True, hide_index=True)


# ── 5. Zone 온도 점검 ─────────────────────────
elif page == "Zone 온도 점검":
    st.markdown('<div class="page-title">Zone별 온도 점검</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    section("Zone 온도 분포")
    st.plotly_chart(chart_zone(), use_container_width=True, config={"displayModeBar": False})

    abnormal = zone_temp_df[zone_temp_df["note"].str.contains("이상치", na=False)]
    if not abnormal.empty:
        banner("이상치 의심 Zone이 감지됐습니다. 센서 및 공정 제어 조건 점검이 필요합니다.", "danger")
        st.markdown('<br>', unsafe_allow_html=True)
        section("이상 구간")
        st.dataframe(abnormal.rename(columns={"zone":"Zone","avg_temp":"평균온도(°C)","note":"비고"}),
                     use_container_width=True, hide_index=True)

    st.markdown('<br>', unsafe_allow_html=True)
    section("전체 Zone 데이터")
    st.dataframe(zone_temp_df.rename(columns={"zone":"Zone","avg_temp":"평균온도(°C)","note":"비고"}),
                 use_container_width=True, hide_index=True)


# ── 6. 공정변수 상관 ──────────────────────────
elif page == "공정변수 상관":
    st.markdown('<div class="page-title">공정변수 × 불량 상관 분석</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    section("상관계수 차트")
    st.plotly_chart(chart_corr(), use_container_width=True, config={"displayModeBar": False})

    col1, col2 = st.columns(2)
    with col1:
        banner("양(+) 방향 변수: 온도·압력·시간 — 불량 증가와 연관", "warn")
    with col2:
        banner("음(−) 방향 변수: 속도 — 저속 조건에서 불량 증가 경향", "info")

    st.markdown('<br>', unsafe_allow_html=True)
    section("원시 데이터")
    st.dataframe(corr_df.rename(columns={"variable":"공정변수","corr_with_defect":"불량 상관계수"}),
                 use_container_width=True, hide_index=True)


# ── 7. 핵심 인사이트 ──────────────────────────
elif page == "핵심 인사이트":
    st.markdown('<div class="page-title">핵심 인사이트</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    section("분석 요약")
    for i, item in enumerate(insight_data, 1):
        st.markdown(f"""
        <div class="insight-item">
            <span class="insight-num">0{i}</span>
            <span>{item}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    section("개선 방향")
    for label, detail in improvement_data:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f'<div style="font-size:.88rem;color:{ACCENT};font-weight:500;">{label}</div>',
                        unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="font-size:.85rem;color:#8B9BB4;padding-top:.05rem;">{detail}</div>',
                        unsafe_allow_html=True)
        st.markdown('<hr style="border:none;border-top:1px solid #0F1922;margin:.4rem 0">', unsafe_allow_html=True)


# ── 8. 데이터 업로드 ──────────────────────────
elif page == "데이터 업로드":
    st.markdown('<div class="page-title">실데이터 업로드</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    section("파일 업로드")
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요",
                                     type=["csv","xlsx"],
                                     label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") \
                 else pd.read_excel(uploaded_file)

            banner(f"'{uploaded_file.name}' 업로드 완료 — {len(df):,}행 × {len(df.columns)}열", "info")
            st.markdown('<br>', unsafe_allow_html=True)

            section("데이터 미리보기 (상위 10행)")
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)

            st.markdown('<br>', unsafe_allow_html=True)
            section("컬럼 목록")
            cols = st.columns(min(len(df.columns), 4))
            for i, col in enumerate(df.columns):
                with cols[i % len(cols)]:
                    dtype = str(df[col].dtype)
                    st.markdown(f"""
                    <div style="background:#0D1117;border:1px solid #1A2332;border-radius:6px;
                                padding:.5rem .75rem;margin-bottom:.4rem;font-size:.8rem;">
                        <span style="color:#C9D1D9">{col}</span>
                        <span style="color:#3D4F63;font-size:.7rem;margin-left:.4rem">{dtype}</span>
                    </div>""", unsafe_allow_html=True)

            st.markdown('<br>', unsafe_allow_html=True)
            section("다음 단계 제안")
            steps = [
                "월 · 제품 · 불량유형 · 공정변수 컬럼 매핑",
                "현재 샘플 차트를 실데이터 기반으로 교체",
                "제품군 · 기간 · 불량유형 필터 추가",
                "이상치 탐지 및 머신러닝 모델링 탭 확장",
            ]
            for s in steps:
                st.markdown(f'<div class="insight-item"><span class="insight-num">→</span><span>{s}</span></div>',
                            unsafe_allow_html=True)

        except Exception as e:
            banner(f"파일 읽기 오류: {e}", "danger")

    else:
        st.markdown("""
        <div style="background:#0D1117;border:1px solid #1A2332;border-radius:10px;
                    padding:2.5rem;text-align:center;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:.75rem;opacity:.4">⬡</div>
            <div style="color:#6B7A90;font-size:.88rem;line-height:1.7">
                현재 보고서 기반 샘플 데이터가 표시 중입니다.<br>
                실데이터 CSV / Excel 파일을 업로드하면 전체 대시보드가 갱신됩니다.
            </div>
        </div>""", unsafe_allow_html=True)
