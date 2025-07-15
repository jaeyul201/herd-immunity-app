import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 이미지 불러오기
image = Image.open("capybara.png")
st.image(image, caption="Capybara & Herd Immunity Simulation", use_column_width=True)

# 앱 타이틀
st.title("🦠 집단면역 시뮬레이션")

# 설명 텍스트
st.markdown("""
이 앱은 기초감염재생산수(R₀)에 따라 이론적 집단면역 조건을 계산하고,  
현재 연령대별 인구 구조를 바탕으로 실제로 면역자가 전체 인구 중  
얼마나 되는지 비교할 수 있도록 만든 시뮬레이션 앱입니다.
""")

# 슬라이더: R₀ 값 설정
R0 = st.slider("기초감염재생산수 R₀", min_value=1.0, max_value=10.0, value=3.0, step=0.1)

# 집단면역 임계값 계산
herd_threshold = 1 - (1 / R0)
herd_threshold_percent = herd_threshold * 100
st.markdown(f"**이론적 집단면역 달성 최소 면역자 비율:** {herd_threshold_percent:.1f}%")

# -------------------------------
# 연령대별 인구 시뮬레이션
# -------------------------------

st.subheader("📊 연령대별 인구 구조 변화 시뮬레이션")

# 연령 구간 (10세 단위)
age_labels = [f"{i}~{i+9}" for i in range(0, 100, 10)] + ["100세 이상"]
n_age = len(age_labels)

# 초기 인구 구조 (예시값)
initial_population = np.array([10000, 9500, 9000, 8500, 8000, 7500, 7000, 6500, 6000, 5500, 5000])

# 생존율 (다음 연령대로 넘어갈 확률)
survival_rates = np.array([0.99, 0.985, 0.98, 0.97, 0.95, 0.9, 0.85, 0.8, 0.7, 0.5, 0.3])

# 출산율 (신생아로 유입되는 수 비율)
fertility_rates = np.array([0, 0, 0.2, 0.3, 0.3, 0.1, 0, 0, 0, 0, 0])

# 시뮬레이션 연도 수
years = 20
population_by_year = [initial_population]

for _ in range(years):
    current = population_by_year[-1]
    next_gen = np.zeros(n_age)
    
    # 출산
    next_gen[0] = np.sum(current * fertility_rates)
    
    # 생존 및 이동
    for i in range(1, n_age):
        next_gen[i] = current[i - 1] * survival_rates[i - 1]
    
    population_by_year.append(next_gen)

population_by_year = np.array(population_by_year)

# 그래프
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(n_age):
    ax.plot(range(years + 1), population_by_year[:, i], label=age_labels[i])
ax.set_xlabel("년 (단위: 1년)")
ax.set_ylabel("인구 수")
ax.set_title("세대별 연령 인구 변화 시뮬레이션")
ax.legend()
st.pyplot(fig)

# -------------------------------
# 집단면역 달성 가능성 분석
# -------------------------------

st.subheader("📌 접종 가능 인구 비율 vs 집단면역 조건")

# 예시: 20세 이상만 백신 가능하다고 가정
vaccinable_pop = population_by_year[-1][2:]  # 20세 이상
vaccinable_ratio = np.sum(vaccinable_pop) / np.sum(population_by_year[-1]) * 100

st.markdown(f"- 현재 인구 구조 기준 접종 가능 인구 비율: **{vaccinable_ratio:.1f}%**")
st.markdown(f"- 필요한 최소 면역자 비율: **{herd_threshold_percent:.1f}%**")

if vaccinable_ratio >= herd_threshold_percent:
    st.success("✅ 현재 인구 구조로도 집단면역 달성 가능")
else:
    st.error("⚠️ 현재 인구 구조로는 집단면역 달성 어려움")

