import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os

warnings.filterwarnings('ignore')

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="따릉이 데이터 시각화 완전 정복",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 한글 폰트 설정 ───────────────────────────────────────
@st.cache_resource
def setup_font():
    """시스템에서 사용 가능한 한글 폰트를 탐색하여 설정"""
    font_candidates = [
        'NanumGothic', 'NanumBarunGothic', 'NanumBarunpen',
        'Malgun Gothic', 'AppleGothic', 'DejaVu Sans'
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for font in font_candidates:
        if font in available:
            plt.rcParams['font.family'] = font
            return font
    plt.rcParams['font.family'] = 'DejaVu Sans'
    return 'DejaVu Sans'

chosen_font = setup_font()
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(font=chosen_font, font_scale=1.0)

# ── CSS 스타일 ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 전체 배경 */
.stApp {
    background: #0f1117;
    color: #e8eaf0;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1d2e 0%, #0f1117 100%);
    border-right: 1px solid #2a2d3e;
}

/* 헤더 */
.main-header {
    background: linear-gradient(135deg, #1a1d2e 0%, #0d1b2a 100%);
    border: 1px solid #2a3f5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(56,189,248,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.main-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #38bdf8;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: #94a3b8;
    margin: 0;
    font-size: 0.95rem;
}

/* 섹션 카드 */
.section-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* 코드 블록 */
.code-block {
    background: #0d1117;
    border: 1px solid #30363d;
    border-left: 3px solid #38bdf8;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #e6edf3;
    overflow-x: auto;
    white-space: pre;
    line-height: 1.6;
    margin: 0.8rem 0;
}

/* KPI 카드 */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1rem 0;
}
.kpi-card {
    background: linear-gradient(135deg, #1e2a3a 0%, #1a1d2e 100%);
    border: 1px solid #2a3f5f;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #38bdf8;
}
.kpi-label {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 0.3rem;
}

/* 정보 박스 */
.info-box {
    background: rgba(56,189,248,0.07);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #94a3b8;
}
.warn-box {
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #94a3b8;
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1d2e;
    border-radius: 8px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #64748b;
    border-radius: 6px;
    font-size: 0.85rem;
}
.stTabs [aria-selected="true"] {
    background: #38bdf8 !important;
    color: #0f1117 !important;
    font-weight: 600;
}

/* 스크롤바 */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1a1d2e; }
::-webkit-scrollbar-thumb { background: #2a3f5f; border-radius: 3px; }

/* Streamlit 기본 요소 재정의 */
h1, h2, h3 { color: #e2e8f0 !important; }
.stMarkdown p { color: #94a3b8; }
[data-testid="metric-container"] {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 10px;
    padding: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ── 데이터 로드 ──────────────────────────────────────────
@st.cache_data
def load_data():
    """샘플 데이터 생성 (실제 CSV 없을 경우 시뮬레이션)"""
    rent_path = "./data/서울특별시 공공자전거 대여이력 정보_2512.csv"
    station_path = "./data/공공자전거 대여소 정보(25.12월 기준).csv"

    def file_ok(path):
        return os.path.exists(path) and os.path.getsize(path) > 1024

    use_sample = True
    if file_ok(rent_path) and file_ok(station_path):
        try:
            rent = pd.read_csv(rent_path, encoding='cp949', encoding_errors='replace', low_memory=False)
            station = pd.read_csv(station_path, encoding='utf-8')
            if rent.empty or station.empty:
                raise ValueError("빈 파일")
            rent.columns = [
                '자전거번호','대여일시','대여소번호','대여소명','대여거치대',
                '반납일시','반납소번호','반납소명','반납거치대','이용시간',
                '이용거리','생년','성별','이용자종류','대여소ID','반납소ID','자전거구분'
            ]
            station.columns = [
                '대여소번호','대여소명','자치구','상세주소','위도','경도','설치시기','거치대수','기타'
            ]
            use_sample = False
        except Exception:
            rent, station = generate_sample_data()
    else:
        rent, station = generate_sample_data()

    # 전처리
    rent['성별'] = rent['성별'].fillna('알수없음').str.upper()
    rent.loc[rent['성별'].isin(['\\N', '내국인']), '성별'] = '알수없음'
    mode_val = rent['자전거구분'].mode()[0]
    rent['자전거구분'] = rent['자전거구분'].fillna(mode_val)
    invalid_mask = rent['이용자종류'].str.startswith('ST-', na=False)
    rent.loc[invalid_mask, '이용자종류'] = '알수없음'

    Q1 = rent['이용시간'].quantile(0.25)
    Q3 = rent['이용시간'].quantile(0.75)
    IQR = Q3 - Q1
    rent = rent[(rent['이용시간'] >= Q1 - 1.5*IQR) & (rent['이용시간'] <= Q3 + 1.5*IQR)].copy()

    rent['대여일시'] = pd.to_datetime(rent['대여일시'])
    rent['시간대'] = rent['대여일시'].dt.hour
    rent['요일'] = rent['대여일시'].dt.dayofweek
    rent['요일명'] = rent['대여일시'].dt.day_name()
    rent['일자'] = rent['대여일시'].dt.day

    def time_label(h):
        if 6 <= h < 12: return '오전(6~12시)'
        elif 12 <= h < 18: return '오후(12~18시)'
        elif 18 <= h < 22: return '저녁(18~22시)'
        else: return '심야(22~6시)'
    rent['시간구분'] = rent['시간대'].apply(time_label)

    dow_kor = {'Monday':'월','Tuesday':'화','Wednesday':'수',
               'Thursday':'목','Friday':'금','Saturday':'토','Sunday':'일'}
    rent['요일명_한'] = rent['요일명'].map(dow_kor)
    rent['주말여부'] = rent['요일'].apply(lambda x: '주말' if x >= 5 else '평일')

    return rent, station, use_sample


def generate_sample_data():
    """실제 CSV 없을 때 시뮬레이션 데이터 생성"""
    np.random.seed(42)
    dates = pd.date_range("2025-12-01", "2025-12-31", freq="1min")
    n = min(50000, len(dates))
    idx = np.random.choice(len(dates), size=n, replace=False)
    sampled_dates = sorted(dates[idx].to_pydatetime())

    bike_types = np.random.choice(['일반자전거', '새싹자전거'], n, p=[0.99, 0.01])
    genders = np.random.choice(['M', 'F', '알수없음'], n, p=[0.56, 0.27, 0.17])
    user_types = np.random.choice(['내국인', '비회원', '알수없음'], n, p=[0.83, 0.11, 0.06])
    usage_time = np.random.exponential(10, n).clip(1, 120).astype(int)
    usage_dist = (usage_time * np.random.uniform(80, 200, n)).astype(int)

    station_names = [f"따릉이대여소{i:04d}" for i in range(1, 301)]
    rent_stations = np.random.choice(station_names, n)
    rent_station_nos = [f"ST{i:04d}" for i in range(1, 301)]
    station_map = dict(zip(station_names, rent_station_nos))

    rent = pd.DataFrame({
        '자전거번호': [f'B{i:05d}' for i in np.random.randint(1,10000,n)],
        '대여일시': sampled_dates,
        '대여소번호': [station_map[s] for s in rent_stations],
        '대여소명': rent_stations,
        '대여거치대': np.random.randint(1, 20, n),
        '반납일시': [pd.Timestamp(d) + pd.Timedelta(minutes=int(t))
                    for d, t in zip(sampled_dates, usage_time)],
        '반납소번호': np.random.choice(rent_station_nos, n),
        '반납소명': np.random.choice(station_names, n),
        '반납거치대': np.random.randint(1, 20, n),
        '이용시간': usage_time,
        '이용거리': usage_dist,
        '생년': np.random.randint(1960, 2005, n),
        '성별': genders,
        '이용자종류': user_types,
        '대여소ID': [station_map[s] for s in rent_stations],
        '반납소ID': np.random.choice(rent_station_nos, n),
        '자전거구분': bike_types,
    })

    gus = ['강남구','강동구','강북구','강서구','관악구','광진구','구로구',
           '금천구','노원구','도봉구','동대문구','동작구','마포구','서대문구',
           '서초구','성동구','성북구','송파구','양천구','영등포구','용산구',
           '은평구','종로구','중구','중랑구']
    s_n = 300
    station = pd.DataFrame({
        '대여소번호': rent_station_nos,
        '대여소명': station_names,
        '자치구': np.random.choice(gus, s_n),
        '상세주소': [f"서울시 {np.random.choice(gus)} 어딘가 {i}" for i in range(s_n)],
        '위도': np.random.uniform(37.46, 37.69, s_n),
        '경도': np.random.uniform(126.82, 127.18, s_n),
        '설치시기': np.random.choice(['2015','2016','2017','2018','2019','2020','2021','2022','2023'], s_n),
        '거치대수': np.random.randint(5, 30, s_n),
        '기타': [''] * s_n,
    })
    return rent, station


# ── 사이드바 ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-size: 2.5rem;">🚲</div>
        <div style="font-family:'Space Mono',monospace; font-size:1rem; color:#38bdf8; font-weight:700;">
            따릉이 시각화
        </div>
        <div style="font-size:0.75rem; color:#475569; margin-top:0.3rem;">
            Data Visualization Guide
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    page = st.selectbox(
        "📌 단원 선택",
        ["🏠 개요 & 데이터", "📊 1. Matplotlib", "🎨 2. Seaborn", "⚡ 3. Plotly", "🗺️ 지도 시각화", "🏆 종합 대시보드"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem; color:#475569;">💡 실제 데이터가 없으면<br>시뮬레이션 데이터로 실행됩니다.</div>',
                unsafe_allow_html=True)

# ── 데이터 로드 ──────────────────────────────────────────
with st.spinner("데이터 로딩 중..."):
    rent, station, use_sample = load_data()

if use_sample:
    st.warning("⚠️ `data/` 폴더에 원본 CSV가 없어 **시뮬레이션 데이터**로 실행 중입니다. 원본 데이터를 넣으면 실제 분석이 가능합니다.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 1 : 개요 & 데이터
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if page == "🏠 개요 & 데이터":
    st.markdown("""
    <div class="main-header">
        <h1>🚲 서울 따릉이로 배우는 데이터 시각화</h1>
        <p>Matplotlib · Seaborn · Plotly 를 활용한 완전 정복 가이드 — 2025년 12월 데이터 기반</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 이용건수", f"{len(rent):,}건")
    with col2:
        st.metric("평균 이용시간", f"{rent['이용시간'].mean():.1f}분")
    with col3:
        st.metric("평균 이용거리", f"{rent['이용거리'].mean()/1000:.2f}km")
    with col4:
        st.metric("대여소 수", f"{len(station):,}개소")

    st.markdown("---")

    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown("### 📚 학습 구성")
        st.markdown("""
        <div class="section-card">
        <b style="color:#38bdf8">1. Matplotlib</b><br>
        <span style="color:#94a3b8; font-size:0.88rem">Figure/Axes 구조 · 선/막대/히스토그램/파이 차트</span>
        <br><br>
        <b style="color:#34d399">2. Seaborn</b><br>
        <span style="color:#94a3b8; font-size:0.88rem">스타일 설정 · hue/col/row · Boxplot · Heatmap · Pairplot</span>
        <br><br>
        <b style="color:#f59e0b">3. Plotly</b><br>
        <span style="color:#94a3b8; font-size:0.88rem">Express · Graph Objects · 인터랙티브 · 지도 · 대시보드</span>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("### 📂 사용 데이터")
        st.markdown("""
        <div class="section-card">
        <b style="color:#38bdf8">대여이력 데이터</b><br>
        <span style="color:#94a3b8; font-size:0.85rem">서울특별시_공공자전거_대여이력_정보_2512.csv<br>
        컬럼: 자전거번호, 대여일시, 대여소, 이용시간, 이용거리, 성별 등 17개</span>
        <br><br>
        <b style="color:#34d399">대여소 정보</b><br>
        <span style="color:#94a3b8; font-size:0.85rem">공공자전거_대여소_정보_25_12월_기준_.csv<br>
        컬럼: 대여소번호, 대여소명, 자치구, 위도, 경도, 거치대수 등 9개</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔍 데이터 미리보기")
    tab1, tab2 = st.tabs(["대여이력 (rent)", "대여소 정보 (station)"])
    with tab1:
        st.dataframe(rent.head(10), use_container_width=True, height=280)
    with tab2:
        st.dataframe(station.head(10), use_container_width=True, height=280)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 2 : Matplotlib
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "📊 1. Matplotlib":
    st.markdown("""
    <div class="main-header">
        <h1>📊 1. Matplotlib</h1>
        <p>정적 시각화의 기본 — Figure & Axes 구조부터 다양한 차트 유형까지</p>
    </div>
    """, unsafe_allow_html=True)

    sub = st.radio("섹션 선택", ["1-1. Figure & Axes", "1-2. 선 그래프", "1-3. 막대 그래프", "1-4. 히스토그램", "1-5. 파이 차트", "✏️ 연습문제"], horizontal=True)

    # 1-1
    if sub == "1-1. Figure & Axes":
        st.markdown("#### Figure & Axes 기본 구조")
        st.markdown("""
        <div class="info-box">
        <b>Figure</b>: 전체 캔버스 — <code>plt.figure()</code> 또는 <code>plt.subplots()</code>로 생성<br>
        <b>Axes</b>: 실제 그래프가 그려지는 영역, 하나의 Figure에 여러 개 배치 가능<br>
        <b>Axis</b>: x축·y축 (눈금, 범위 등) &nbsp;|&nbsp; <b>Artist</b>: 선, 점, 텍스트 등 모든 객체
        </div>
        """, unsafe_allow_html=True)

        fig, axes = plt.subplots(1, 3, figsize=(14, 4), facecolor='#1a1d2e')
        for ax in axes:
            ax.set_facecolor('#0f1117')
            for spine in ax.spines.values():
                spine.set_edgecolor('#2a2d3e')
            ax.tick_params(colors='#64748b')
            ax.xaxis.label.set_color('#94a3b8')
            ax.yaxis.label.set_color('#94a3b8')
            ax.title.set_color('#e2e8f0')

        axes[0].set_title('Axes[0] — 빈 그래프')
        axes[0].set_xlabel('x축'); axes[0].set_ylabel('y축')

        x = [0,1,2,3,4]; y = [0,1,4,9,16]
        axes[1].plot(x, y, color='#38bdf8', linewidth=2, marker='o')
        axes[1].set_title('Axes[1] — 선 그래프')
        axes[1].set_xlabel('x'); axes[1].set_ylabel('y = x²')

        axes[2].bar(['A','B','C'], [30,50,20],
                    color=['#f87171','#38bdf8','#34d399'])
        axes[2].set_title('Axes[2] — 막대 그래프')
        axes[2].set_xlabel('범주'); axes[2].set_ylabel('값')

        fig.suptitle('Figure 안에 3개의 Axes', fontsize=13, color='#e2e8f0', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class="code-block">fig, axes = plt.subplots(1, 3, figsize=(15, 4))  # 1행 3열 서브플롯 생성

axes[0].set_title('빈 그래프')
axes[1].plot(x, y, color='steelblue', linewidth=2, marker='o')
axes[2].bar(categories, values, color=['#e74c3c','#3498db','#2ecc71'])

fig.suptitle('Figure 안에 3개의 Axes', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()</div>
        """, unsafe_allow_html=True)

    # 1-2
    elif sub == "1-2. 선 그래프":
        st.markdown("#### 선 그래프 (Line Plot) — 시간에 따른 변화, 연속적 흐름")
        daily = rent.groupby('일자').size().reset_index(name='이용건수')

        fig, ax = plt.subplots(figsize=(13, 5), facecolor='#1a1d2e')
        ax.set_facecolor('#0f1117')
        for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
        ax.tick_params(colors='#64748b')

        ax.plot(daily['일자'], daily['이용건수'], color='#38bdf8', linewidth=2.5,
                marker='s', markersize=6, label='일별 이용건수')
        avg = daily['이용건수'].mean()
        ax.axhline(avg, color='#f87171', linestyle='--', linewidth=1.5,
                   label=f'평균 ({avg:,.0f}건)')

        max_day = daily.loc[daily['이용건수'].idxmax()]
        min_day = daily.loc[daily['이용건수'].idxmin()]
        ax.annotate(f"최대\n{max_day['이용건수']:,}건",
                    xy=(max_day['일자'], max_day['이용건수']),
                    xytext=(max_day['일자']+1, max_day['이용건수']+max(daily['이용건수'])*0.03),
                    arrowprops=dict(arrowstyle='->', color='#34d399'), color='#34d399', fontsize=9)
        ax.annotate(f"최소\n{min_day['이용건수']:,}건",
                    xy=(min_day['일자'], min_day['이용건수']),
                    xytext=(min_day['일자']+1, min_day['이용건수']-max(daily['이용건수'])*0.05),
                    arrowprops=dict(arrowstyle='->', color='#f87171'), color='#f87171', fontsize=9)

        ax.set_title('2025년 12월 일별 따릉이 이용건수', color='#e2e8f0', fontsize=13)
        ax.set_xlabel('날짜(일)', color='#94a3b8'); ax.set_ylabel('이용건수', color='#94a3b8')
        ax.set_xticks(daily['일자'])
        ax.grid(axis='y', alpha=0.2, color='#2a2d3e')
        ax.legend(facecolor='#1a1d2e', edgecolor='#2a2d3e', labelcolor='#94a3b8')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class="code-block">ax.plot(daily['일자'], daily['이용건수'],
        color='steelblue', linewidth=2.5, marker='s', markersize=6, label='일별 이용건수')

ax.axhline(avg, color='tomato', linestyle='--', linewidth=1.5)   # 평균선
ax.annotate('최대', xy=(...), xytext=(...), arrowprops=dict(arrowstyle='->'))
ax.grid(axis='y', alpha=0.4)
ax.legend()</div>
        """, unsafe_allow_html=True)

    # 1-3
    elif sub == "1-3. 막대 그래프":
        st.markdown("#### 막대 그래프 (Bar Chart) — 범주 간 크기 비교")
        dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        dow_kor   = ['월','화','수','목','금','토','일']
        dow_counts = (rent.groupby('요일명').size().reindex(dow_order, fill_value=0)
                      .reset_index(name='이용건수'))
        dow_counts['요일_한'] = dow_kor

        fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor='#1a1d2e')
        for ax in axes:
            ax.set_facecolor('#0f1117')
            for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
            ax.tick_params(colors='#64748b')

        bar_colors = ['#38bdf8']*5 + ['#f87171','#f87171']
        bars = axes[0].bar(dow_counts['요일_한'], dow_counts['이용건수'],
                           color=bar_colors, edgecolor='#1a1d2e', width=0.7)
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                axes[0].text(bar.get_x()+bar.get_width()/2, h+h*0.01,
                             f'{int(h):,}', ha='center', va='bottom', fontsize=8, color='#94a3b8')
        axes[0].set_title('요일별 이용건수', color='#e2e8f0', fontsize=12)
        axes[0].set_xlabel('요일', color='#94a3b8'); axes[0].set_ylabel('이용건수', color='#94a3b8')
        axes[0].grid(axis='y', alpha=0.2, color='#2a2d3e')

        # 자치구별 누적 막대
        gu_stats = (station.groupby('자치구')
                    .agg(대여소수=('대여소명','count'), 거치대수=('거치대수','sum'))
                    .sort_values('대여소수', ascending=False).head(8))
        x = np.arange(len(gu_stats)); w = 0.38
        axes[1].bar(x-w/2, gu_stats['대여소수'], w, label='대여소 수', color='#38bdf8', alpha=0.85)
        axes[1].bar(x+w/2, gu_stats['거치대수'], w, label='거치대 수', color='#f59e0b', alpha=0.85)
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(gu_stats.index, rotation=30, ha='right', color='#64748b')
        axes[1].set_title('자치구별 대여소·거치대 수 TOP8', color='#e2e8f0', fontsize=12)
        axes[1].set_ylabel('수량', color='#94a3b8')
        axes[1].legend(facecolor='#1a1d2e', edgecolor='#2a2d3e', labelcolor='#94a3b8')
        axes[1].grid(axis='y', alpha=0.2, color='#2a2d3e')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # 1-4
    elif sub == "1-4. 히스토그램":
        st.markdown("#### 히스토그램 (Histogram) — 수치형 변수의 분포 확인")
        fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='#1a1d2e')
        for ax in axes:
            ax.set_facecolor('#0f1117')
            for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
            ax.tick_params(colors='#64748b')

        axes[0].hist(rent['이용시간'], bins=40, color='#38bdf8', edgecolor='#1a1d2e', alpha=0.85)
        axes[0].axvline(rent['이용시간'].mean(), color='#f87171', ls='--', lw=1.5,
                        label=f"평균 {rent['이용시간'].mean():.1f}분")
        axes[0].axvline(rent['이용시간'].median(), color='#f59e0b', ls='--', lw=1.5,
                        label=f"중앙값 {rent['이용시간'].median():.1f}분")
        axes[0].set_title('이용시간 분포', color='#e2e8f0')
        axes[0].set_xlabel('이용시간(분)', color='#94a3b8'); axes[0].set_ylabel('빈도', color='#94a3b8')
        axes[0].legend(facecolor='#1a1d2e', edgecolor='#2a2d3e', labelcolor='#94a3b8')
        axes[0].grid(alpha=0.15, color='#2a2d3e')

        dist_km = rent['이용거리']/1000
        axes[1].hist(dist_km, bins=40, color='#34d399', edgecolor='#1a1d2e', alpha=0.85)
        axes[1].axvline(dist_km.mean(), color='#f87171', ls='--', lw=1.5,
                        label=f"평균 {dist_km.mean():.2f}km")
        axes[1].axvline(dist_km.median(), color='#f59e0b', ls='--', lw=1.5,
                        label=f"중앙값 {dist_km.median():.2f}km")
        axes[1].set_title('이용거리 분포', color='#e2e8f0')
        axes[1].set_xlabel('이용거리(km)', color='#94a3b8'); axes[1].set_ylabel('빈도', color='#94a3b8')
        axes[1].legend(facecolor='#1a1d2e', edgecolor='#2a2d3e', labelcolor='#94a3b8')
        axes[1].grid(alpha=0.15, color='#2a2d3e')

        fig.suptitle('따릉이 이용 패턴 분포', fontsize=13, color='#e2e8f0', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class="code-block">axes[0].hist(rent['이용시간'], bins=40, color='steelblue', edgecolor='white', alpha=0.85)
axes[0].axvline(rent['이용시간'].mean(),   color='red',    ls='--', lw=1.5, label=f'평균')
axes[0].axvline(rent['이용시간'].median(), color='orange', ls='--', lw=1.5, label=f'중앙값')

# bins: 구간 수 (많을수록 세밀)
# density=True: y축을 빈도 대신 확률 밀도로 표현</div>
        """, unsafe_allow_html=True)

    # 1-5
    elif sub == "1-5. 파이 차트":
        st.markdown("#### 파이 차트 / 도넛 차트 — 비율 표현")
        bike_counts = rent['자전거구분'].value_counts()
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor='#1a1d2e')
        for ax in axes: ax.set_facecolor('#1a1d2e')

        axes[0].pie(bike_counts, labels=bike_counts.index, autopct='%1.1f%%',
                    colors=['#38bdf8','#34d399'], startangle=90,
                    wedgeprops={'edgecolor':'#1a1d2e','linewidth':2},
                    textprops={'color':'#94a3b8'})
        axes[0].set_title('자전거 구분 비율', color='#e2e8f0')

        axes[1].pie(bike_counts, labels=bike_counts.index, autopct='%1.1f%%',
                    colors=['#38bdf8','#34d399'], startangle=90,
                    wedgeprops={'edgecolor':'#1a1d2e','linewidth':2,'width':0.6},
                    textprops={'color':'#94a3b8'})
        axes[1].text(0, 0, f'총\n{bike_counts.sum():,}건', ha='center', va='center',
                     fontsize=11, color='#e2e8f0', fontweight='bold')
        axes[1].set_title('자전거 구분 비율 (도넛)', color='#e2e8f0')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class="code-block"># 도넛 차트 — width 파라미터로 구멍 크기 조절
axes[1].pie(bike_counts,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.6})
axes[1].text(0, 0, f'총\n{total:,}건', ha='center', va='center', fontsize=12)</div>
        """, unsafe_allow_html=True)

    # 연습문제
    elif sub == "✏️ 연습문제":
        st.markdown("#### ✏️ Part 1 연습문제 — 정답 코드 & 시각화")
        q = st.selectbox("문제 선택", ["문제 1: 시간대별 평균 이용거리", "문제 2: 이용자종류별 수평 막대", "문제 3: 이용거리 구간별 히스토그램"])

        if "문제 1" in q:
            hourly_dist = rent.groupby('시간대')['이용거리'].mean() / 1000
            fig, ax = plt.subplots(figsize=(12,5), facecolor='#1a1d2e')
            ax.set_facecolor('#0f1117')
            for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
            ax.plot(hourly_dist.index, hourly_dist.values, color='#38bdf8',
                    lw=2, marker='o', ms=5, label='평균 이용거리')
            ax.axhline(hourly_dist.mean(), color='#f87171', ls='--', lw=1.5,
                       label=f'전체 평균 {hourly_dist.mean():.2f}km')
            ax.set_title('시간대별 평균 이용거리(km)', color='#e2e8f0', fontsize=13)
            ax.set_xlabel('시간대', color='#94a3b8'); ax.set_ylabel('평균 이용거리(km)', color='#94a3b8')
            ax.tick_params(colors='#64748b')
            ax.set_xticks(range(24)); ax.grid(alpha=0.15, color='#2a2d3e')
            ax.legend(facecolor='#1a1d2e', edgecolor='#2a2d3e', labelcolor='#94a3b8')
            plt.tight_layout(); st.pyplot(fig); plt.close()

        elif "문제 2" in q:
            user_counts = (rent[rent['이용자종류'] != '알수없음']['이용자종류']
                           .value_counts().sort_values())
            fig, ax = plt.subplots(figsize=(9,4), facecolor='#1a1d2e')
            ax.set_facecolor('#0f1117')
            for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
            bars = ax.barh(user_counts.index, user_counts.values,
                           color='#818cf8', edgecolor='#1a1d2e')
            for bar in bars:
                w = bar.get_width()
                ax.text(w+w*0.01, bar.get_y()+bar.get_height()/2,
                        f'{int(w):,}', va='center', fontsize=10, color='#94a3b8')
            ax.set_title('이용자종류별 이용건수', color='#e2e8f0', fontsize=13)
            ax.set_xlabel('이용건수', color='#94a3b8')
            ax.tick_params(colors='#64748b'); ax.grid(axis='x', alpha=0.15, color='#2a2d3e')
            plt.tight_layout(); st.pyplot(fig); plt.close()

        else:
            dist_km = rent['이용거리']/1000
            bins = np.arange(0, dist_km.max()+0.5, 0.5)
            fig, ax = plt.subplots(figsize=(11,5), facecolor='#1a1d2e')
            ax.set_facecolor('#0f1117')
            for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
            ax.hist(dist_km[dist_km<=3], bins=bins, color='#38bdf8', alpha=0.8,
                    edgecolor='#1a1d2e', label='0~3km (단거리)')
            ax.hist(dist_km[(dist_km>3)&(dist_km<=6)], bins=bins, color='#f59e0b', alpha=0.8,
                    edgecolor='#1a1d2e', label='3~6km (중거리)')
            ax.hist(dist_km[dist_km>6], bins=bins, color='#f87171', alpha=0.8,
                    edgecolor='#1a1d2e', label='6km+ (장거리)')
            ax.set_title('이용거리 구간별 분포', color='#e2e8f0', fontsize=13)
            ax.set_xlabel('이용거리(km)', color='#94a3b8'); ax.set_ylabel('빈도', color='#94a3b8')
            ax.tick_params(colors='#64748b')
            ax.legend(facecolor='#1a1d2e', edgecolor='#2a2d3e', labelcolor='#94a3b8')
            ax.grid(alpha=0.15, color='#2a2d3e')
            plt.tight_layout(); st.pyplot(fig); plt.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 3 : Seaborn
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "🎨 2. Seaborn":
    st.markdown("""
    <div class="main-header">
        <h1>🎨 2. Seaborn</h1>
        <p>통계 기반 시각화 — hue · Boxplot · Violin · Heatmap · Pairplot</p>
    </div>
    """, unsafe_allow_html=True)

    sub = st.radio("섹션 선택", ["2-1. 스타일 & KDE", "2-2. Boxplot & Violin", "2-3. Heatmap", "2-4. Pairplot", "✏️ 연습문제"], horizontal=True)

    if sub == "2-1. 스타일 & KDE":
        st.markdown("#### 성별별 이용시간 분포 — KDE & Histogram")
        fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='#1a1d2e')
        sns.set_theme(style='darkgrid', font=chosen_font)
        data_mf = rent[rent['성별'].isin(['M','F'])]

        for ax in axes:
            ax.set_facecolor('#0f1117')
            for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
            ax.tick_params(colors='#64748b')

        sns.kdeplot(data=data_mf, x='이용시간', hue='성별', fill=True, alpha=0.4,
                    palette={'M':'#38bdf8','F':'#f472b6'}, ax=axes[0])
        axes[0].set_title('성별별 이용시간 분포 (KDE)', color='#e2e8f0')
        axes[0].set_xlabel('이용시간(분)', color='#94a3b8')

        sns.histplot(data=data_mf, x='이용시간', hue='성별', bins=30, alpha=0.6,
                     palette={'M':'#38bdf8','F':'#f472b6'}, ax=axes[1])
        axes[1].set_title('성별별 이용시간 분포 (Histogram)', color='#e2e8f0')
        axes[1].set_xlabel('이용시간(분)', color='#94a3b8')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        sns.set_theme(style='whitegrid', font=chosen_font)

        st.markdown("""
        <div class="info-box">
        <b>hue</b>: 색상으로 그룹 구분 (같은 Axes 안에서)<br>
        <b>col</b>: 열 방향으로 Axes를 분리 (FacetGrid)<br>
        <b>row</b>: 행 방향으로 Axes를 분리 (FacetGrid)
        </div>
        """, unsafe_allow_html=True)

    elif sub == "2-2. Boxplot & Violin":
        st.markdown("#### Boxplot & Violinplot — 이용자 유형별 이용시간")
        target_types = ['내국인','비회원','알수없음']
        filtered = rent[rent['이용자종류'].isin(target_types)]

        fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#1a1d2e')
        sns.set_theme(style='whitegrid', font=chosen_font)
        for ax in axes:
            ax.set_facecolor('#0f1117')
            ax.grid(color='#2a2d3e', alpha=0.5)
            for spine in ax.spines.values(): spine.set_edgecolor('#2a2d3e')
            ax.tick_params(colors='#64748b')

        sns.boxplot(data=filtered, x='이용자종류', y='이용시간',
                    palette='Set2', ax=axes[0])
        axes[0].set_title('이용자종류별 이용시간 (Boxplot)', color='#e2e8f0')
        axes[0].set_xlabel('이용자종류', color='#94a3b8')
        axes[0].set_ylabel('이용시간(분)', color='#94a3b8')

        sns.violinplot(data=filtered, x='이용자종류', y='이용시간',
                       palette='Set2', inner='quartile', ax=axes[1])
        axes[1].set_title('이용자종류별 이용시간 (Violinplot)', color='#e2e8f0')
        axes[1].set_xlabel('이용자종류', color='#94a3b8')
        axes[1].set_ylabel('이용시간(분)', color='#94a3b8')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    elif sub == "2-3. Heatmap":
        st.markdown("#### 상관계수 Heatmap")
        num_cols = ['이용시간','이용거리','시간대','요일']
        corr = rent[num_cols].corr()

        fig, ax = plt.subplots(figsize=(7, 6), facecolor='#1a1d2e')
        ax.set_facecolor('#0f1117')
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                    vmin=-1, vmax=1, square=True, linewidths=0.5, ax=ax,
                    annot_kws={'color':'#e2e8f0'})
        ax.set_title('수치형 변수 상관계수 히트맵', color='#e2e8f0', fontsize=13)
        ax.tick_params(colors='#94a3b8')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class="info-box">
        Pairplot 읽는 법: <b>대각선</b> = 각 변수의 KDE 분포 &nbsp;|&nbsp;
        <b>비대각선</b> = 변수 간 산점도 (↗ 양의 상관, ↘ 음의 상관)
        </div>
        """, unsafe_allow_html=True)

    elif sub == "2-4. Pairplot":
        st.markdown("#### Pairplot — 변수 간 모든 조합 산점도")
        sample_pair = rent[['이용시간','이용거리','시간대','자전거구분']].sample(1500, random_state=42)
        with st.spinner("Pairplot 생성 중... (잠시 기다려주세요)"):
            g = sns.pairplot(sample_pair, hue='자전거구분',
                             palette=['#38bdf8','#34d399'],
                             diag_kind='kde',
                             plot_kws={'alpha':0.4,'s':15})
            g.figure.suptitle('수치형 변수 Pairplot (자전거구분별)', fontsize=12, y=1.02,
                               color='#e2e8f0')
            st.pyplot(g.figure)
            plt.close()

    elif sub == "✏️ 연습문제":
        st.markdown("#### ✏️ Part 2 연습문제")
        q = st.selectbox("문제 선택", ["문제 4: 시간대별×요일별 이용건수 히트맵"])

        if "문제 4" in q:
            dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            dow_kor = ['월','화','수','목','금','토','일']
            pivot = (rent.groupby(['시간대','요일명']).size().unstack()
                     .reindex(columns=dow_order))
            pivot.columns = dow_kor

            fig, ax = plt.subplots(figsize=(11, 9), facecolor='#1a1d2e')
            ax.set_facecolor('#0f1117')
            sns.heatmap(pivot, cmap='YlOrRd', annot=False, linewidths=0.3,
                        linecolor='#1a1d2e', ax=ax, cbar_kws={'label':'이용건수'})
            ax.set_title('시간대 × 요일별 이용건수 히트맵', color='#e2e8f0', fontsize=13)
            ax.set_xlabel('요일', color='#94a3b8'); ax.set_ylabel('시간대', color='#94a3b8')
            ax.tick_params(colors='#94a3b8')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 4 : Plotly
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "⚡ 3. Plotly":
    st.markdown("""
    <div class="main-header">
        <h1>⚡ 3. Plotly</h1>
        <p>인터랙티브 시각화 — hover · zoom · pan · filtering 완전 정복</p>
    </div>
    """, unsafe_allow_html=True)

    sub = st.radio("섹션 선택", ["3-1. Express 기본", "3-2. 히스토그램 & 박스", "3-3. Graph Objects", "✏️ 연습문제"], horizontal=True)

    PLOTLY_THEME = dict(
        template='plotly_dark',
        paper_bgcolor='#1a1d2e',
        plot_bgcolor='#0f1117',
        font=dict(color='#94a3b8')
    )

    if sub == "3-1. Express 기본":
        st.markdown("#### 일별 이용건수 — 선 그래프 (인터랙티브)")
        daily = rent.groupby('일자').size().reset_index(name='이용건수')
        fig = px.line(daily, x='일자', y='이용건수',
                      title='2025년 12월 일별 따릉이 이용건수',
                      markers=True, labels={'일자':'날짜(일)','이용건수':'이용건수(건)'},
                      template='plotly_dark')
        fig.update_traces(line_color='#38bdf8', line_width=2.5)
        fig.update_layout(hovermode='x unified', **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 시간대별 이용건수 — 막대 그래프")
        hourly = rent.groupby('시간대').size().reset_index(name='이용건수')
        hourly['비율'] = (hourly['이용건수']/hourly['이용건수'].sum()*100).round(1)
        fig2 = px.bar(hourly, x='시간대', y='이용건수',
                      title='시간대별 따릉이 이용건수',
                      color='이용건수', color_continuous_scale='Blues',
                      hover_data=['비율'], template='plotly_dark')
        fig2.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1),
                           coloraxis_showscale=False, **PLOTLY_THEME)
        st.plotly_chart(fig2, use_container_width=True)

    elif sub == "3-2. 히스토그램 & 박스":
        st.markdown("#### 자전거구분별 이용시간 분포")
        fig = px.histogram(rent, x='이용시간', color='자전거구분',
                           barmode='overlay', opacity=0.7, nbins=40,
                           title='자전거구분별 이용시간 분포',
                           labels={'이용시간':'이용시간(분)'},
                           color_discrete_map={'일반자전거':'#38bdf8','새싹자전거':'#34d399'},
                           template='plotly_dark')
        fig.update_layout(bargap=0.05, **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 이용자종류 × 자전거구분별 이용시간 — Boxplot")
        target_types = ['내국인','비회원','알수없음']
        filtered = rent[rent['이용자종류'].isin(target_types)]
        fig2 = px.box(filtered, x='이용자종류', y='이용시간', color='자전거구분',
                      points='outliers', title='이용자종류 × 자전거구분별 이용시간 분포',
                      labels={'이용시간':'이용시간(분)','이용자종류':'이용자 종류'},
                      color_discrete_map={'일반자전거':'#38bdf8','새싹자전거':'#34d399'},
                      template='plotly_dark')
        fig2.update_layout(boxmode='group', legend_title='자전거 구분', **PLOTLY_THEME)
        st.plotly_chart(fig2, use_container_width=True)

    elif sub == "3-3. Graph Objects":
        st.markdown("#### go를 사용한 다중 선 그래프")
        daily_bike = (rent.groupby(['일자','자전거구분']).size()
                      .reset_index(name='이용건수'))
        fig = go.Figure()
        color_map = {'일반자전거':'#38bdf8','새싹자전거':'#34d399'}
        for btype in daily_bike['자전거구분'].unique():
            sub_df = daily_bike[daily_bike['자전거구분']==btype]
            fig.add_trace(go.Scatter(
                x=sub_df['일자'], y=sub_df['이용건수'],
                mode='lines+markers', name=btype,
                line=dict(color=color_map.get(btype,'gray'), width=2.5),
                marker=dict(size=6),
                hovertemplate=f'<b>{btype}</b><br>%{{x}}일<br>이용건수: %{{y:,}}건<extra></extra>'
            ))
        fig.update_layout(title='자전거구분별 일별 이용건수',
                          xaxis_title='날짜(일)', yaxis_title='이용건수',
                          hovermode='x unified', legend_title='자전거 구분', **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="info-box">
        <b>hover 팁</b>: <code>hovertemplate</code>에서 <code>%{{x}}</code>, <code>%{{y:,}}</code>로 값 포맷 지정<br>
        <b>zoom</b>: 마우스 드래그 → 더블 클릭으로 원래 범위 복귀<br>
        <b>filtering</b>: 범례 클릭 → 특정 그룹 숨기기 / 더블 클릭 → 해당 그룹만 표시
        </div>
        """, unsafe_allow_html=True)

    elif sub == "✏️ 연습문제":
        st.markdown("#### ✏️ Part 3 연습문제 — 시간대별 평균 이용거리")
        hourly_agg = rent.groupby('시간대').agg(
            평균이용거리=('이용거리', lambda x: (x/1000).mean()),
            이용건수=('이용거리','count')
        ).reset_index()
        fig = px.line(hourly_agg, x='시간대', y='평균이용거리', markers=True,
                      hover_data={'이용건수':True,'시간대':False},
                      title='시간대별 평균 이용거리(km)',
                      labels={'시간대':'시간대','평균이용거리':'평균 이용거리(km)'},
                      template='plotly_dark')
        fig.update_traces(line_color='#00d4ff', line_width=2.5)
        fig.update_layout(xaxis=dict(tickmode='linear', dtick=1), **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 5 : 지도 시각화
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "🗺️ 지도 시각화":
    st.markdown("""
    <div class="main-header">
        <h1>🗺️ 지도 시각화</h1>
        <p>Plotly Mapbox — 대여소 위치 + 이용건수 버블맵</p>
    </div>
    """, unsafe_allow_html=True)

    station_clean = station[['대여소번호','대여소명','자치구','위도','경도','거치대수']].copy()
    station_clean['대여소번호'] = station_clean['대여소번호'].astype(str).str.strip()
    rent_cp = rent.copy()
    rent_cp['대여소번호'] = rent_cp['대여소번호'].astype(str).str.strip()
    rent_cnt = rent_cp.groupby('대여소번호').size().reset_index(name='이용건수')
    merged = station_clean.merge(rent_cnt, on='대여소번호', how='left')
    merged['이용건수'] = merged['이용건수'].fillna(0).astype(int)
    merged = merged.dropna(subset=['위도','경도'])
    merged = merged[(merged['위도']>37.4)&(merged['위도']<37.8)&
                    (merged['경도']>126.7)&(merged['경도']<127.3)]

    fig = px.scatter_mapbox(
        merged, lat='위도', lon='경도',
        size='이용건수', color='이용건수',
        hover_name='대여소명',
        hover_data={'자치구':True,'거치대수':True,'이용건수':True,'위도':False,'경도':False},
        color_continuous_scale='Reds', size_max=25,
        zoom=10, center=dict(lat=37.56, lon=126.99),
        mapbox_style='carto-positron',
        title='서울시 따릉이 대여소 이용건수 지도 (2025년 12월)', height=580
    )
    fig.update_layout(coloraxis_colorbar_title='이용건수',
                      paper_bgcolor='#1a1d2e', font=dict(color='#94a3b8'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 자치구별 총 이용건수")
    gu_cnt = (merged.groupby('자치구')['이용건수'].sum().reset_index()
              .sort_values('이용건수', ascending=False))
    fig2 = px.bar(gu_cnt, x='자치구', y='이용건수',
                  color='이용건수', color_continuous_scale='Reds',
                  title='자치구별 따릉이 이용건수', template='plotly_dark', height=400)
    fig2.update_layout(xaxis_tickangle=-30, coloraxis_showscale=False,
                       paper_bgcolor='#1a1d2e', plot_bgcolor='#0f1117',
                       font=dict(color='#94a3b8'))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="code-block">fig = px.scatter_mapbox(
    station_merged,
    lat='위도', lon='경도',
    size='이용건수',          # 원 크기 = 이용건수
    color='이용건수',         # 색상도 이용건수에 비례
    hover_name='대여소명',
    color_continuous_scale='Reds',
    size_max=25,
    zoom=10,
    center=dict(lat=37.56, lon=126.99),
    mapbox_style='carto-positron'
)</div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE 6 : 종합 대시보드
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "🏆 종합 대시보드":
    st.markdown("""
    <div class="main-header">
        <h1>🏆 종합 대시보드</h1>
        <p>KPI + 시계열 + 분포 + 지도 — 실무형 따릉이 분석 대시보드</p>
    </div>
    """, unsafe_allow_html=True)

    # 집계
    daily = rent.groupby('일자').size().reset_index(name='이용건수')
    hourly = rent.groupby('시간대').size().reset_index(name='이용건수')
    dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow_kor_map = {'Monday':'월','Tuesday':'화','Wednesday':'수',
                   'Thursday':'목','Friday':'금','Saturday':'토','Sunday':'일'}
    dow = (rent.groupby('요일명').size().reindex(dow_order).reset_index(name='이용건수'))
    dow['요일'] = dow['요일명'].map(dow_kor_map)
    bike_avg = rent.groupby('자전거구분')['이용시간'].mean().reset_index(name='평균이용시간')
    bike_cnt = rent.groupby('자전거구분').size().reset_index(name='이용건수')
    gender_cnt = rent[rent['성별'].isin(['M','F'])].groupby('성별').size().reset_index(name='이용건수')

    THEME = dict(template='plotly_dark', paper_bgcolor='#1a1d2e',
                 plot_bgcolor='#0f1117', font=dict(color='#94a3b8'))

    fig = make_subplots(
        rows=3, cols=3,
        specs=[
            [{'type':'indicator'},{'type':'indicator'},{'type':'indicator'}],
            [{'colspan':2},None,{'type':'xy'}],
            [{'type':'xy'},{'type':'xy'},{'type':'domain'}]
        ],
        subplot_titles=('','','',
                        '일별 이용건수 추이','시간대별 이용건수',
                        '요일별 이용건수','자전거구분별 평균이용시간','자전거구분 비율')
    )

    fig.add_trace(go.Indicator(
        mode='number', value=len(rent),
        title={'text':'총 이용건수','font':{'size':15}},
        number={'suffix':'건','font':{'size':32},'valueformat':','}
    ), row=1, col=1)
    fig.add_trace(go.Indicator(
        mode='number+delta', value=rent['이용시간'].mean(),
        delta={'reference':20,'relative':False,'suffix':'분'},
        title={'text':'평균 이용시간(분)','font':{'size':15}},
        number={'suffix':'분','font':{'size':32},'valueformat':'.1f'}
    ), row=1, col=2)
    fig.add_trace(go.Indicator(
        mode='number', value=rent['이용거리'].mean()/1000,
        title={'text':'평균 이용거리(km)','font':{'size':15}},
        number={'suffix':'km','font':{'size':32},'valueformat':'.2f'}
    ), row=1, col=3)

    fig.add_trace(go.Scatter(
        x=daily['일자'], y=daily['이용건수'],
        mode='lines+markers', line=dict(color='#38bdf8', width=2.5),
        marker=dict(size=6), name='일별 이용건수',
        hovertemplate='%{x}일: %{y:,}건<extra></extra>'
    ), row=2, col=1)
    fig.add_trace(go.Bar(
        x=hourly['시간대'], y=hourly['이용건수'],
        marker_color='#38bdf8', showlegend=False, name='시간대별',
        hovertemplate='%{x}시: %{y:,}건<extra></extra>'
    ), row=2, col=3)

    bar_colors = ['#38bdf8']*5 + ['#f87171','#f87171']
    fig.add_trace(go.Bar(
        x=dow['요일'], y=dow['이용건수'],
        marker_color=bar_colors, showlegend=False, name='요일별',
        hovertemplate='%{x}: %{y:,}건<extra></extra>'
    ), row=3, col=1)
    fig.add_trace(go.Bar(
        x=bike_avg['자전거구분'], y=bike_avg['평균이용시간'],
        marker_color=['#38bdf8','#34d399'], showlegend=False, name='평균이용시간',
        hovertemplate='%{x}: %{y:.1f}분<extra></extra>'
    ), row=3, col=2)
    fig.add_trace(go.Pie(
        labels=bike_cnt['자전거구분'], values=bike_cnt['이용건수'],
        marker_colors=['#38bdf8','#34d399'], hole=0.4, showlegend=False,
        hovertemplate='%{label}: %{value:,}건 (%{percent})<extra></extra>'
    ), row=3, col=3)

    fig.update_layout(
        title_text='🚲 서울 따릉이 종합 대시보드 — 2025년 12월',
        title_font_size=17, height=900,
        showlegend=False, **THEME
    )
    st.plotly_chart(fig, use_container_width=True)
