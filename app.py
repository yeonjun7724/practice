import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="헬륨기밀검사 불량 EDA 대시보드",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# 샘플 데이터
# 보고서 내용을 바탕으로 만든 러프 데이터입니다.
# 실제 CSV/엑셀 연결 전 구조 확인용입니다.
# -------------------------------------------------
monthly_df = pd.DataFrame({
    "month": [
        "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03",
        "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10"
    ],
    "defect_count": [85, 92, 180, 230, 140, 120, 115, 165, 190, 135, 125, 118, 110]
})

product_df = pd.DataFrame({
    "product": ["P890", "Q890", "P880", "Q880", "기타"],
    "defect_count": [320, 280, 150, 120, 90]
})

pareto_df = pd.DataFrame({
    "defect_type": ["RH누설", "LF누설", "FLUX미도포", "핀드랍", "이물낙하", "기타"],
    "count": [240, 180, 110, 95, 70, 55]
})
pareto_df["ratio"] = pareto_df["count"] / pareto_df["count"].sum()
pareto_df["cum_ratio"] = pareto_df["ratio"].cumsum()

zone_temp_df = pd.DataFrame({
    "zone": ["Zone1", "Zone2", "Zone3", "Zone4", "Zone5", "Zone6"],
    "avg_temp": [610, 625, 638, 645, 710, 650],
    "note": ["정상", "정상", "정상", "정상", "이상치 의심", "정상"]
})

corr_df = pd.DataFrame({
    "variable": ["온도", "압력", "시간", "속도"],
    "corr_with_defect": [0.18, 0.22, 0.15, -0.28]
})

insight_data = [
    "브레이징 공정은 전체 기간 중 가장 큰 변동성을 보임",
    "2024-12 ~ 2025-01 구간에서 1차 불량 피크가 확인됨",
    "2025-05 ~ 2025-06 구간에서 2차 상승 패턴이 나타남",
    "P890, Q890 계열 제품군에서 불량 집중도가 높음",
    "핵심 불량은 RH누설, LF누설, FLUX미도포, 핀드랍으로 요약 가능",
    "Zone5 온도는 다른 구간 대비 이상치 가능성이 있어 센서 점검 필요",
    "속도 변수는 불량과 음의 상관을 보여 저속 조건 재점검이 필요함"
]

# -------------------------------------------------
# 함수
# -------------------------------------------------
def draw_bar_chart(df, x_col, y_col, title, rotate=False):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df[x_col], df[y_col])
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    if rotate:
        plt.xticks(rotation=45)
    st.pyplot(fig)


def draw_line_chart(df, x_col, y_col, title, rotate=False):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(df[x_col], df[y_col], marker="o")
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    if rotate:
        plt.xticks(rotation=45)
    st.pyplot(fig)


def draw_pareto_chart(df, category_col, value_col):
    fig, ax1 = plt.subplots(figsize=(10, 4))

    ax1.bar(df[category_col], df[value_col])
    ax1.set_xlabel(category_col)
    ax1.set_ylabel("불량 건수")
    ax1.set_title("불량유형 Pareto Chart")
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(df[category_col], df["cum_ratio"] * 100, marker="o")
    ax2.set_ylabel("누적 비율(%)")
    ax2.set_ylim(0, 110)

    st.pyplot(fig)


# -------------------------------------------------
# 사이드바
# -------------------------------------------------
st.sidebar.title("헬륨기밀검사 EDA")
page = st.sidebar.radio(
    "메뉴 선택",
    [
        "대시보드 개요",
        "월별 불량 추이",
        "제품별 불량",
        "불량유형 Pareto",
        "Zone 온도 점검",
        "공정변수 상관",
        "핵심 인사이트",
        "데이터 업로드"
    ]
)

# -------------------------------------------------
# 메인
# -------------------------------------------------
st.title("헬륨기밀검사 불량 EDA 대시보드")
st.caption("보고서 기반 러프 버전 | Streamlit Prototype")

