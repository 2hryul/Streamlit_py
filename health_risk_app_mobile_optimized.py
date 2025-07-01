# health_risk_app_mobile_optimized.py
import streamlit as st

# 모바일 최적화된 페이지 설정
st.set_page_config(
    page_title="건강 위험 평가",
    page_icon="💡",
    layout="wide",  # wide로 변경하여 모바일에서 더 나은 레이아웃 제공
    initial_sidebar_state="collapsed"  # 사이드바 접기
)

# 모바일 친화적 CSS 스타일 적용
st.markdown("""
<style>
    /* 모바일 최적화 스타일 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* 제목 스타일 */
    .main-title {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    /* 섹션 제목 스타일 */
    .section-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2e7d32;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
    }
    
    /* 결과 박스 스타일 */
    .result-box {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    
    /* 위험도 색상 */
    .low-risk { border-left-color: #4caf50; }
    .medium-risk { border-left-color: #ff9800; }
    .high-risk { border-left-color: #f44336; }
    
    /* 모바일 반응형 */
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }
        .section-title { font-size: 1.2rem; }
        .stSlider > div > div > div { font-size: 0.9rem; }
    }
</style>
""", unsafe_allow_html=True)

# 메인 제목
st.markdown('<div class="main-title">💡 건강 위험 평가 시스템</div>', unsafe_allow_html=True)
st.markdown("**입력값을 바탕으로 각 질환의 발병 위험도를 개별적으로 계산합니다.**")

# 진행 상황 표시
progress_placeholder = st.empty()

