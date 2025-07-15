import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 이미지 출력
image = Image.open("capybara.png")
st.image(image, caption="Capybara & Herd Immunity Simulation", use_column_width=True)

# 제목
st.title("💉 집단면역 시뮬레이션")

st.markdown("""
이 앱은 **기초감염재생산수(R₀)** 에 따라 **최소 면역자 비율**을 계산하고,  
현재 대한민국의 인구 구조를 바탕으로 **세대별 인구 변화**와 함께  
**집단 면역 달성 조건**을 시각적으로 보여주는 앱입니다.
""")

# 사용자 입력: R0
R0 = st.slider("기초감염재생산수 R₀", min_value=1.0, max_value=10.0, step=0.1, value=3.0)
p_immune = 1 - 1 / R0
st.metric("이론적 집단면역 달성 최소 면역자 비율", f"{p_immune*100:.1f}%")

st.divider()

# 레슬리 행렬 구성
fertility_rate = 0.75  # 합계출산율
survival_rates = [0.89, 0.87, 0.85, 0.83, 0.80, 0.77, 0.73, 0.68, 0.61, 0.50]  # 연령별 생존율
female_life_expectancy = [86.4, 76.7, 66.8, 57.0, 47.2, 37.6, 28.2, 19.0, 10.7, 5.0, 2.3]

leslie_matrix = np.zeros((11, 11))
leslie_matrix[0, 1:5] = fertility_rate / 4  # 출산 가능 연령: 10~40대
for i in range(10):
    leslie_matrix[i + 1, i] = survival_rates[i]

# 초기 인구 분포 (임의)
initial_population = np.array([500000] * 11)

# 시뮬레이션 연도 고정 (세대 단위 50)
years = 50
populations = [initial_population]

for _ in range(years):
    next_gen = leslie_matrix @ populations[-1]
    populations.append(next_gen)

populations = np.array(populations)

# 인구 변화 시각화
st.subheader("📊 세대별 연령 인구 변화 시뮬레이션")
fig, ax = plt.subplots()
for i in range(11):
    ax.plot(populations[:, i], label=f"{i*10}대")
ax.set_xlabel("세대 (년)")
ax.set_ylabel("인구")
ax.legend()
st.pyplot(fig)

# 접종 가능 인구: 0~60대까지
last_population = populations[-1]
vaccinable_population = np.sum(last_population[:7])
total_population = np.sum(last_population)
v_ratio = vaccinable_population / total_population

st.subheader("📉 접종 가능 인구 비율 vs 집단면역 조건")
st.markdown(f"""
- 현재 인구 구조 기준 접종 가능 인구 비율: **{v_ratio*100:.1f}%**  
- 필요한 최소 면역자 비율 (pₙ): **{p_immune*100:.1f}%**
""")

# 경고 출력
if v_ratio < p_immune:
    st.error("⚠️ 현재 인구 구조로는 집단면역 달성 어려움")
else:
    st.success("✅ 현재 인구 구조로도 집단면역 달성 가능")

st.caption("© 2025. kimjaeyul제작")
