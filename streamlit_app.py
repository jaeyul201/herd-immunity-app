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
R0 = st.slider("기초감염재생산수 (R₀)", min_value=1.0, max_value=10.0, step=0.1, value=3.0)
p_immune = 1 - 1 / R0
st.metric("필요한 최소 면역자 비율", f"{p_immune*100:.1f}%")

st.divider()

# 레슬리 행렬 구성
fertility_rate = 0.75  # 합계출산율
survival_rates = [0.99, 0.99, 0.98, 0.97, 0.95, 0.92, 0.88, 0.80, 0.65, 0.45]  # 연령별 생존율

# 초기 인구 분포 (대한민국 추정 구조 반영)
initial_population = [
    700000, 750000, 800000, 750000, 700000,
    650000, 550000, 450000, 300000, 150000, 50000
]

leslie_matrix = np.zeros((11, 11))
leslie_matrix[0, 2:6] = fertility_rate / 4  # 출산 가능 연령: 20~49세

for i in range(10):
    leslie_matrix[i + 1, i] = survival_rates[i]

years = 50
populations = [np.array(initial_population)]

for _ in range(years):
    next_gen = leslie_matrix @ populations[-1]
    populations.append(next_gen)

populations = np.array(populations)

# 인구 구조 변화 시각화
st.subheader("📊 연령대별 인구 구조 변화 시뮬레이션")

fig, ax = plt.subplots()
for i in range(11):
    ax.plot(populations[:, i], label=f"{i*10}대")
ax.set_xlabel("세대 (년)")
ax.set_ylabel("인구 수")
ax.legend()
st.pyplot(fig)

# 집단면역 달성 가능성 평가
eligible = sum(initial_population[2:7])  # 20~69세
total = sum(initial_population)
if eligible / total < p_immune:
    st.error("⚠️ 현재 인구 구조로는 이론상 집단면역 달성이 어려울 수 있습니다.")
else:
    st.success("✅ 현재 인구 구조로도 이론상 집단면역 달성이 가능합니다.")

st.caption("© 2025. kimjaeyul제작")
