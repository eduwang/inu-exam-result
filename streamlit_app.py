import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="문항별 점수 분석", layout="wide")

st.title("문항별 점수 분석 대시보드")
st.caption("총 28명의 학생, 1번~5번 문항 점수 및 종합 점수 분석")


@st.cache_data
def load_data() -> pd.DataFrame:
    rows = [
        [4, 6, 2, 3, 3],
        [5, 1, 3, 3, 1],
        [2, 5, 0, 2, 1],
        [6, 8, 3, 4, 1],
        [4, 3, 3, 4, 2],
        [5, 8, 3, 3, 2],
        [9, 8, 3, 4, 3.5],
        [5, 4, 4, 3, 2],
        [1, 7, 2, 1, 2],
        [6, 5, 4, 3, 1],
        [2, 6, 0, 2, 1],
        [4, 6, 2, 3, 2],
        [4, 7, 1, 3, 1],
        [3, 6, 1, 1, 2],
        [7, 8, 4, 3, 2],
        [6, 5, 1, 3, 2],
        [6, 5, 1, 3, 1],
        [5, 3, 3, 2, 2],
        [2, 3, 2, 2, 0],
        [6, 6, 3, 2, 3],
        [6, 7, 2, 0, 0],
        [7, 1, 4, 2, 4],
        [7, 8, 3, 3, 2],
        [6, 8, 2, 3, 2],
        [8, 5, 1, 4, 2],
        [8, 3, 3, 4, 4],
        [3, 6, 3, 3, 1],
        [5, 5, 2, 3, 3],
    ]
    df = pd.DataFrame(rows, columns=["1번", "2번", "3번", "4번", "5번"])
    df["종합"] = df.sum(axis=1)
    return df


def summary_stats(series: pd.Series) -> pd.DataFrame:
    stats = {
        "표본 수": int(series.count()),
        "평균": series.mean(),
        "중앙값": series.median(),
        "표준편차": series.std(),
        "최솟값": series.min(),
        "1사분위수(Q1)": series.quantile(0.25),
        "3사분위수(Q3)": series.quantile(0.75),
        "최댓값": series.max(),
    }
    stats_df = pd.DataFrame([stats]).T.reset_index()
    stats_df.columns = ["지표", "값"]
    return stats_df


def render_tab(df: pd.DataFrame, col_name: str) -> None:
    series = df[col_name]

    m1, m2, m3 = st.columns(3)
    m1.metric("평균", f"{series.mean():.2f}")
    m2.metric("중앙값", f"{series.median():.2f}")
    m3.metric("표준편차", f"{series.std():.2f}")

    st.subheader("요약 통계")
    st.dataframe(summary_stats(series), use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("점수 분포")
        hist = px.histogram(
            df,
            x=col_name,
            nbins=12,
            title=f"{col_name} 점수 히스토그램",
            labels={col_name: "점수"},
        )
        hist.update_layout(bargap=0.08)
        st.plotly_chart(hist, use_container_width=True)

    with c2:
        st.subheader("상자 그림")
        box = px.box(
            df,
            y=col_name,
            points="all",
            title=f"{col_name} 상자 그림",
            labels={col_name: "점수"},
        )
        st.plotly_chart(box, use_container_width=True)


scores = load_data()

tabs = st.tabs(["1번 문항", "2번 문항", "3번 문항", "4번 문항", "5번 문항", "최종 종합"])

with tabs[0]:
    render_tab(scores, "1번")
with tabs[1]:
    render_tab(scores, "2번")
with tabs[2]:
    render_tab(scores, "3번")
with tabs[3]:
    render_tab(scores, "4번")
with tabs[4]:
    render_tab(scores, "5번")
with tabs[5]:
    render_tab(scores, "종합")
