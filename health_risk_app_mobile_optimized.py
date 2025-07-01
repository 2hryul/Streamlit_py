# health_risk_app_with_bar_charts.py
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
        padding: 0.5rem;
        border-radius: 8px;
        margin-top: 0.5rem;
        font-weight: bold;
    }
    
    .risk-low { background: #d4edda; color: #155724; }
    .risk-medium { background: #fff3cd; color: #856404; }
    .risk-high { background: #f8d7da; color: #721c24; }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes chartUpdate {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }
        .chart-container { padding: 1rem; }
        .value-comparison { flex-direction: column; gap: 0.5rem; }
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
            return "낮음", "risk-low", "#28a745", "1% 미만"
        elif score <= 22:
            return "보통", "risk-medium", "#ffc107", "1-3%"
        else:
            return "높음", "risk-high", "#dc3545", "4% 이상"
    elif disease_type == "heart":
        risk_percent = min(30, score * 2)
        if risk_percent < 10:
            return "낮음", "risk-low", "#28a745", f"{risk_percent}%"
        elif risk_percent < 20:
            return "보통", "risk-medium", "#ffc107", f"{risk_percent}%"
        else:
            return "높음", "risk-high", "#dc3545", f"{risk_percent}%"
    else:  # diabetes
        if score <= 4:
            return "낮음", "risk-low", "#28a745", "기준 대비 1배"
        elif score <= 7:
            return "보통", "risk-medium", "#ffc107", "기준 대비 2배"
        else:
            return "높음", "risk-high", "#dc3545", "기준 대비 3배 이상"

def create_comparison_chart(current_score, prev_score, title, disease_type, max_score=50):
    """비교 막대그래프 생성"""
    
    # 위험도 정보 가져오기
    risk_level, risk_class, color, risk_text = get_risk_info(current_score, disease_type)
    prev_risk_level, _, prev_color, _ = get_risk_info(prev_score, disease_type)
    
    # 막대그래프 생성
    fig = go.Figure()
    
    # 이전 값 (회색, 투명)
    if prev_score > 0:
        fig.add_trace(go.Bar(
            x=['이전', '현재'],
            y=[prev_score, 0],
            name='이전 값',
            marker_color='rgba(108, 117, 125, 0.5)',
            text=[f'{prev_score}', ''],
            textposition='outside',
            textfont=dict(size=12, color='#6c757d'),
            hovertemplate='이전 값: %{y}<extra></extra>'
        ))
    
    # 현재 값 (컬러)
    fig.add_trace(go.Bar(
        x=['이전', '현재'],
        y=[0, current_score],
        name='현재 값',
        marker_color=color,
        text=['', f'{current_score}'],
        textposition='outside',
        textfont=dict(size=14, color=color, family='Arial Black'),
        hovertemplate='현재 값: %{y}<extra></extra>'
    ))
    
    # 위험도 구간 배경 추가
    if disease_type == "stroke":
        fig.add_hline(y=10, line_dash="dash", line_color="green", opacity=0.5, annotation_text="낮음 (≤10)")
        fig.add_hline(y=22, line_dash="dash", line_color="orange", opacity=0.5, annotation_text="보통 (≤22)")
    elif disease_type == "heart":
        fig.add_hline(y=10, line_dash="dash", line_color="green", opacity=0.5, annotation_text="낮음 (≤10)")
        fig.add_hline(y=20, line_dash="dash", line_color="orange", opacity=0.5, annotation_text="보통 (≤20)")
    else:  # diabetes
        fig.add_hline(y=4, line_dash="dash", line_color="green", opacity=0.5, annotation_text="낮음 (≤4)")
        fig.add_hline(y=7, line_dash="dash", line_color="orange", opacity=0.5, annotation_text="보통 (≤7)")
    
    # 레이아웃 설정
    fig.update_layout(
        title=dict(
            text=f"{title}<br><span style='font-size:14px; color:{color}'>{risk_level} 위험도 ({risk_text})</span>",
            x=0.5,
            font=dict(size=16, color='#495057')
        ),
        xaxis=dict(showgrid=False, showline=False, zeroline=False),
        yaxis=dict(
            title="위험 점수",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            range=[0, max_score],
            dtick=5
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=40, r=40, t=80, b=40),
        showlegend=False,
        bargap=0.4,
        font=dict(family="Arial, sans-serif")
    )
    
    return fig

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
    
    # 막대그래프
    stroke_chart = create_comparison_chart(
        stroke_score, st.session_state.prev_stroke_score, 
        "🧠 뇌졸중", "stroke", 40
    )
    st.plotly_chart(stroke_chart, use_container_width=True, config={'displayModeBar': False})
    
    # 변화 정보
    if not st.session_state.is_first_run:
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
    
    # 막대그래프
    heart_chart = create_comparison_chart(
        heart_score, st.session_state.prev_heart_score, 
        "❤️ 심혈관질환", "heart", 35
    )
    st.plotly_chart(heart_chart, use_container_width=True, config={'displayModeBar': False})
    
    # 변화 정보
    if not st.session_state.is_first_run:
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
    
    # 막대그래프
    diab_chart = create_comparison_chart(
        diab_score, st.session_state.prev_diab_score, 
        "🍬 당뇨병", "diabetes", 15
    )
    st.plotly_chart(diab_chart, use_container_width=True, config={'displayModeBar': False})
    
    # 변화 정보
    if not st.session_state.is_first_run:
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

# 종합 분석 차트
st.markdown("---")
st.markdown("### 📈 종합 위험도 비교")

# 종합 비교 차트
comparison_fig = go.Figure()

# 현재 값들
comparison_fig.add_trace(go.Bar(
    x=['뇌졸중', '심혈관질환', '당뇨병'],
    y=[stroke_score, heart_score, diab_score],
    name='현재 값',
    marker_color=['#dc3545' if stroke_score > 22 else '#ffc107' if stroke_score > 10 else '#28a745',
                  '#dc3545' if heart_score > 20 else '#ffc107' if heart_score > 10 else '#28a745',
                  '#dc3545' if diab_score > 7 else '#ffc107' if diab_score > 4 else '#28a745'],
    text=[stroke_score, heart_score, diab_score],
    textposition='outside',
    textfont=dict(size=14, color='#333')
))

# 이전 값들 (투명)
if not st.session_state.is_first_run:
    comparison_fig.add_trace(go.Bar(
        x=['뇌졸중', '심혈관질환', '당뇨병'],
        y=[st.session_state.prev_stroke_score, st.session_state.prev_heart_score, st.session_state.prev_diab_score],
        name='이전 값',
        marker_color='rgba(108, 117, 125, 0.3)',
        text=[st.session_state.prev_stroke_score, st.session_state.prev_heart_score, st.session_state.prev_diab_score],
        textposition='inside',
        textfont=dict(size=12, color='#6c757d')
    ))

comparison_fig.update_layout(
    title="전체 위험도 비교",
    xaxis_title="질환 유형",
    yaxis_title="위험 점수",
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    barmode='group',
    font=dict(family="Arial, sans-serif")
)

st.plotly_chart(comparison_fig, use_container_width=True)

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
