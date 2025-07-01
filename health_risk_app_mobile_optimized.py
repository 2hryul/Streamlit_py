# health_risk_app_with_bar_charts.py
import streamlit as st
import pandas as pd
import numpy as np

# 모바일 최적화된 페이지 설정
st.set_page_config(
    page_title="건강 위험 평가",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 적용
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    .main-title {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-in;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .chart-container.updated {
        animation: chartUpdate 1.5s ease-in-out;
        border: 2px solid #007bff;
        box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
    }
    
    .chart-title {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        color: #495057;
    }
    
    .value-comparison {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    .prev-value {
        color: #6c757d;
        text-decoration: line-through;
    }
    
    .current-value {
        color: #007bff;
        font-weight: bold;
    }
    
    .change-indicator {
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .change-up {
        background: #dc3545;
        color: white;
    }
    
    .change-down {
        background: #28a745;
        color: white;
    }
    
    .change-same {
        background: #6c757d;
        color: white;
    }
    
    .risk-summary {
        text-align: center;
        padding: 0.8rem;
        border-radius: 8px;
        margin-top: 0.5rem;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .risk-low { 
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border: 2px solid #b1dfbb;
    }
    .risk-medium { 
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        color: #856404;
        border: 2px solid #f1c40f;
    }
    .risk-high { 
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        color: #721c24;
        border: 2px solid #e74c3c;
    }
    
    /* 프로그레스 바 스타일 */
    .progress-container {
        background: #e9ecef;
        height: 25px;
        border-radius: 12px;
        overflow: hidden;
        margin: 0.5rem 0;
        position: relative;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 12px;
        transition: width 1s ease-in-out;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .progress-low { 
        background: linear-gradient(90deg, #28a745, #20c997);
    }
    .progress-medium { 
        background: linear-gradient(90deg, #ffc107, #fd7e14);
    }
    .progress-high { 
        background: linear-gradient(90deg, #dc3545, #e74c3c);
    }
    
    .score-display {
        background: #fff;
        border: 3px solid #007bff;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem auto;
        font-size: 1.5rem;
        font-weight: bold;
        color: #007bff;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .score-display.updated {
        animation: scoreUpdate 1s ease-in-out;
        transform: scale(1.1);
    }
    
    .comparison-bars {
        display: flex;
        align-items: end;
        justify-content: center;
        gap: 20px;
        margin: 1rem 0;
        height: 200px;
    }
    
    .bar {
        width: 60px;
        background: linear-gradient(to top, #007bff, #0056b3);
        border-radius: 4px 4px 0 0;
        position: relative;
        transition: all 0.8s ease;
        display: flex;
        align-items: end;
        justify-content: center;
        color: white;
        font-weight: bold;
        padding-bottom: 8px;
    }
    
    .bar.prev {
        background: linear-gradient(to top, #6c757d, #495057);
        opacity: 0.5;
    }
    
    .bar-label {
        position: absolute;
        bottom: -25px;
        text-align: center;
        font-size: 0.8rem;
        color: #495057;
        font-weight: bold;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes chartUpdate {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    @keyframes scoreUpdate {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1.1); }
    }
    
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }
        .chart-container { padding: 1rem; }
        .value-comparison { flex-direction: column; gap: 0.5rem; }
        .comparison-bars { height: 150px; }
        .bar { width: 40px; }
        .score-display { width: 60px; height: 60px; font-size: 1.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'prev_stroke_score' not in st.session_state:
    st.session_state.prev_stroke_score = 0
if 'prev_heart_score' not in st.session_state:
    st.session_state.prev_heart_score = 0
if 'prev_diab_score' not in st.session_state:
    st.session_state.prev_diab_score = 0
if 'is_first_run' not in st.session_state:
    st.session_state.is_first_run = True

# 메인 제목
st.markdown('<div class="main-title">💡 건강 위험 평가 시스템</div>', unsafe_allow_html=True)
st.markdown("**입력값을 바탕으로 각 질환의 발병 위험도를 실시간으로 계산하고 변화를 시각화합니다.**")

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

def get_risk_info(score, disease_type):
    """위험도 정보 반환"""
    if disease_type == "stroke":
        if score <= 10:
            return "낮음", "risk-low", "progress-low", "1% 미만", 25
        elif score <= 22:
            return "보통", "risk-medium", "progress-medium", "1-3%", 40
        else:
            return "높음", "risk-high", "progress-high", "4% 이상", 40
    elif disease_type == "heart":
        risk_percent = min(30, score * 2)
        if risk_percent < 10:
            return "낮음", "risk-low", "progress-low", f"{risk_percent}%", 35
        elif risk_percent < 20:
            return "보통", "risk-medium", "progress-medium", f"{risk_percent}%", 35
        else:
            return "높음", "risk-high", "progress-high", f"{risk_percent}%", 35
    else:  # diabetes
        if score <= 4:
            return "낮음", "risk-low", "progress-low", "기준 대비 1배", 15
        elif score <= 7:
            return "보통", "risk-medium", "progress-medium", "기준 대비 2배", 15
        else:
            return "높음", "risk-high", "progress-high", "기준 대비 3배 이상", 15

def create_comparison_bars(current_score, prev_score, max_score):
    """비교 막대 HTML 생성"""
    current_height = min(180, (current_score / max_score) * 180)
    prev_height = min(180, (prev_score / max_score) * 180) if prev_score > 0 else 0
    
    return f"""
    <div class="comparison-bars">
        <div class="bar prev" style="height: {prev_height}px;">
            <div class="bar-label">이전<br>{prev_score}</div>
            {prev_score if prev_score > 0 else ''}
        </div>
        <div class="bar" style="height: {current_height}px;">
            <div class="bar-label">현재<br>{current_score}</div>
            {current_score}
        </div>
    </div>
    """

def create_change_indicator(current, prev):
    """변화 지시자 생성"""
    if current > prev:
        return f'<span class="change-indicator change-up">↑ +{current-prev}</span>'
    elif current < prev:
        return f'<span class="change-indicator change-down">↓ -{prev-current}</span>'
    else:
        return f'<span class="change-indicator change-same">= 동일</span>'

# 결과 계산
stroke_score = calc_stroke_score()
heart_score = calc_heart_score()
diab_score = calc_diabetes_score()

# 변화 감지
stroke_changed = stroke_score != st.session_state.prev_stroke_score
heart_changed = heart_score != st.session_state.prev_heart_score
diab_changed = diab_score != st.session_state.prev_diab_score

# 결과 표시
st.markdown("---")
st.markdown("## 📊 위험도 평가 결과")

# 전체 변화 요약
if not st.session_state.is_first_run and (stroke_changed or heart_changed or diab_changed):
    changes = []
    if stroke_changed:
        changes.append(f"뇌졸중: {st.session_state.prev_stroke_score}→{stroke_score}")
    if heart_changed:
        changes.append(f"심혈관: {st.session_state.prev_heart_score}→{heart_score}")
    if diab_changed:
        changes.append(f"당뇨병: {st.session_state.prev_diab_score}→{diab_score}")
    
    st.info(f"🔄 **변화 감지**: {', '.join(changes)}")

# 3개 컬럼으로 차트 표시
col1, col2, col3 = st.columns(3)

with col1:
    container_class = "chart-container updated" if stroke_changed else "chart-container"
    st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
    
    # 제목
    st.markdown('<div class="chart-title">🧠 뇌졸중 위험도</div>', unsafe_allow_html=True)
    
    # 점수 표시
    score_class = "updated" if stroke_changed else ""
    st.markdown(f'<div class="score-display {score_class}">{stroke_score}</div>', unsafe_allow_html=True)
    
    # 위험도 정보
    risk_level, risk_class, progress_class, risk_text, max_score = get_risk_info(stroke_score, "stroke")
    
    # 프로그레스 바
    progress_width = min(100, (stroke_score / max_score) * 100)
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar {progress_class}" style="width: {progress_width}%;">
            {stroke_score}/{max_score}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 위험도 요약
    st.markdown(f'<div class="risk-summary {risk_class}">{risk_level} 위험도<br>({risk_text})</div>', unsafe_allow_html=True)
    
    # 비교 막대
    if not st.session_state.is_first_run:
        comparison_html = create_comparison_bars(stroke_score, st.session_state.prev_stroke_score, max_score)
        st.markdown(comparison_html, unsafe_allow_html=True)
        
        # 변화 정보
        change_html = f"""
        <div class="value-comparison">
            <div>
                <span class="prev-value">이전: {st.session_state.prev_stroke_score}</span>
                <span class="current-value">현재: {stroke_score}</span>
            </div>
            {create_change_indicator(stroke_score, st.session_state.prev_stroke_score)}
        </div>
        """
        st.markdown(change_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    container_class = "chart-container updated" if heart_changed else "chart-container"
    st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
    
    # 제목
    st.markdown('<div class="chart-title">❤️ 심혈관질환 위험도</div>', unsafe_allow_html=True)
    
    # 점수 표시
    score_class = "updated" if heart_changed else ""
    st.markdown(f'<div class="score-display {score_class}">{heart_score}</div>', unsafe_allow_html=True)
    
    # 위험도 정보
    risk_level, risk_class, progress_class, risk_text, max_score = get_risk_info(heart_score, "heart")
    
    # 프로그레스 바
    progress_width = min(100, (heart_score / max_score) * 100)
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar {progress_class}" style="width: {progress_width}%;">
            {heart_score}/{max_score}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 위험도 요약
    st.markdown(f'<div class="risk-summary {risk_class}">{risk_level} 위험도<br>({risk_text})</div>', unsafe_allow_html=True)
    
    # 비교 막대
    if not st.session_state.is_first_run:
        comparison_html = create_comparison_bars(heart_score, st.session_state.prev_heart_score, max_score)
        st.markdown(comparison_html, unsafe_allow_html=True)
        
        # 변화 정보
        change_html = f"""
        <div class="value-comparison">
            <div>
                <span class="prev-value">이전: {st.session_state.prev_heart_score}</span>
                <span class="current-value">현재: {heart_score}</span>
            </div>
            {create_change_indicator(heart_score, st.session_state.prev_heart_score)}
        </div>
        """
        st.markdown(change_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    container_class = "chart-container updated" if diab_changed else "chart-container"
    st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
    
    # 제목
    st.markdown('<div class="chart-title">🍬 당뇨병 위험도</div>', unsafe_allow_html=True)
    
    # 점수 표시
    score_class = "updated" if diab_changed else ""
    st.markdown(f'<div class="score-display {score_class}">{diab_score}</div>', unsafe_allow_html=True)
    
    # 위험도 정보
    risk_level, risk_class, progress_class, risk_text, max_score = get_risk_info(diab_score, "diabetes")
    
    # 프로그레스 바
    progress_width = min(100, (diab_score / max_score) * 100)
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar {progress_class}" style="width: {progress_width}%;">
            {diab_score}/{max_score}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 위험도 요약
    st.markdown(f'<div class="risk-summary {risk_class}">{risk_level} 위험도<br>({risk_text})</div>', unsafe_allow_html=True)
    
    # 비교 막대
    if not st.session_state.is_first_run:
        comparison_html = create_comparison_bars(diab_score, st.session_state.prev_diab_score, max_score)
        st.markdown(comparison_html, unsafe_allow_html=True)
        
        # 변화 정보
        change_html = f"""
        <div class="value-comparison">
            <div>
                <span class="prev-value">이전: {st.session_state.prev_diab_score}</span>
                <span class="current-value">현재: {diab_score}</span>
            </div>
            {create_change_indicator(diab_score, st.session_state.prev_diab_score)}
        </div>
        """
        st.markdown(change_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 종합 분석
st.markdown("---")
st.markdown("### 📈 종합 위험도 분석")

# Streamlit 내장 차트 사용
if not st.session_state.is_first_run:
    chart_data = pd.DataFrame({
        '이전값': [st.session_state.prev_stroke_score, st.session_state.prev_heart_score, st.session_state.prev_diab_score],
        '현재값': [stroke_score, heart_score, diab_score]
    }, index=['뇌졸중', '심혈관질환', '당뇨병'])
    
    st.bar_chart(chart_data, height=400, use_container_width=True)
else:
    chart_data = pd.DataFrame({
        '현재값': [stroke_score, heart_score, diab_score]
    }, index=['뇌졸중', '심혈관질환', '당뇨병'])
    
    st.bar_chart(chart_data, height=400, use_container_width=True)

# 이전 값들 업데이트
st.session_state.prev_stroke_score = stroke_score
st.session_state.prev_heart_score = heart_score
st.session_state.prev_diab_score = diab_score
st.session_state.is_first_run = False

# 추가 정보
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
    "정확한 건강 상태는 전문의와 상담하시기 바랍니다."
    "</div>", 
    unsafe_allow_html=True
)
