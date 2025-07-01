# health_risk_app_pie_chart.py
# 건강 위험도 평가 웹 애플리케이션 (파이차트 버전)

# 필요한 라이브러리들을 가져옵니다
import streamlit as st  # 웹 애플리케이션을 만들기 위한 라이브러리
import pandas as pd     # 데이터 처리를 위한 라이브러리
import numpy as np      # 수치 계산을 위한 라이브러리
import math            # 수학 계산을 위한 라이브러리

# 웹 페이지의 기본 설정을 합니다
st.set_page_config(
    page_title="건강 위험 평가",      # 브라우저 탭에 표시될 제목
    page_icon="💡",                # 브라우저 탭에 표시될 아이콘
    layout="wide",                 # 페이지 레이아웃을 넓게 설정
    initial_sidebar_state="collapsed"  # 사이드바를 접어둔 상태로 시작
)

# CSS 스타일을 정의합니다 (웹페이지의 디자인을 꾸미는 코드)
st.markdown("""

    /* 메인 컨테이너의 여백과 패딩을 설정합니다 */
    .main .block-container {
        padding-top: 2rem;      /* 위 여백 */
        padding-bottom: 2rem;   /* 아래 여백 */
        padding-left: 1rem;     /* 왼쪽 여백 */
        padding-right: 1rem;    /* 오른쪽 여백 */
        max-width: 100%;        /* 최대 너비를 100%로 설정 */
    }
    
    /* 메인 제목의 스타일을 정의합니다 */
    .main-title {
        font-size: 1.8rem;      /* 글자 크기 */
        font-weight: bold;      /* 글자 굵기를 굵게 */
        text-align: center;     /* 텍스트를 가운데 정렬 */
        color: #1f77b4;         /* 글자 색상 (파란색) */
        margin-bottom: 1rem;    /* 아래 여백 */
        animation: fadeIn 1s ease-in;  /* 페이드인 애니메이션 적용 */
    }
    
    /* 차트를 담는 컨테이너의 스타일 */
    .chart-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);  /* 그라데이션 배경 */
        padding: 1.5rem;        /* 내부 여백 */
        border-radius: 15px;    /* 모서리를 둥글게 */
        margin: 1rem 0;         /* 위아래 여백 */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);  /* 그림자 효과 */
        border: 1px solid #e9ecef;  /* 테두리 */
        transition: all 0.3s ease;  /* 모든 변화에 0.3초 전환 효과 */
    }
    
    /* 파이차트 컨테이너의 특별한 스타일 */
    .pie-chart-container {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);  /* 흰색 그라데이션 배경 */
        padding: 2rem;          /* 내부 여백을 크게 */
        border-radius: 20px;    /* 모서리를 더 둥글게 */
        margin: 2rem 0;         /* 위아래 여백을 크게 */
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);  /* 더 진한 그림자 */
        border: 2px solid #e9ecef;  /* 두꺼운 테두리 */
        text-align: center;     /* 텍스트를 가운데 정렬 */
    }
    
    /* 파이차트 제목의 스타일 */
    .pie-title {
        font-size: 1.5rem;      /* 큰 글자 크기 */
        font-weight: bold;      /* 굵은 글자 */
        color: #495057;         /* 회색 글자 */
        margin-bottom: 1.5rem;  /* 아래 여백 */
        text-align: center;     /* 가운데 정렬 */
    }
    
    /* 파이차트 SVG의 스타일 */
    .pie-chart {
        width: 100%;            /* 너비를 100%로 */
        max-width: 400px;       /* 최대 너비 400px */
        height: 400px;          /* 높이 400px */
        margin: 0 auto;         /* 가운데 정렬 */
        display: block;         /* 블록 요소로 표시 */
    }
    
    /* 범례(legend)의 스타일 */
    .legend {
        display: flex;          /* 가로로 배치 */
        justify-content: center; /* 가운데 정렬 */
        flex-wrap: wrap;        /* 줄바꿈 허용 */
        gap: 1rem;              /* 항목 간 간격 */
        margin-top: 1.5rem;     /* 위 여백 */
    }
    
    /* 개별 범례 항목의 스타일 */
    .legend-item {
        display: flex;          /* 가로로 배치 */
        align-items: center;    /* 세로 가운데 정렬 */
        gap: 0.5rem;            /* 내부 간격 */
        padding: 0.5rem 1rem;   /* 내부 여백 */
        border-radius: 20px;    /* 둥근 모서리 */
        background: rgba(255,255,255,0.8);  /* 반투명 흰색 배경 */
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);  /* 그림자 */
        font-weight: bold;      /* 굵은 글자 */
    }
    
    /* 범례 색상 표시 원의 스타일 */
    .legend-color {
        width: 20px;            /* 너비 20px */
        height: 20px;           /* 높이 20px */
        border-radius: 50%;     /* 원형으로 만들기 */
    }
    
    /* 점수를 표시하는 원형 박스의 스타일 */
    .score-display {
        background: #fff;       /* 흰색 배경 */
        border: 3px solid #007bff;  /* 파란색 테두리 */
        border-radius: 50%;     /* 완전한 원형으로 만들기 */
        width: 80px;            /* 너비 */
        height: 80px;           /* 높이 */
        display: flex;          /* 플렉스 레이아웃 */
        align-items: center;    /* 세로 가운데 정렬 */
        justify-content: center; /* 가로 가운데 정렬 */
        margin: 1rem auto;      /* 가운데 정렬과 위아래 여백 */
        font-size: 1.5rem;      /* 글자 크기 */
        font-weight: bold;      /* 굵은 글자 */
        color: #007bff;         /* 파란색 글자 */
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);  /* 파란색 그림자 */
        transition: all 0.3s ease;  /* 모든 변화에 애니메이션 */
    }
    
    /* 점수가 업데이트될 때의 스타일 */
    .score-display.updated {
        animation: scoreUpdate 1s ease-in-out;  /* 점수 업데이트 애니메이션 */
        transform: scale(1.1);  /* 크기를 10% 크게 */
    }
    
    /* 프로그레스 바(진행률 표시줄)의 컨테이너 스타일 */
    .progress-container {
        background: #e9ecef;    /* 회색 배경 */
        height: 25px;           /* 높이 */
        border-radius: 12px;    /* 둥근 모서리 */
        overflow: hidden;       /* 넘치는 부분 숨김 */
        margin: 0.5rem 0;       /* 위아래 여백 */
        position: relative;     /* 상대적 위치 */
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);  /* 안쪽 그림자 */
    }
    
    /* 프로그레스 바의 실제 진행률을 보여주는 부분 */
    .progress-bar {
        height: 100%;           /* 컨테이너 높이와 동일 */
        border-radius: 12px;    /* 둥근 모서리 */
        transition: width 1s ease-in-out;  /* 너비 변화에 1초 애니메이션 */
        position: relative;     /* 상대적 위치 */
        display: flex;          /* 플렉스 레이아웃 */
        align-items: center;    /* 세로 가운데 정렬 */
        justify-content: center; /* 가로 가운데 정렬 */
        color: white;           /* 흰색 글자 */
        font-weight: bold;      /* 굵은 글자 */
        font-size: 0.9rem;      /* 글자 크기 */
    }
    
    /* 낮은 위험도 프로그레스 바 (초록색) */
    .progress-low { 
        background: linear-gradient(90deg, #28a745, #20c997);  /* 초록색 그라데이션 */
    }
    
    /* 보통 위험도 프로그레스 바 (노란색) */
    .progress-medium { 
        background: linear-gradient(90deg, #ffc107, #fd7e14);  /* 노란색 그라데이션 */
    }
    
    /* 높은 위험도 프로그레스 바 (빨간색) */
    .progress-high { 
        background: linear-gradient(90deg, #dc3545, #e74c3c);  /* 빨간색 그라데이션 */
    }
    
    /* 위험도 요약 박스의 기본 스타일 */
    .risk-summary {
        text-align: center;     /* 텍스트 가운데 정렬 */
        padding: 0.8rem;        /* 내부 여백 */
        border-radius: 8px;     /* 모서리를 둥글게 */
        margin-top: 0.5rem;     /* 위 여백 */
        font-weight: bold;      /* 굵은 글자 */
        font-size: 1.1rem;      /* 글자 크기 */
    }
    
    /* 낮은 위험도일 때의 스타일 (초록색 계열) */
    .risk-low { 
        background: linear-gradient(135deg, #d4edda, #c3e6cb);  /* 초록색 그라데이션 */
        color: #155724;         /* 진한 초록색 글자 */
        border: 2px solid #b1dfbb;  /* 초록색 테두리 */
    }
    
    /* 보통 위험도일 때의 스타일 (노란색 계열) */
    .risk-medium { 
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);  /* 노란색 그라데이션 */
        color: #856404;         /* 진한 노란색 글자 */
        border: 2px solid #f1c40f;  /* 노란색 테두리 */
    }
    
    /* 높은 위험도일 때의 스타일 (빨간색 계열) */
    .risk-high { 
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);  /* 빨간색 그라데이션 */
        color: #721c24;         /* 진한 빨간색 글자 */
        border: 2px solid #e74c3c;  /* 빨간색 테두리 */
    }
    
    /* 값 비교 박스의 스타일 */
    .value-comparison {
        display: flex;          /* 가로로 배치 */
        justify-content: space-between;  /* 양끝으로 정렬 */
        align-items: center;    /* 세로 가운데 정렬 */
        background: #f8f9fa;    /* 배경색 */
        padding: 0.8rem;        /* 내부 여백 */
        border-radius: 8px;     /* 모서리를 둥글게 */
        margin: 1rem 0;         /* 위아래 여백 */
        font-size: 0.9rem;      /* 글자 크기 */
    }
    
    /* 이전 값 텍스트의 스타일 (취소선 적용) */
    .prev-value {
        color: #6c757d;         /* 회색 글자 */
        text-decoration: line-through;  /* 취소선 */
    }
    
    /* 현재 값 텍스트의 스타일 */
    .current-value {
        color: #007bff;         /* 파란색 글자 */
        font-weight: bold;      /* 굵은 글자 */
    }
    
    /* 변화 지시자(↑, ↓, =)의 기본 스타일 */
    .change-indicator {
        padding: 0.2rem 0.5rem; /* 내부 여백 */
        border-radius: 12px;    /* 둥근 모서리 */
        font-size: 0.8rem;      /* 작은 글자 */
        font-weight: bold;      /* 굵은 글자 */
    }
    
    /* 값이 증가했을 때의 스타일 (빨간색) */
    .change-up {
        background: #dc3545;    /* 빨간색 배경 */
        color: white;           /* 흰색 글자 */
    }
    
    /* 값이 감소했을 때의 스타일 (초록색) */
    .change-down {
        background: #28a745;    /* 초록색 배경 */
        color: white;           /* 흰색 글자 */
    }
    
    /* 값이 동일할 때의 스타일 (회색) */
    .change-same {
        background: #6c757d;    /* 회색 배경 */
        color: white;           /* 흰색 글자 */
    }
    
    /* 비교 막대그래프를 담는 컨테이너 */
    .comparison-bars {
        display: flex;          /* 가로로 배치 */
        align-items: end;       /* 아래쪽 정렬 */
        justify-content: center; /* 가운데 정렬 */
        gap: 20px;              /* 막대 사이 간격 */
        margin: 1rem 0;         /* 위아래 여백 */
        height: 200px;          /* 컨테이너 높이 */
    }
    
    /* 개별 막대의 스타일 */
    .bar {
        width: 60px;            /* 막대 너비 */
        background: linear-gradient(to top, #007bff, #0056b3);  /* 파란색 그라데이션 */
        border-radius: 4px 4px 0 0;  /* 위쪽 모서리만 둥글게 */
        position: relative;     /* 상대적 위치 */
        transition: all 0.8s ease;  /* 모든 변화에 애니메이션 */
        display: flex;          /* 플렉스 레이아웃 */
        align-items: end;       /* 아래쪽 정렬 */
        justify-content: center; /* 가운데 정렬 */
        color: white;           /* 흰색 글자 */
        font-weight: bold;      /* 굵은 글자 */
        padding-bottom: 8px;    /* 아래 패딩 */
    }
    
    /* 이전 값 막대의 스타일 (회색, 투명) */
    .bar.prev {
        background: linear-gradient(to top, #6c757d, #495057);  /* 회색 그라데이션 */
        opacity: 0.5;           /* 50% 투명도 */
    }
    
    /* 막대 아래 라벨의 스타일 */
    .bar-label {
        position: absolute;     /* 절대 위치 */
        bottom: -25px;          /* 막대 아래 25px */
        text-align: center;     /* 가운데 정렬 */
        font-size: 0.8rem;      /* 작은 글자 */
        color: #495057;         /* 회색 글자 */
        font-weight: bold;      /* 굵은 글자 */
    }
    
    /* 페이드인 애니메이션 정의 */
    @keyframes fadeIn {
        from { 
            opacity: 0;         /* 투명한 상태에서 시작 */
            transform: translateY(20px);  /* 아래에서 시작 */
        }
        to { 
            opacity: 1;         /* 완전히 보이는 상태로 */
            transform: translateY(0);     /* 원래 위치로 */
        }
    }
    
    /* 차트 업데이트 애니메이션 정의 */
    @keyframes chartUpdate {
        0% { transform: scale(1); }      /* 원래 크기 */
        50% { transform: scale(1.02); }  /* 2% 크게 */
        100% { transform: scale(1); }    /* 다시 원래 크기 */
    }
    
    /* 점수 업데이트 애니메이션 정의 */
    @keyframes scoreUpdate {
        0% { transform: scale(1); }      /* 원래 크기 */
        50% { transform: scale(1.2); }   /* 20% 크게 */
        100% { transform: scale(1.1); }  /* 10% 크게 유지 */
    }
    
    /* 모바일 화면을 위한 반응형 디자인 (화면 너비 768px 이하) */
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }     /* 제목 글자 크기 줄임 */
        .chart-container { padding: 1rem; }    /* 컨테이너 패딩 줄임 */
        .value-comparison { 
            flex-direction: column;  /* 세로로 배치 */
            gap: 0.5rem;            /* 간격 */
        }
        .comparison-bars { height: 150px; }    /* 막대 높이 줄임 */
        .bar { width: 40px; }                  /* 막대 너비 줄임 */
        .score-display { 
            width: 60px;            /* 점수 박스 크기 줄임 */
            height: 60px; 
            font-size: 1.2rem;      /* 글자 크기 줄임 */
        }
        .pie-chart { 
            max-width: 300px;       /* 파이차트 크기 줄임 */
            height: 300px; 
        }
        .legend { 
            flex-direction: column; /* 범례를 세로로 배치 */
            align-items: center; 
        }
    }

""", unsafe_allow_html=True)

