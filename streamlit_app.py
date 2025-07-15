import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit UI
st.set_page_config(layout="wide")
st.title("📉 세대별 연령 인구 변화 시뮬레이션")

# 초기 설정
age_groups = [f"{i}~{i+9}" for i in range(0, 100, 10)] + ["100세 이상"]
num_groups = len(age_groups)

# 초기 인구 분포 설정 (예시)
initial_population = np.array([10000, 9500, 9000, 8500, 8000, 7500, 7000, 6500, 6000, 5500, 5000])

# 기대 여명 (각 연령대에서 다음 연령대로 생존할 확률)
survival_rates = np.array([0.99, 0.985, 0.98, 0.97, 0.95, 0.9, 0.85, 0.8, 0.7, 0.5, 0.3])

# 출산율 (0~9세 그룹으로 들어오는 인구 수 생성용)
fertility_rates = np.array([0, 0, 0.2, 0.3, 0.3, 0.1, 0, 0, 0, 0, 0])

# 슬라이더로 시뮬레이션 연도 수 설정 (고정 50으로 할 수도 있음)
years = 20

# 시뮬레이션 저장
pop_by_year = [initial_population]

for _ in range(years):
    current = pop_by_year[-1]
    next_gen = np.zeros(num_groups)

    # 출산
    next_gen[0] = np.sum(current * fertility_rates)

    # 생존 및 이동
    for i in range(1, num_groups):
        next_gen[i] = current[i - 1] * survival_rates[i - 1]

    pop_by_year.append(next_gen)

pop_by_year = np.array(pop_by_year)

# 그래프 시각화
st.subheader("📊 세대별 연령 인구 변화 시뮬레이션")
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(num_groups):
    ax.plot(range(years + 1), pop_by_year[:, i], label=age_groups[i])
ax.set_xlabel("연도 (5년 단위)")
ax.set_ylabel("인구 수")
ax.set_title("세대별 인구 변화 추이")
ax.legend()
st.pyplot(fig)

# 집단면역 계산
st.subheader("🧪 접종 가능 인구 비율 vs 집단면역 조건")

# 집단면역에 포함 가능한 나이대: 예) 20세 이상
eligible = np.sum(pop_by_year[-1][2:])  # 20세 이상
total_pop = np.sum(pop_by_year[-1])
eligible_ratio = eligible / total_pop * 100
R0 = 3.3
herd_thresh = (1 - 1 / R0) * 100

st.markdown(f"- 현재 인구 구조 기준 접종 가능 인구 비율: **{eligible_ratio:.1f}%**")
st.markdown(f"- 필요한 최소 면역자 비율 (pₙ): **{herd_thresh:.1f}%**")

if eligible_ratio >= herd_thresh:
    st.success("✅ 현재 인구 구조로도 집단면역 달성 가능")
else:
    st.error("⚠️ 현재 인구 구조로는 집단면역 달성 어려움")
