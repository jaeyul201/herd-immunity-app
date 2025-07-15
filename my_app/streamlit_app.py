import streamlit as st

st.title("집단면역 계산기")

R0 = st.slider("기초감염재생산수 R₀", min_value=1.0, max_value=10.0, value=2.5, step=0.1)
p_c = 1 - (1 / R0)

st.markdown(f"**이론적 집단면역 달성 최소 면역자 비율:** {p_c:.1%}")