# 세션 상태를 초기화합니다 (사용자가 페이지를 새로고침해도 값을 유지하기 위함)
if 'prev_stroke_score' not in st.session_state:
    st.session_state.prev_stroke_score = 0      # 이전 뇌졸중 점수
if 'prev_heart_score' not in st.session_state:
    st.session_state.prev_heart_score = 0       # 이전 심혈관질환 점수
if 'prev_diab_score' not in st.session_state:
    st.session_state.prev_diab_score = 0        # 이전 당뇨병 점수
if 'is_first_run' not in st.session_state:
    st.session_state.is_first_run = True        # 첫 실행 여부

# 메인 제목을 HTML로 표시합니다
st.markdown('💡 건강 위험 평가 시스템', unsafe_allow_html=True)
st.markdown("**입력값을 바탕으로 각 질환의 발병 위험도를 실시간으로 계산하고 파이차트로 시각화합니다.**")

# 기본 정보 입력 섹션 (접었다 펼 수 있는 형태)
with st.expander("📋 기본 정보 입력", expanded=True):
    # 2개의 컬럼으로 나누어 입력 필드를 배치합니다
    col1, col2 = st.columns(2)
    
    # 첫 번째 컬럼의 입력 필드들
    with col1:
        # 나이 슬라이더 (20세부터 80세까지, 기본값 45세)
        age = st.slider("나이", 20, 80, 45, help="현재 나이를 선택하세요")
        # 성별 선택 박스
        sex = st.selectbox("성별", ["남성", "여성"])
        # 흡연 상태 선택 박스
        smoking = st.selectbox("흡연 상태", ["비흡연자", "남성 흡연자", "여성 흡연자"])
        # BMI 슬라이더 (15.0부터 40.0까지, 0.5 단위로 조절)
        bmi = st.slider("BMI", 15.0, 40.0, 22.0, step=0.5, help="체질량지수")
    
    # 두 번째 컬럼의 입력 필드들
    with col2:
        # 수축기 혈압 슬라이더
        systolic_bp = st.slider("수축기 혈압", 90, 200, 120, help="mmHg")
        # 이완기 혈압 슬라이더
        diastolic_bp = st.slider("이완기 혈압", 60, 120, 80, help="mmHg")
        # 총 콜레스테롤 슬라이더
        cholesterol = st.slider("총 콜레스테롤", 100, 300, 180, help="mg/dL")
        # HDL 콜레스테롤 슬라이더
        hdl = st.slider("HDL 콜레스테롤", 20, 100, 50, help="mg/dL")

