import streamlit as st
import pandas as pd

# --- 1. 가상의(Dummy) 감염병 데이터 생성 ---
# 실제 데이터가 아니며, 기능을 시연하기 위한 예시 데이터입니다.
# 2024년 기준 최신 데이터를 가정합니다. (실제 데이터는 질병관리청 등에서 확인 필요)

data = {
    '지역': ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
             '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도',
             '충청북도', '충청남도', '전라북도', '전라남도', '경상북도',
             '경상남도', '제주특별자치도'],
    '인구수_2024_가상': [9400000, 3300000, 2400000, 3000000, 1400000,
                       1450000, 1100000, 390000, 13600000, 1500000,
                       1650000, 2150000, 1750000, 1800000, 2600000,
                       3300000, 680000],
    '독감_환자수_2024_가상': [282000, 99000, 72000, 90000, 42000,
                             43500, 33000, 11700, 408000, 45000,
                             49500, 64500, 52500, 54000, 78000,
                             99000, 20400],
    '결핵_환자수_2024_가상': [9400, 3300, 2400, 3000, 1400,
                           1450, 1100, 390, 13600, 1500,
                           1650, 2150, 1750, 1800, 2600,
                           3300, 680],
    '수족구병_환자수_2024_가상': [47000, 16500, 12000, 15000, 7000,
                                 7250, 5500, 1950, 68000, 7500,
                                 8250, 10750, 8750, 9000, 13000,
                                 16500, 3400],
    '노로바이러스_환자수_2024_가상': [18800, 6600, 4800, 6000, 2800,
                                   2900, 2200, 780, 27200, 3000,
                                   3300, 4300, 3500, 3600, 5200,
                                   6600, 1360],
    '일본뇌염_환자수_2024_가상': [94, 165, 72, 90, 70, # 남부 지역 환자수 상향 조정
                              73, 55, 19, 136, 45,
                              49, 107, 87, 180, 130, # 남부 지역 환자수 상향 조정
                              165, 102], # 제주 지역 상향 조정
    '비브리오패혈증_환자수_2024_가상': [0, 66, 0, 90, 0, # 해안 지역 위주 발생
                                   0, 55, 0, 0, 0,
                                   0, 107, 175, 270, 130, # 서남해안 지역 상향 조정
                                   165, 68] # 제주 지역 상향 조정
}

df = pd.DataFrame(data)

# 각 질병의 퍼센트 계산 함수
def calculate_percentage(row, disease_col_prefix):
    disease_name = disease_col_prefix.split('_')[0]
    patient_col = f'{disease_name}_환자수_2024_가상'

    total_patients = row[patient_col]
    population = row['인구수_2024_가상']
    return (total_patients / population) * 100 if population > 0 else 0.0

# 모든 감염병 퍼센트 칼럼 추가
disease_names = ['독감', '결핵', '수족구병', '노로바이러스', '일본뇌염', '비브리오패혈증']
for disease in disease_names:
    df[f'{disease}_퍼센트'] = df.apply(lambda row: calculate_percentage(row, disease), axis=1)

# --- Streamlit 앱 구성 ---
st.set_page_config(layout="centered") # 페이지 레이아웃 설정
st.title("🇰🇷 대한민국 지역별 주요 감염병 현황")
st.markdown("---")
st.write("2024년 가상 데이터를 기반으로, 대한민국 시/도별 주요 감염병 유병률(퍼센트)을 보여드립니다.")
st.write("아래 드롭다운 메뉴에서 지역을 선택해주세요.")

# 지역 목록 생성
regions = df['지역'].tolist()
# 스트림릿 selectbox를 사용하여 지역 선택 UI 생성
selected_region = st.selectbox(
    "**지역을 선택해주세요:**",
    regions
)

# 선택된 지역에 대한 정보 표시
if selected_region:
    selected_row = df[df['지역'] == selected_region].iloc[0]
    population = selected_row['인구수_2024_가상']

    st.subheader(f"📍 {selected_region} ({population:,}명)의 주요 감염병 현황")

    diseases_info = {}
    for disease in disease_names:
        percentage_col = f'{disease}_퍼센트'
        if percentage_col in selected_row:
            diseases_info[disease] = selected_row[percentage_col]

    # 퍼센트가 높은 순서대로 정렬하여 상위 3개만 선택
    sorted_diseases = sorted(diseases_info.items(), key=lambda item: item[1], reverse=True)[:3]

    if sorted_diseases:
        for i, (disease, percentage) in enumerate(sorted_diseases):
            patient_count_col = f'{disease}_환자수_2024_가상'
            patient_count = selected_row[patient_count_col] if patient_count_col in selected_row else 'N/A'
            st.write(f"**{i+1}. {disease}:** {percentage:.2f}% (환자수: {patient_count:,}명)")
        st.markdown("---")
        st.info("💡 **참고:** 이 데이터는 실제 통계가 아닌, 앱 기능 시연을 위한 가상 데이터입니다.")
    else:
        st.warning("선택하신 지역에 대한 주요 감염병 정보가 부족합니다.")
