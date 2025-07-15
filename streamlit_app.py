import streamlit as st

st.title("집단면역 계산기")

R0 = st.slider("기초감염재생산수 R₀", min_value=1.0, max_value=10.0, value=2.5, step=0.1)
p_c = 1 - (1 / R0)

st.markdown(f"**이론적 집단면역 달성 최소 면역자 비율:** {p_c:.1%}")
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 이미지 출력
image = Image.open("capybara.png")
st.image(image, caption="Capybara & Herd Immunity Simulation", use_column_width=True)

st.title("💉 집단면역 시뮬레이션")

st.markdown("""
이 앱은 **기초감염재생산수(R₀)** 에 따라 **최소 면역자 비율**을 계산하고,  
현재 대한민국의 인구 구조를 바탕으로 **세대별 인구 변화**와 함께  
**집단 면역 달성 조건**을 시각적으로 보여주는 앱입니다.
""")

# 사용자 입력: R0
R0 = st.slider("기초감염재생산수 (R₀)", min_value=1.0, max_value=10.0, step=0.1, value=3.0)
p_immune = 1 - 1 / R0
st.metric("필요한 최소 면역자 비율", f"{p_immune*100:.1f}%")

st.divider()

# ✅ 레슬리 행렬 구성
fertility_rate = 0.75
survival_rates = [0.89, 0.87, 0.85, 0.83, 0.80, 0.77, 0.73, 0.68, 0.61, 0.50]
female_life_expectancy = [86.4, 76.7, 66.8, 57.0, 47.2, 37.6, 28.2, 19.0, 10.7, 5.0, 2.3]

leslie_matrix = n_