# 건강 상태 및 생활습관 입력 섹션
with st.expander("🏥 건강 상태 및 생활습관"):
    col1, col2 = st.columns(2)
    
    # 첫 번째 컬럼의 체크박스들
    with col1:
        bp_med = st.checkbox("혈압약 복용 중")        # 혈압약 복용 여부
        diabetes = st.checkbox("당뇨병 진단받음")     # 당뇨병 진단 여부
        bp_history = st.checkbox("혈압 140/90 이상 경험")  # 고혈압 경험
        family_diabetes = st.checkbox("가족 중 당뇨병")      # 가족력
    
    # 두 번째 컬럼의 입력 필드들
    with col2:
        waist = st.slider("허리둘레 (cm)", 60, 130, 85)     # 허리둘레
        alcohol = st.selectbox("음주량 (하루 평균)", ["1잔 미만", "1~4.9잔", "5잔 이상"])  # 음주량

# 뇌졸중 위험 점수를 계산하는 함수
def calc_stroke_score():
    """
    뇌졸중 위험 점수를 계산합니다.
    여러 위험 요인들을 점수화하여 합산합니다.
    """
    score = 0  # 점수를 0부터 시작
    
    # 나이에 따른 점수 추가
    if 50 <= age < 55: 
        score += 6      # 50-54세: 6점
    elif 55 <= age < 60: 
        score += 12     # 55-59세: 12점
    elif 60 <= age: 
        score += 16     # 60세 이상: 16점
    
    # 성별에 따른 점수 (남성이 위험도가 높음)
    score += 6 if sex == "남성" else 0
    
    # 흡연에 따른 점수
    if smoking == "남성 흡연자": 
        score += 4      # 남성 흡연자: 4점
    elif smoking == "여성 흡연자": 
        score += 8      # 여성 흡연자: 8점 (더 위험)
    
    # BMI(체질량지수)에 따른 점수
    if bmi >= 30: 
        score += 3      # 비만(30 이상): 3점
    elif bmi >= 25: 
        score += 2      # 과체중(25 이상): 2점
    
    # 혈압에 따른 점수 (약물 복용 중이거나 혈압이 높으면)
    if bp_med or systolic_bp >= 140 or diastolic_bp >= 90: 
        score += 11     # 고혈압: 11점
    
    # 당뇨병이 있으면 점수 추가
    if diabetes: 
        score += 7      # 당뇨병: 7점
    
    return score        # 계산된 총 점수를 반환

