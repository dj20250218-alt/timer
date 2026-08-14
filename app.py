import streamlit as st

st.title("나의 척번쨰 웹페이지😑")
st.write("오눌은 기분이 별로다 왜냐 밥을 못먹었기 때문이다😭😭😭😭😭")
import time
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 Custom CSS
# ==========================================
st.set_page_config(
    page_title="⏱️ 나만의 반응형 타이머",
    page_icon="⏱️",
    layout="centered"
)

# 스마트폰, 태블릿, PC 대응 반응형 CSS (clamp 사용)
st.markdown("""
<style>
    /* 메인 컨테이너 카드 스타일링 */
    .main-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 2rem 1.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
    }
    
    /* 화면 크기에 따라 반응하는 타이머 텍스트 (clamp 사용) */
    .timer-display {
        font-size: clamp(3.5rem, 12vw, 6.5rem);
        font-weight: 800;
        color: #2D3748;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: -2px;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    /* 서브 타이틀 스타일 */
    .timer-subtitle {
        text-align: center;
        color: #718096;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    /* Streamlit 기본 버튼 반응형 최적화 */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        height: 3rem;
        border: none;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Session State (상태 관리) 초기화
# ==========================================
if "status" not in st.session_state:
    st.session_state.status = "IDLE"      # 상태: IDLE(대기), RUNNING(실행중), PAUSED(일시정지), FINISHED(완료)
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0   # 전체 설정 시간 (초)
if "end_time" not in st.session_state:
    st.session_state.end_time = 0.0      # 종료 목표 시각 (monotonic 시간)
if "pause_time" not in st.session_state:
    st.session_state.pause_time = 0.0    # 일시정지 버튼을 누른 시각
if "input_minutes" not in st.session_state:
    st.session_state.input_minutes = 3   # 기본 설정: 3분
if "input_seconds" not in st.session_state:
    st.session_state.input_seconds = 0   # 기본 설정: 0초

# ==========================================
# 3. 타이머 제어 함수 정의
# ==========================================
def start_timer():
    """타이머 시작 함수"""
    total = (st.session_state.input_minutes * 60) + st.session_state.input_seconds
    if total <= 0:
        st.warning("⚠️ 0초보다 큰 시간을 설정해 주세요!")
        return
    
    st.session_state.total_seconds = total
    st.session_state.end_time = time.monotonic() + total
    st.session_state.status = "RUNNING"

def pause_timer():
    """타이머 일시정지 함수"""
    if st.session_state.status == "RUNNING":
        st.session_state.pause_time = time.monotonic()
        st.session_state.status = "PAUSED"

def resume_timer():
    """타이머 재개(계속) 함수"""
    if st.session_state.status == "PAUSED":
        # 일시정지되었던 시간만큼 end_time을 연장하여 정확도 유지
        paused_duration = time.monotonic() - st.session_state.pause_time
        st.session_state.end_time += paused_duration
        st.session_state.status = "RUNNING"

def reset_timer():
    """타이머 초기화 함수"""
    st.session_state.status = "IDLE"
    st.session_state.total_seconds = 0
    st.session_state.end_time = 0.0

def set_quick_time(minutes):
    """빠른 시간 설정 버튼 제어 함수"""
    if st.session_state.status in ["IDLE", "FINISHED"]:
        st.session_state.input_minutes = minutes
        st.session_state.input_seconds = 0

# ==========================================
# 4. 앱 UI 레이아웃 구현
# ==========================================
st.title("⏱️ 나만의 반응형 타이머")
st.write("간편하고 정확한 카운트다운 타이머입니다.")

# --- 빠른 설정 버튼 영역 ---
st.caption("⚡ 빠른 시간 설정")
q_col1, q_col2, q_col3, q_col4 = st.columns(4)
is_disabled = st.session_state.status in ["RUNNING", "PAUSED"]

with q_col1:
    if st.button("1분", disabled=is_disabled):
        set_quick_time(1)
with q_col2:
    if st.button("3분", disabled=is_disabled):
        set_quick_time(3)
with q_col3:
    if st.button("5분", disabled=is_disabled):
        set_quick_time(5)
with q_col4:
    if st.button("10분", disabled=is_disabled):
        set_quick_time(10)

# --- 시간 입력 영역 (실행 중에는 수정 불가) ---
col_m, col_s = st.columns(2)
with col_m:
    st.number_input(
        "분 (Minutes)",
        min_value=0,
        max_value=180,
        key="input_minutes",
        disabled=is_disabled
    )
with col_s:
    st.number_input(
        "초 (Seconds)",
        min_value=0,
        max_value=59,
        key="input_seconds",
        disabled=is_disabled
    )

st.divider()

# ==========================================
# 5. st.fragment를 통한 실시간 타이머 디스플레이
# ==========================================
# 0.5초마다 부분 리프레시를 수행하여 타이머를 실시간 업데이트
@st.fragment(run_every=0.5)
def timer_display_fragment():
    # 현재 남은 시간 계산
    if st.session_state.status == "RUNNING":
        remaining = st.session_state.end_time - time.monotonic()
        if remaining <= 0:
            remaining = 0
            st.session_state.status = "FINISHED"
    elif st.session_state.status == "PAUSED":
        remaining = st.session_state.end_time - st.session_state.pause_time
    elif st.session_state.status == "FINISHED":
        remaining = 0
    else:  # IDLE 상태
        remaining = (st.session_state.input_minutes * 60) + st.session_state.input_seconds

    # 분, 초 계산 및 MM:SS 포맷팅
    rem_int = int(max(0, round(remaining)))
    mins, secs = divmod(rem_int, 60)
    time_str = f"{mins:02d}:{secs:02d}"

    # 진행률(Progress Bar) 계산
    if st.session_state.total_seconds > 0:
        progress = max(0.0, min(1.0, remaining / st.session_state.total_seconds))
    else:
        progress = 1.0

    # 메인 카드 디스플레이
    st.markdown(f"""
    <div class="main-card">
        <div class="timer-subtitle">남은 시간</div>
        <div class="timer-display">{time_str}</div>
    </div>
    """, unsafe_allow_html=True)

    # 진행률 표시 바
    st.progress(progress)

    # 타이머 완료 처리
    if st.session_state.status == "FINISHED":
        st.balloons()
        st.success("🎉 설정한 시간이 완료되었습니다!")

# 디스플레이 프래그먼트 호출
timer_display_fragment()

# ==========================================
# 6. 제어 버튼 영역 (시작, 일시정지, 계속, 초기화)
# ==========================================
b_col1, b_col2 = st.columns(2)

with b_col1:
    if st.session_state.status in ["IDLE", "FINISHED"]:
        st.button("▶️ 시작", on_click=start_timer, type="primary")
    elif st.session_state.status == "RUNNING":
        st.button("⏸️ 일시정지", on_click=pause_timer)
    elif st.session_state.status == "PAUSED":
        st.button("▶️ 계속", on_click=resume_timer, type="primary")

with b_col2:
    st.button("🔄 초기화", on_click=reset_timer)