if page == "대시보드 개요":
    st.subheader("개요")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 불량 건수", int(monthly_df["defect_count"].sum()))
    col2.metric("최대 월 불량", int(monthly_df["defect_count"].max()))
    col3.metric("주요 제품군", "P890 / Q890")
    col4.metric("점검 필요 Zone", "Zone5")

    st.markdown("---")
    st.subheader("월별 불량 추이 미리보기")
    draw_line_chart(monthly_df, "month", "defect_count", "월별 불량 추이", rotate=True)

    st.markdown("---")
    st.subheader("주요 요약")
    st.write("브레이징 공정 중심 불량 패턴을 빠르게 확인하기 위한 러프 대시보드입니다.")
    st.write("실제 운영 시에는 CSV/엑셀 업로드 후 컬럼 매핑 로직을 붙여 확장할 수 있습니다.")

elif page == "월별 불량 추이":
    st.subheader("월별 불량 추이")
    st.dataframe(monthly_df, use_container_width=True)
    draw_line_chart(monthly_df, "month", "defect_count", "월별 불량 추이", rotate=True)

    peak_month = monthly_df.loc[monthly_df["defect_count"].idxmax(), "month"]
    peak_value = monthly_df["defect_count"].max()
    st.info(f"최대 불량 시점은 {peak_month}, 불량 건수는 {peak_value}건입니다.")

elif page == "제품별 불량":
    st.subheader("제품별 불량 현황")
    st.dataframe(product_df, use_container_width=True)
    draw_bar_chart(product_df, "product", "defect_count", "제품별 불량 건수")

    top_product = product_df.loc[product_df["defect_count"].idxmax(), "product"]
    st.info(f"가장 불량이 많은 제품군은 {top_product}입니다.")

elif page == "불량유형 Pareto":
    st.subheader("불량유형 Pareto 분석")
    st.dataframe(pareto_df, use_container_width=True)
    draw_pareto_chart(pareto_df, "defect_type", "count")

    top_defect = pareto_df.iloc[0]["defect_type"]
    top_ratio = round(pareto_df.iloc[0]["ratio"] * 100, 1)
    st.info(f"최대 비중 불량은 {top_defect}이며 전체의 약 {top_ratio}% 수준입니다.")

elif page == "Zone 온도 점검":
    st.subheader("Zone별 평균 온도 점검")
    st.dataframe(zone_temp_df, use_container_width=True)
    draw_bar_chart(zone_temp_df, "zone", "avg_temp", "Zone별 평균 온도")

    abnormal = zone_temp_df[zone_temp_df["note"].str.contains("이상치", na=False)]
    if not abnormal.empty:
        st.warning("이상치 의심 Zone이 존재합니다. 센서 및 공정 조건 점검이 필요합니다.")
        st.dataframe(abnormal, use_container_width=True)

elif page == "공정변수 상관":
    st.subheader("공정변수와 불량 간 상관")
    st.dataframe(corr_df, use_container_width=True)
    draw_bar_chart(corr_df, "variable", "corr_with_defect", "공정변수별 불량 상관도")

    st.write("양수는 불량 증가 방향, 음수는 불량 감소 방향으로 해석할 수 있습니다.")
    st.write("현재 러프 버전에서는 단순 상관 참고용으로만 표시합니다.")

elif page == "핵심 인사이트":
    st.subheader("핵심 인사이트")
    for idx, item in enumerate(insight_data, start=1):
        st.write(f"{idx}. {item}")

    st.markdown("---")
    st.subheader("개선 방향")
    st.write("1. 누설 불량 원인 세분화 및 재현실험")
    st.write("2. FLUX 도포 프로세스 관리 강화")
    st.write("3. Zone5 센서 및 제어값 점검")
    st.write("4. 저속 계열 제품 조건 최적화")
    st.write("5. 향후 RandomForest, SPC, 이상탐지 분석으로 확장")

elif page == "데이터 업로드":
    st.subheader("실데이터 업로드")
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일 업로드", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("파일 업로드 완료")
            st.dataframe(df.head(), use_container_width=True)

            st.markdown("### 컬럼 목록")
            st.write(list(df.columns))

            st.markdown("### 다음 단계 제안")
            st.write("- 월 컬럼, 제품 컬럼, 불량유형 컬럼, 공정변수 컬럼을 매핑")
            st.write("- 현재 샘플 차트를 실제 데이터 기반 차트로 교체")
            st.write("- 필터(제품군, 기간, 불량유형) 추가")
            st.write("- 이상치 탐지 및 모델링 탭 확장")
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    else:
        st.info("현재는 보고서 기반 샘플 데이터가 표시되는 프로토타입입니다.")