# 심혈관질환 위험 점수를 계산하는 함수
def calc_heart_score():
    """
    심혈관질환 위험 점수를 계산합니다.
    나이, 콜레스테롤, 흡연, HDL, 혈압 등을 고려합니다.
    """
    score = 0  # 점수를 0부터 시작
    
    # 나이에 따른 점수 (나이가 많을수록 위험도 증가)
    if 45 <= age < 50: 
        score += 3      # 45-49세: 3점
    elif 50 <= age < 55: 
        score += 6      # 50-54세: 6점
    elif 55 <= age < 60: 
        score += 8      # 55-59세: 8점
    elif 60 <= age < 65: 
        score += 10     # 60-64세: 10점
    elif 65 <= age: 
        score += 12     # 65세 이상: 12점
    
    # 총 콜레스테롤 수치에 따른 점수
    if cholesterol >= 280: 
        score += 10     # 280 이상: 10점
    elif cholesterol >= 240: 
        score += 8      # 240-279: 8점
    elif cholesterol >= 200: 
        score += 6      # 200-239: 6점
    elif cholesterol >= 160: 
        score += 3      # 160-199: 3점
    
    # 흡연에 따른 점수
    if smoking != "비흡연자": 
        score += 4      # 흡연자: 4점
    
    # HDL 콜레스테롤(좋은 콜레스테롤)이 낮으면 점수 추가
    if hdl < 40: 
        score += 2      # 40 미만: 2점
    elif hdl < 50: 
        score += 1      # 40-49: 1점
    
    # 수축기 혈압에 따른 점수
    if systolic_bp >= 160: 
        score += 4      # 160 이상: 4점
    elif systolic_bp >= 140: 
        score += 3      # 140-159: 3점
    elif systolic_bp >= 130: 
        score += 2      # 130-139: 2점
    elif systolic_bp >= 120: 
        score += 1      # 120-129: 1점
    
    return score        # 계산된 총 점수를 반환