# 입력 섹션을 확장 가능하게 만들기
with st.expander("📋 기본 정보 입력", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("나이", 20, 80, 45, help="현재 나이를 선택하세요")
        sex = st.selectbox("성별", ["남성", "여성"])
        smoking = st.selectbox("흡연 상태", ["비흡연자", "남성 흡연자", "여성 흡연자"])
        bmi = st.slider("BMI", 15.0, 40.0, 22.0, step=0.5, help="체질량지수")
    
    with col2:
        systolic_bp = st.slider("수축기 혈압", 90, 200, 120, help="mmHg")
        diastolic_bp = st.slider("이완기 혈압", 60, 120, 80, help="mmHg")
        cholesterol = st.slider("총 콜레스테롤", 100, 300, 180, help="mg/dL")
        hdl = st.slider("HDL 콜레스테롤", 20, 100, 50, help="mg/dL")

with st.expander("🏥 건강 상태 및 생활습관"):
    col1, col2 = st.columns(2)
    
    with col1:
        bp_med = st.checkbox("혈압약 복용 중")
        diabetes = st.checkbox("당뇨병 진단받음")
        bp_history = st.checkbox("혈압 140/90 이상 경험")
        family_diabetes = st.checkbox("가족 중 당뇨병")
    
    with col2:
        waist = st.slider("허리둘레 (cm)", 60, 130, 85)
        alcohol = st.selectbox("음주량 (하루 평균)", ["1잔 미만", "1~4.9잔", "5잔 이상"])

# 계산 함수들 (기존과 동일)
def calc_stroke_score():
    score = 0
    if 50 <= age < 55: score += 6
    elif 55 <= age < 60: score += 12
    elif 60 <= age: score += 16
    
    score += 6 if sex == "남성" else 0
    
    if smoking == "남성 흡연자": score += 4
    elif smoking == "여성 흡연자": score += 8
    
    if bmi >= 30: score += 3
    elif bmi >= 25: score += 2
    
    if bp_med or systolic_bp >= 140 or diastolic_bp >= 90: score += 11
    if diabetes: score += 7
    
    return score

def calc_heart_score():
    score = 0
    if 45 <= age < 50: score += 3
    elif 50 <= age < 55: score += 6
    elif 55 <= age < 60: score += 8
    elif 60 <= age < 65: score += 10
    elif 65 <= age: score += 12
    
    if cholesterol >= 280: score += 10
    elif cholesterol >= 240: score += 8
    elif cholesterol >= 200: score += 6
    elif cholesterol >= 160: score += 3
    
    if smoking != "비흡연자": score += 4
    
    if hdl < 40: score += 2
    elif hdl < 50: score += 1
    
    if systolic_bp >= 160: score += 4
    elif systolic_bp >= 140: score += 3
    elif systolic_bp >= 130: score += 2
    elif systolic_bp >= 120: score += 1
    
    return score

def calc_diabetes_score():
    score = 0
    if age >= 45: score += 3
    if family_diabetes: score += 1
    if bp_history: score += 1
    
    if (sex == "남성" and waist >= 90) or (sex == "여성" and waist >= 84): score += 3
    elif (sex == "남성" and waist >= 84) or (sex == "여성" and waist >= 77): score += 2
    
    if smoking != "비흡연자": score += 1
    
    if alcohol == "1~4.9잔": score += 1
    elif alcohol == "5잔 이상": score += 2
    
    return score

def get_risk_level(score, risk_type):
    """위험도 레벨과 색상 클래스 반환"""
    if risk_type == "stroke":
        if score <= 10: return "낮음", "low-risk"
        elif score <= 22: return "보통", "medium-risk"
        else: return "높음", "high-risk"
    elif risk_type == "diabetes":
        if score <= 4: return "낮음", "low-risk"
        elif score <= 7: return "보통", "medium-risk"
        else: return "높음", "high-risk"
    else:  # heart
        if score <= 10: return "낮음", "low-risk"
        elif score <= 20: return "보통", "medium-risk"
        else: return "높음", "high-risk"

# 결과 계산 및 표시
st.markdown("---")
st.markdown("## 📊 위험도 평가 결과")

# 3개 컬럼으로 결과 표시
col1, col2, col3 = st.columns(3)

with col1:
    stroke_score = calc_stroke_score()
    risk_level, risk_class = get_risk_level(stroke_score, "stroke")
    
    st.markdown(f"""
    <div class="result-box {risk_class}">
        <h4>🧠 뇌졸중</h4>
        <p><strong>점수:</strong> {stroke_score}</p>
        <p><strong>위험도:</strong> {risk_level}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 상세 위험률 표시
    if stroke_score <= 10:
        st.info("10년 위험률: 1% 미만")
    elif stroke_score <= 17:
        st.warning("10년 위험률: 1-2%")
    elif stroke_score <= 22:
        st.warning("10년 위험률: 2-3%")
    else:
        st.error("10년 위험률: 4% 이상")

with col2:
    heart_score = calc_heart_score()
    risk_level, risk_class = get_risk_level(heart_score, "heart")
    
    st.markdown(f"""
    <div class="result-box {risk_class}">
        <h4>❤️ 심혈관질환</h4>
        <p><strong>점수:</strong> {heart_score}</p>
        <p><strong>위험도:</strong> {risk_level}</p>
    </div>
    """, unsafe_allow_html=True)
    
    risk_percent = min(30, heart_score * 2)
    if risk_percent < 10:
        st.info(f"10년 위험률: {risk_percent}%")
    elif risk_percent < 20:
        st.warning(f"10년 위험률: {risk_percent}%")
    else:
        st.error(f"10년 위험률: {risk_percent}%")

with col3:
    diab_score = calc_diabetes_score()
    risk_level, risk_class = get_risk_level(diab_score, "diabetes")
    
    st.markdown(f"""
    <div class="result-box {risk_class}">
        <h4>🍬 당뇨병</h4>
        <p><strong>점수:</strong> {diab_score}</p>
        <p><strong>위험도:</strong> {risk_level}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if diab_score <= 4:
        st.info("위험도: 낮음")
    elif diab_score <= 7:
        st.warning("위험도: 보통 (2배)")
    elif diab_score <= 9:
        st.warning("위험도: 높음 (3배)")
    else:
        st.error("위험도: 매우 높음 (3배 이상)")

# 추가 정보 및 권장사항
st.markdown("---")
with st.expander("💡 건강 관리 권장사항"):
    st.markdown("""
    ### 일반적인 건강 관리 수칙
    - **규칙적인 운동**: 주 3회 이상, 30분 이상
    - **금연**: 흡연 시 모든 질환 위험도 증가
    - **적정 체중 유지**: BMI 18.5-24.9 유지
    - **혈압 관리**: 정기적인 혈압 측정
    - **콜레스테롤 관리**: 연 1회 이상 검사
    - **절주**: 적정 음주량 준수
    
    ⚠️ **주의사항**: 이 결과는 참고용이며, 정확한 진단은 의료진과 상담하세요.
    """)

# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666666; font-size: 0.9rem;'>"
    "본 시스템은 건강 위험도 평가를 위한 참고 도구입니다.<br>"
    "정확한 건강 상태는 전문의와 상담하시기 바랍니다. by BJ"
    "</div>", 
    unsafe_allow_html=True
)
