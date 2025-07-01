# health_risk_app_mobile_optimized_with_effects.py
import streamlit as st
import time

# 모바일 최적화된 페이지 설정
st.set_page_config(
    page_title="건강 위험 평가",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 모바일 친화적 CSS 스타일 적용 (애니메이션 효과 추가)
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
        animation: fadeIn 1s ease-in;
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
    
    /* 결과 박스 기본 스타일 */
    .result-box {
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 6px solid #1f77b4;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        transform: translateY(0);
        position: relative;
        overflow: hidden;
    }
    
    /* 결과 박스 호버 효과 */
    .result-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* 포커스 효과 - 값이 변경될 때 적용 */
    .result-box.focused {
        animation: focusGlow 1.5s ease-in-out;
        border-left-width: 8px;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 30px rgba(0,0,0,0.2);
    }
    
    /* 위험도별 색상 및 효과 */
    .low-risk { 
        border-left-color: #4caf50;
        background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%);
    }
    .low-risk.focused {
        box-shadow: 0 12px 30px rgba(76, 175, 80, 0.3);
        animation: focusGlowGreen 1.5s ease-in-out;
    }
    
    .medium-risk { 
        border-left-color: #ff9800;
        background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%);
    }
    .medium-risk.focused {
        box-shadow: 0 12px 30px rgba(255, 152, 0, 0.3);
        animation: focusGlowOrange 1.5s ease-in-out;
    }
    
    .high-risk { 
        border-left-color: #f44336;
        background: linear-gradient(135deg, #ffebee 0%, #ffffff 100%);
    }
    .high-risk.focused {
        box-shadow: 0 12px 30px rgba(244, 67, 54, 0.3);
        animation: focusGlowRed 1.5s ease-in-out;
    }
    
    /* 스코어 숫자 스타일 */
    .score-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .score-number.updated {
        animation: scoreUpdate 0.8s ease-in-out;
        color: #1f77b4;
    }
    
    /* 위험도 레벨 스타일 */
    .risk-level {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        padding: 0.5rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .risk-level.low { 
        background: rgba(76, 175, 80, 0.1);
        color: #2e7d32;
        border: 2px solid rgba(76, 175, 80, 0.3);
    }
    
    .risk-level.medium { 
        background: rgba(255, 152, 0, 0.1);
        color: #ef6c00;
        border: 2px solid rgba(255, 152, 0, 0.3);
    }
    
    .risk-level.high { 
        background: rgba(244, 67, 54, 0.1);
        color: #c62828;
        border: 2px solid rgba(244, 67, 54, 0.3);
    }
    
    /* 진행 바 스타일 */
    .progress-bar-container {
        background: #e0e0e0;
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 4px;
        transition: width 1s ease-in-out;
        position: relative;
    }
    
    .progress-bar.low { background: linear-gradient(90deg, #4caf50, #66bb6a); }
    .progress-bar.medium { background: linear-gradient(90deg, #ff9800, #ffb74d); }
    .progress-bar.high { background: linear-gradient(90deg, #f44336, #ef5350); }
    
    /* 애니메이션 정의 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes focusGlow {
        0% { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        50% { box-shadow: 0 16px 40px rgba(31, 119, 180, 0.4); }
        100% { box-shadow: 0 12px 30px rgba(0,0,0,0.2); }
    }
    
    @keyframes focusGlowGreen {
        0% { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        50% { box-shadow: 0 16px 40px rgba(76, 175, 80, 0.5); }
        100% { box-shadow: 0 12px 30px rgba(76, 175, 80, 0.3); }
    }
    
    @keyframes focusGlowOrange {
        0% { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        50% { box-shadow: 0 16px 40px rgba(255, 152, 0, 0.5); }
        100% { box-shadow: 0 12px 30px rgba(255, 152, 0, 0.3); }
    }
    
    @keyframes focusGlowRed {
        0% { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        50% { box-shadow: 0 16px 40px rgba(244, 67, 54, 0.5); }
        100% { box-shadow: 0 12px 30px rgba(244, 67, 54, 0.3); }
    }
    
    @keyframes scoreUpdate {
        0% { transform: scale(1); }
        50% { transform: scale(1.3); color: #ff4444; }
        100% { transform: scale(1); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* 모바일 반응형 */
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }
        .section-title { font-size: 1.2rem; }
        .result-box { padding: 1rem; }
        .score-number { font-size: 2rem; }
        .risk-level { font-size: 1rem; }
    }
    
    /* 펄스 효과 */
    .pulsing {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화 (이전 값 추적용)
if 'prev_stroke_score' not in st.session_state:
    st.session_state.prev_stroke_score = 0
if 'prev_heart_score' not in st.session_state:
    st.session_state.prev_heart_score = 0
if 'prev_diab_score' not in st.session_state:
    st.session_state.prev_diab_score = 0
if 'focus_stroke' not in st.session_state:
    st.session_state.focus_stroke = False
if 'focus_heart' not in st.session_state:
    st.session_state.focus_heart = False
if 'focus_diab' not in st.session_state:
    st.session_state.focus_diab = False

# 메인 제목
st.markdown('<div class="main-title">💡 건강 위험 평가 시스템</div>', unsafe_allow_html=True)
st.markdown("**입력값을 바탕으로 각 질환의 발병 위험도를 실시간으로 계산합니다.**")

# 입력 섹션
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

# 계산 함수들
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

def get_risk_level_and_class(score, risk_type):
    """위험도 레벨, 색상 클래스, 진행률 반환"""
    if risk_type == "stroke":
        if score <= 10: return "낮음", "low-risk", "low", min(100, score * 10)
        elif score <= 22: return "보통", "medium-risk", "medium", min(100, score * 4.5)
        else: return "높음", "high-risk", "high", min(100, score * 3)
    elif risk_type == "diabetes":
        if score <= 4: return "낮음", "low-risk", "low", min(100, score * 25)
        elif score <= 7: return "보통", "medium-risk", "medium", min(100, score * 14)
        else: return "높음", "high-risk", "high", min(100, score * 10)
    else:  # heart
        if score <= 10: return "낮음", "low-risk", "low", min(100, score * 10)
        elif score <= 20: return "보통", "medium-risk", "medium", min(100, score * 5)
        else: return "높음", "high-risk", "high", min(100, score * 3.3)

def create_result_box(title, icon, score, risk_level, risk_class, progress_class, progress_percent, is_focused=False):
    """결과 박스 HTML 생성"""
    focus_class = "focused" if is_focused else ""
    score_class = "updated" if is_focused else ""
    
    return f"""
    <div class="result-box {risk_class} {focus_class}">
        <h3 style="text-align: center; margin-bottom: 1rem; color: #333;">
            {icon} {title}
        </h3>
        <div class="score-number {score_class}">{score}</div>
        <div class="risk-level {progress_class}">위험도: {risk_level}</div>
        <div class="progress-bar-container">
            <div class="progress-bar {progress_class}" style="width: {progress_percent}%;"></div>
        </div>
        <div style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 0.5rem;">
            위험도 {progress_percent:.0f}%
        </div>
    </div>
    """

# 결과 계산
stroke_score = calc_stroke_score()
heart_score = calc_heart_score()
diab_score = calc_diabetes_score()

# 변화 감지 및 포커스 설정
if stroke_score != st.session_state.prev_stroke_score:
    st.session_state.focus_stroke = True
    st.session_state.prev_stroke_score = stroke_score
else:
    st.session_state.focus_stroke = False

if heart_score != st.session_state.prev_heart_score:
    st.session_state.focus_heart = True
    st.session_state.prev_heart_score = heart_score
else:
    st.session_state.focus_heart = False

if diab_score != st.session_state.prev_diab_score:
    st.session_state.focus_diab = True
    st.session_state.prev_diab_score = diab_score
else:
    st.session_state.focus_diab = False

# 결과 표시
st.markdown("---")
st.markdown("## 📊 위험도 평가 결과")

# 3개 컬럼으로 결과 표시 (애니메이션 효과 적용)
col1, col2, col3 = st.columns(3)

with col1:
    risk_level, risk_class, progress_class, progress_percent = get_risk_level_and_class(stroke_score, "stroke")
    result_html = create_result_box(
        "뇌졸중", "🧠", stroke_score, risk_level, risk_class, 
        progress_class, progress_percent, st.session_state.focus_stroke
    )
    st.markdown(result_html, unsafe_allow_html=True)
    
    # 상세 정보
    if stroke_score <= 10:
        st.info("🟢 10년 위험률: 1% 미만")
    elif stroke_score <= 17:
        st.warning("🟡 10년 위험률: 1-2%")
    elif stroke_score <= 22:
        st.warning("🟡 10년 위험률: 2-3%")
    else:
        st.error("🔴 10년 위험률: 4% 이상")

with col2:
    risk_level, risk_class, progress_class, progress_percent = get_risk_level_and_class(heart_score, "heart")
    result_html = create_result_box(
        "심혈관질환", "❤️", heart_score, risk_level, risk_class, 
        progress_class, progress_percent, st.session_state.focus_heart
    )
    st.markdown(result_html, unsafe_allow_html=True)
    
    risk_percent = min(30, heart_score * 2)
    if risk_percent < 10:
        st.info(f"🟢 10년 위험률: {risk_percent}%")
    elif risk_percent < 20:
        st.warning(f"🟡 10년 위험률: {risk_percent}%")
    else:
        st.error(f"🔴 10년 위험률: {risk_percent}%")

with col3:
    risk_level, risk_class, progress_class, progress_percent = get_risk_level_and_class(diab_score, "diabetes")
    result_html = create_result_box(
        "당뇨병", "🍬", diab_score, risk_level, risk_class, 
        progress_class, progress_percent, st.session_state.focus_diab
    )
    st.markdown(result_html, unsafe_allow_html=True)
    
    if diab_score <= 4:
        st.info("🟢 위험도: 낮음")
    elif diab_score <= 7:
        st.warning("🟡 위험도: 보통 (2배)")
    elif diab_score <= 9:
        st.warning("🟡 위험도: 높음 (3배)")
    else:
        st.error("🔴 위험도: 매우 높음 (3배 이상)")

# 실시간 업데이트 알림
if any([st.session_state.focus_stroke, st.session_state.focus_heart, st.session_state.focus_diab]):
    st.markdown("""
    <div style="background: linear-gradient(90deg, #4CAF50, #2196F3); 
                color: white; padding: 1rem; border-radius: 10px; 
                text-align: center; margin: 1rem 0; animation: fadeIn 0.5s ease-in;">
        ✨ 위험도가 업데이트되었습니다!
    </div>
    """, unsafe_allow_html=True)

# 전체 위험도 요약
st.markdown("---")
st.markdown("### 📈 종합 위험도 분석")

total_risk_score = (stroke_score + heart_score + diab_score) / 3
if total_risk_score <= 8:
    summary_color = "#4CAF50"
    summary_icon = "🟢"
    summary_text = "전반적으로 양호한 상태입니다."
elif total_risk_score <= 15:
    summary_color = "#FF9800"
    summary_icon = "🟡"
    summary_text = "주의가 필요한 상태입니다."
else:
    summary_color = "#F44336"
    summary_icon = "🔴"
    summary_text = "적극적인 관리가 필요합니다."

st.markdown(f"""
<div style="background: linear-gradient(135deg, {summary_color}20, #ffffff); 
            border: 2px solid {summary_color}40; border-radius: 15px; 
            padding: 1.5rem; text-align: center; margin: 1rem 0;">
    <h3 style="color: {summary_color}; margin-bottom: 1rem;">
        {summary_icon} 종합 평가
    </h3>
    <p style="font-size: 1.1rem; font-weight: bold; color: #333;">
        평균 위험도: {total_risk_score:.1f}점
    </p>
    <p style="color: #666;">{summary_text}</p>
</div>
""", unsafe_allow_html=True)

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
    "정확한 건강 상태는 전문의와 상담하시기 바랍니다.by BJ"
    "</div>", 
    unsafe_allow_html=True
)

# 자동 새로고침을 위한 스크립트 (선택사항)
st.markdown("""
<script>
    // 페이지 포커스 시 자동 새로고침 (선택사항)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            setTimeout(() => {
                const focused = document.querySelectorAll('.result-box.focused');
                focused.forEach(box => {
                    box.classList.remove('focused');
                });
            }, 2000);
        }
    });
</script>
""", unsafe_allow_html=True)