# 당뇨병 위험 점수를 계산하는 함수
def calc_diabetes_score():
    """
    당뇨병 위험 점수를 계산합니다.
    나이, 가족력, 혈압 이력, 허리둘레, 생활습관 등을 고려합니다.
    """
    score = 0  # 점수를 0부터 시작
    
    # 나이에 따른 점수 (45세 이상부터 위험도 증가)
    if age >= 45: 
        score += 3      # 45세 이상: 3점
    
    # 가족력에 따른 점수
    if family_diabetes: 
        score += 1      # 가족 중 당뇨병: 1점
    
    # 혈압 이력에 따른 점수
    if bp_history: 
        score += 1      # 고혈압 경험: 1점
    
    # 허리둘레에 따른 점수 (성별로 기준이 다름)
    if (sex == "남성" and waist >= 90) or (sex == "여성" and waist >= 84): 
        score += 3      # 복부비만(남성 90cm, 여성 84cm 이상): 3점
    elif (sex == "남성" and waist >= 84) or (sex == "여성" and waist >= 77): 
        score += 2      # 복부비만 전단계: 2점
    
    # 흡연에 따른 점수
    if smoking != "비흡연자": 
        score += 1      # 흡연자: 1점
    
    # 음주량에 따른 점수
    if alcohol == "1~4.9잔": 
        score += 1      # 적당한 음주: 1점
    elif alcohol == "5잔 이상": 
        score += 2      # 과도한 음주: 2점
    
    return score        # 계산된 총 점수를 반환

# 위험도 정보를 가져오는 함수
def get_risk_info(score, disease_type):
    """
    점수에 따른 위험도 정보를 반환합니다.
    각 질환별로 다른 기준을 적용합니다.
    """
    if disease_type == "stroke":        # 뇌졸중의 경우
        if score <= 10:
            return "낮음", "risk-low", "progress-low", "1% 미만", 25
        elif score <= 22:
            return "보통", "risk-medium", "progress-medium", "1-3%", 40
        else:
            return "높음", "risk-high", "progress-high", "4% 이상", 40
    elif disease_type == "heart":       # 심혈관질환의 경우
        risk_percent = min(30, score * 2)  # 최대 30%로 제한
        if risk_percent < 10:
            return "낮음", "risk-low", "progress-low", f"{risk_percent}%", 35
        elif risk_percent < 20:
            return "보통", "risk-medium", "progress-medium", f"{risk_percent}%", 35
        else:
            return "높음", "risk-high", "progress-high", f"{risk_percent}%", 35
    else:  # 당뇨병의 경우
        if score <= 4:
            return "낮음", "risk-low", "progress-low", "기준 대비 1배", 15
        elif score <= 7:
            return "보통", "risk-medium", "progress-medium", "기준 대비 2배", 15
        else:
            return "높음", "risk-high", "progress-high", "기준 대비 3배 이상", 15

# 비교 막대그래프 HTML을 생성하는 함수
def create_comparison_bars(current_score, prev_score, max_score):
    """
    현재 점수와 이전 점수를 비교하는 막대그래프를 HTML로 생성합니다.
    """
    # 막대의 높이를 계산합니다 (최대 180px)
    current_height = min(180, (current_score / max_score) * 180)
    prev_height = min(180, (prev_score / max_score) * 180) if prev_score > 0 else 0
    
    # HTML 문자열을 반환합니다
    return f"""
    
        
            이전{prev_score}
            {prev_score if prev_score > 0 else ''}
        
        
            현재{current_score}
            {current_score}
        
    
    """

# 변화 지시자를 생성하는 함수
def create_change_indicator(current, prev):
    """
    현재값과 이전값의 변화를 나타내는 지시자를 생성합니다.
    """
    if current > prev:
        return f'↑ +{current-prev}'
    elif current < prev:
        return f'↓ -{prev-current}'
    else:
        return f'= 동일'

# 파이차트 SVG를 생성하는 함수
def create_pie_chart_svg(stroke_score, heart_score, diab_score):
    """
    세 질환의 위험도를 파이차트로 시각화하는 SVG를 생성합니다.
    """
    # 총 점수를 계산합니다
    total = stroke_score + heart_score + diab_score
    
    # 총 점수가 0이면 기본 차트를 표시
    if total == 0:
        return """
            
            
                데이터가 없습니다
            
        """
    
    # 각 질환의 비율을 계산합니다
    stroke_percent = (stroke_score / total) * 100
    heart_percent = (heart_score / total) * 100
    diab_percent = (diab_score / total) * 100
    
    # 각 질환의 각도를 계산합니다 (360도 기준)
    stroke_angle = (stroke_score / total) * 360
    heart_angle = (heart_score / total) * 360
    diab_angle = (diab_score / total) * 360
    
    # SVG 경로를 계산하는 함수
    def get_path(start_angle, end_angle, radius=150, center_x=200, center_y=200):
        """SVG 경로를 계산합니다"""
        start_rad = math.radians(start_angle - 90)  # 12시 방향부터 시작
        end_rad = math.radians(end_angle - 90)
        
        # 시작점과 끝점 계산
        start_x = center_x + radius * math.cos(start_rad)
        start_y = center_y + radius * math.sin(start_rad)
        end_x = center_x + radius * math.cos(end_rad)
        end_y = center_y + radius * math.sin(end_rad)
        
        # 큰 호인지 작은 호인지 판단
        large_arc = "1" if (end_angle - start_angle) > 180 else "0"
        
        # SVG 경로 문자열 생성
        return f"M {center_x} {center_y} L {start_x} {start_y} A {radius} {radius} 0 {large_arc} 1 {end_x} {end_y} Z"
    
    # 각 구간의 시작 각도 계산
    stroke_start = 0
    stroke_end = stroke_angle
    heart_start = stroke_end
    heart_end = heart_start + heart_angle
    diab_start = heart_end
    diab_end = diab_start + diab_angle
    
    # 색상 정의
    colors = {
        'stroke': '#ff6b6b',    # 뇌졸중: 빨간색
        'heart': '#4ecdc4',     # 심혈관: 청록색
        'diabetes': '#45b7d1'   # 당뇨병: 파란색
    }
    
    # SVG 문자열 생성
    svg_content = f"""
    
        
        
        
        
        {f'' if stroke_score > 0 else ''}
        
        
        {f'' if heart_score > 0 else ''}
        
        
        {f'' if diab_score > 0 else ''}
        
        
        
        
        
        
            총 점수
        
        
            {total}
        
        
        
        {f'{stroke_score}' if stroke_score > 0 else ''}
        {f'{heart_score}' if heart_score > 0 else ''}
        {f'{diab_score}' if diab_score > 0 else ''}
    
    """
    
    return svg_content

# 범례 HTML을 생성하는 함수
def create_legend(stroke_score, heart_score, diab_score):
    """
    파이차트의 범례를 HTML로 생성합니다.
    """
    total = stroke_score + heart_score + diab_score
    
    # 각 질환의 비율 계산
    stroke_percent = (stroke_score / total * 100) if total > 0 else 0
    heart_percent = (heart_score / total * 100) if total > 0 else 0
    diab_percent = (diab_score / total * 100) if total > 0 else 0
    
    return f"""
    
        
            
            뇌졸중 {stroke_score}점 ({stroke_percent:.1f}%)
        
        
            
            심혈관질환 {heart_score}점 ({heart_percent:.1f}%)
        
        
            
            당뇨병 {diab_score}점 ({diab_percent:.1f}%)
        
    
    """

# 결과 계산
stroke_score = calc_stroke_score()    # 뇌졸중 점수 계산
heart_score = calc_heart_score()      # 심혈관질환 점수 계산
diab_score = calc_diabetes_score()    # 당뇨병 점수 계산

# 변화 감지 (이전 값과 현재 값 비교)
stroke_changed = stroke_score != st.session_state.prev_stroke_score
heart_changed = heart_score != st.session_state.prev_heart_score
diab_changed = diab_score != st.session_state.prev_diab_score

# 결과 표시 섹션
st.markdown("---")
st.markdown("## 📊 위험도 평가 결과")

# 전체 변화 요약 (값이 변경된 경우에만 표시)
if not st.session_state.is_first_run and (stroke_changed or heart_changed or diab_changed):
    changes = []    # 변화된 항목들을 저장할 리스트
    if stroke_changed:
        changes.append(f"뇌졸중: {st.session_state.prev_stroke_score}→{stroke_score}")
    if heart_changed:
        changes.append(f"심혈관: {st.session_state.prev_heart_score}→{heart_score}")
    if diab_changed:
        changes.append(f"당뇨병: {st.session_state.prev_diab_score}→{diab_score}")
    
    # 변화 정보를 정보 박스로 표시
    st.info(f"🔄 **변화 감지**: {', '.join(changes)}")

# 3개 컬럼으로 개별 위험도 차트 표시
col1, col2, col3 = st.columns(3)

# 첫 번째 컬럼: 뇌졸중 위험도
with col1:
    # 값이 변경되었으면 업데이트 클래스 추가
    container_class = "chart-container updated" if stroke_changed else "chart-container"
    st.markdown(f'', unsafe_allow_html=True)
    
    # 제목 표시
    st.markdown('🧠 뇌졸중 위험도', unsafe_allow_html=True)
    
    # 점수 표시 (원형 박스)
    score_class = "updated" if stroke_changed else ""
    st.markdown(f'{stroke_score}', unsafe_allow_html=True)
    
    # 위험도 정보 가져오기
    risk_level, risk_class, progress_class, risk_text, max_score = get_risk_info(stroke_score, "stroke")
    
    # 프로그레스 바 표시
    progress_width = min(100, (stroke_score / max_score) * 100)
    st.markdown(f"""
    
        
            {stroke_score}/{max_score}
        
    
    """, unsafe_allow_html=True)
    
    # 위험도 요약 박스
    st.markdown(f'{risk_level} 위험도({risk_text})', unsafe_allow_html=True)
    
    # 비교 막대그래프 (첫 실행이 아닌 경우에만 표시)
    if not st.session_state.is_first_run:
        comparison_html = create_comparison_bars(stroke_score, st.session_state.prev_stroke_score, max_score)
        st.markdown(comparison_html, unsafe_allow_html=True)
        
        # 변화 정보 표시
        change_html = f"""
        
            
                이전: {st.session_state.prev_stroke_score}
                현재: {stroke_score}
            
            {create_change_indicator(stroke_score, st.session_state.prev_stroke_score)}
        
        """
        st.markdown(change_html, unsafe_allow_html=True)
    
    st.markdown('', unsafe_allow_html=True)

# 두 번째 컬럼: 심혈관질환 위험도
with col2:
    container_class = "chart-container updated" if heart_changed else "chart-container"
    st.markdown(f'', unsafe_allow_html=True)
    
    st.markdown('❤️ 심혈관질환 위험도', unsafe_allow_html=True)
    
    score_class = "updated" if heart_changed else ""
    st.markdown(f'{heart_score}', unsafe_allow_html=True)
    
    risk_level, risk_class, progress_class, risk_text, max_score = get_risk_info(heart_score, "heart")
    
    progress_width = min(100, (heart_score / max_score) * 100)
    st.markdown(f"""
    
        
            {heart_score}/{max_score}
        
    
    """, unsafe_allow_html=True)
    
    st.markdown(f'{risk_level} 위험도({risk_text})', unsafe_allow_html=True)
    
    if not st.session_state.is_first_run:
        comparison_html = create_comparison_bars(heart_score, st.session_state.prev_heart_score, max_score)
        st.markdown(comparison_html, unsafe_allow_html=True)
        
        change_html = f"""
        
            
                이전: {st.session_state.prev_heart_score}
                현재: {heart_score}
            
            {create_change_indicator(heart_score, st.session_state.prev_heart_score)}
        
        """
        st.markdown(change_html, unsafe_allow_html=True)
    
    st.markdown('', unsafe_allow_html=True)

# 세 번째 컬럼: 당뇨병 위험도
with col3:
    container_class = "chart-container updated" if diab_changed else "chart-container"
    st.markdown(f'', unsafe_allow_html=True)
    
    st.markdown('🍬 당뇨병 위험도', unsafe_allow_html=True)
    
    score_class = "updated" if diab_changed else ""
    st.markdown(f'{diab_score}', unsafe_allow_html=True)
    
    risk_level, risk_class, progress_class, risk_text, max_score = get_risk_info(diab_score, "diabetes")
    
    progress_width = min(100, (diab_score / max_score) * 100)
    st.markdown(f"""
    
        
            {diab_score}/{max_score}
        
    
    """, unsafe_allow_html=True)
    
    st.markdown(f'{risk_level} 위험도({risk_text})', unsafe_allow_html=True)
    
    if not st.session_state.is_first_run:
        comparison_html = create_comparison_bars(diab_score, st.session_state.prev_diab_score, max_score)
        st.markdown(comparison_html, unsafe_allow_html=True)
        
        change_html = f"""
        
            
                이전: {st.session_state.prev_diab_score}
                현재: {diab_score}
            
            {create_change_indicator(diab_score, st.session_state.prev_diab_score)}
        
        """
        st.markdown(change_html, unsafe_allow_html=True)
    
    st.markdown('', unsafe_allow_html=True)

# 종합 분석 섹션 (파이차트로 표시)
st.markdown("---")
st.markdown("### 📈 종합 위험도 분석")

# 파이차트 컨테이너
st.markdown('', unsafe_allow_html=True)
st.markdown('🥧 질환별 위험도 비율', unsafe_allow_html=True)

# 파이차트 SVG 생성 및 표시
pie_chart_svg = create_pie_chart_svg(stroke_score, heart_score, diab_score)
st.markdown(pie_chart_svg, unsafe_allow_html=True)

# 범례 표시
legend_html = create_legend(stroke_score, heart_score, diab_score)
st.markdown(legend_html, unsafe_allow_html=True)

st.markdown('', unsafe_allow_html=True)

# 종합 위험도 해석
total_score = stroke_score + heart_score + diab_score
if total_score > 0:
    # 가장 높은 위험도 질환 찾기
    max_score = max(stroke_score, heart_score, diab_score)
    if max_score == stroke_score:
        primary_risk = "뇌졸중"
        primary_icon = "🧠"
    elif max_score == heart_score:
        primary_risk = "심혈관질환"
        primary_icon = "❤️"
    else:
        primary_risk = "당뇨병"
        primary_icon = "🍬"
    
    # 종합 위험도 분석 표시
    if total_score <= 15:
        summary_color = "#28a745"
        summary_text = "전반적으로 양호한 건강 상태입니다."
        summary_icon = "😊"
    elif total_score <= 30:
        summary_color = "#ffc107"
        summary_text = "일부 위험 요인이 있어 주의가 필요합니다."
        summary_icon = "😐"
    else:
        summary_color = "#dc3545"
        summary_text = "적극적인 건강 관리가 필요합니다."
        summary_icon = "😰"
    
    st.markdown(f"""
    
        
            {summary_icon} 종합 건강 위험도 평가
        
        
            총 위험 점수: {total_score}점
        
        
            {summary_text}
        
        
            주요 위험 요인: {primary_icon} {primary_risk} ({max_score}점)
        
    
    """, unsafe_allow_html=True)

# 이전 값들을 현재 값으로 업데이트 (다음 비교를 위해)
st.session_state.prev_stroke_score = stroke_score
st.session_state.prev_heart_score = heart_score
st.session_state.prev_diab_score = diab_score
st.session_state.is_first_run = False

# 건강 관리 권장사항 섹션
st.markdown("---")
with st.expander("💡 건강 관리 권장사항"):
    st.markdown("""
    ### 📋 일반적인 건강 관리 수칙
    
    #### 🏃‍♂️ 운동 관리
    - **규칙적인 운동**: 주 3회 이상, 30분 이상의 유산소 운동
    - **근력 운동**: 주 2회 이상의 근력 강화 운동
    - **일상 활동**: 계단 이용, 도보 통근 등으로 활동량 증가
    
    #### 🚭 금연 및 금주
    - **금연**: 흡연 시 모든 질환의 위험도가 크게 증가
    - **절주**: 남성 하루 2잔, 여성 하루 1잔 이하로 제한
    - **금연 클리닉**: 전문적인 금연 상담 및 치료 프로그램 이용
    
    #### ⚖️ 체중 관리
    - **적정 체중 유지**: BMI 18.5-24.9 범위 유지
    - **허리둘레 관리**: 남성 90cm, 여성 85cm 미만 유지
    - **균형 잡힌 식단**: 나트륨, 당분, 포화지방 섭취 제한
    
    #### 🩺 정기 검진
    - **혈압 측정**: 매년 1회 이상 정기 측정
    - **콜레스테롤 검사**: 연 1회 이상 혈액 검사
    - **당뇨병 검사**: 공복혈당 및 당화혈색소 검사
    - **종합 건강검진**: 2년마다 국가건강검진 수검
    
    #### ⚠️ 주의사항
    - **개인차 고려**: 개인의 건강 상태에 따라 관리 방법이 달라질 수 있음
    - **전문의 상담**: 정확한 진단과 치료는 반드시 전문의와 상담
    - **지속적 관리**: 일시적인 관리보다는 지속적인 생활습관 개선이 중요
    - **응급 상황**: 가슴 통증, 심한 두통, 호흡곤란 등의 증상 시 즉시 응급실 방문
    """)

# 추가 정보 섹션
st.markdown("---")
with st.expander("ℹ️ 위험도 계산 기준"):
    st.markdown("""
    ### 🧠 뇌졸중 위험도 계산 기준
    - **나이**: 50세 이상부터 점수 부여 (50-54세: 6점, 55-59세: 12점, 60세 이상: 16점)
    - **성별**: 남성 6점 추가
    - **흡연**: 남성 흡연자 4점, 여성 흡연자 8점
    - **BMI**: 25-29.9는 2점, 30 이상은 3점
    - **혈압**: 고혈압(140/90 이상) 또는 혈압약 복용 시 11점
    - **당뇨병**: 진단 시 7점 추가
    
    ### ❤️ 심혈관질환 위험도 계산 기준
    - **나이**: 45세부터 점수 부여 (45-49세: 3점, 50-54세: 6점, 55-59세: 8점, 60-64세: 10점, 65세 이상: 12점)
    - **총 콜레스테롤**: 160-199: 3점, 200-239: 6점, 240-279: 8점, 280 이상: 10점
    - **흡연**: 흡연자 4점 추가
    - **HDL 콜레스테롤**: 40 미만: 2점, 40-49: 1점
    - **수축기 혈압**: 120-129: 1점, 130-139: 2점, 140-159: 3점, 160 이상: 4점
    
    ### 🍬 당뇨병 위험도 계산 기준
    - **나이**: 45세 이상 3점
    - **가족력**: 당뇨병 가족력 1점
    - **혈압 이력**: 고혈압 경험 1점
    - **허리둘레**: 남성 84-89cm/여성 77-83cm는 2점, 남성 90cm 이상/여성 84cm 이상은 3점
    - **흡연**: 흡연자 1점
    - **음주**: 적당한 음주(1-4.9잔) 1점, 과도한 음주(5잔 이상) 2점
    
    ### 📊 위험도 분류 기준
    - **뇌졸중**: 10점 이하(낮음), 11-22점(보통), 23점 이상(높음)
    - **심혈관질환**: 점수 × 2 = 위험률(%), 10% 미만(낮음), 10-19%(보통), 20% 이상(높음)
    - **당뇨병**: 4점 이하(낮음), 5-7점(보통), 8점 이상(높음)
    """)

# 푸터
st.markdown("---")
st.markdown(
    """
    
        📋 건강 위험도 평가 시스템
        본 시스템은 건강 위험도 평가를 위한 참고 도구입니다.
        정확한 건강 상태 진단과 치료는 의료 전문가와 상담하시기 바랍니다.
        
            ⚠️ 응급 상황 시 즉시 119에 신고하거나 가까운 응급실로 방문하세요.
        
    
    """, 
    unsafe_allow_html=True
)

# 프로그램 종료 주석
"""
이 프로그램은 사용자가 입력한 건강 정보를 바탕으로
뇌졸중, 심혈관질환, 당뇨병의 위험도를 계산하고
시각적으로 표현하는 웹 애플리케이션입니다.

주요 특징:
1. 실시간 위험도 계산 및 업데이트
2. 개별 질환별 막대그래프 표시
3. 종합 위험도 파이차트 시각화
4. 이전값과 현재값 비교 기능
5. 모바일 최적화된 반응형 디자인

사용 방법:
1. 기본 정보 입력 (나이, 성별, 흡연 상태, BMI, 혈압, 콜레스테롤)
2. 건강 상태 및 생활습관 정보 입력
3. 실시간으로 계산되는 위험도 확인
4. 파이차트로 종합 위험도 분석
5. 건강 관리 권장사항 참고

주의사항:
- 이 도구는 참고용이며 의학적 진단을 대체하지 않습니다
- 정확한 건강 상태는 전문의와 상담하세요
- 응급 상황 시 즉시 응급실로 방문하세요
"""
