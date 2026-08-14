import streamlit as st

st.title("나의 척번쨰 웹페이지😑")
st.write("오눌은 기분이 별로다 왜냐 밥을 못먹었기 때문이다😭😭😭😭😭")

import time
import streamlit as st

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 반응형 CSS 스타일 정의
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="⏱️ 인공지능 요리사",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 반응형 디자인, 카드 레이아웃, clamp() 적용 CSS
st.markdown("""
<style>
    /* 전체 배경색 밝고 깔끔하게 설정 */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* 중앙 카드 스타일 */
    .chef-card {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid #E9ECEF;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* 화면 크기에 따라 반응하는 타이머 텍스트 */
    .responsive-timer {
        font-size: clamp(2.5rem, 8vw, 4.5rem);
        font-weight: 800;
        color: #FF6B6B; /* 타이머 포인트 색상 (주홍빛 Red) */
        font-family: monospace;
        letter-spacing: 2px;
        margin: 10px 0;
    }
    
    /* 모바일 맞춤형 버튼 스타일링 */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
        background-color: #4ECDC4; /* 버튼 메인 색상 (Mint) */
        color: white;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    
    div.stButton > button:hover {
        background-color: #3B9A93;
        color: white;
        transform: translateY(-2px);
    }
    
    /* 선택 강조 박스 */
    .recipe-box {
        background-color: #FFF9DB;
        border-left: 5px solid #FCC419;
        padding: 15px;
        border-radius: 8px;
        text-align: left;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. 레시피 및 카운트다운 데이터베이스 (표준 딕셔너리 구조)
# -----------------------------------------------------------------------------
RECIPE_DB = {
    "한식": {
        "초보": {"name": "김치볶음밥", "time": 180, "recipe": "1. 김치와 밥을 준비합니다.\n2. 팬에 기름을 두르고 김치를 볶습니다.\n3. 밥을 넣고 함께 볶은 후 계란후라이를 올립니다."},
        "중수": {"name": "된장찌개", "time": 300, "recipe": "1. 멸치 육수를 끓입니다.\n2. 된장을 풀고 두부와 애호박을 넣습니다.\n3. 파와 고추를 넣고 중불에서 푹 끓입니다."},
        "고수": {"name": "갈비찜", "time": 600, "recipe": "1. 갈비의 핏물을 30분 이상 뺍니다.\n2. 양념장을 만들어 갈비에 재워둡니다.\n3. 야채와 함께 약불에서 양념이 베어들도록 오래 조립니다."}
    },
    "양식": {
        "초보": {"name": "알리오 올리오", "time": 240, "recipe": "1. 면을 소금물에 삶습니다.\n2. 올리브유에 편마늘과 페페론치노를 볶습니다.\n3. 삶은 면과 면수를 넣고 만테카레(유화)합니다."},
        "중수": {"name": "까르보나라", "time": 360, "recipe": "1. 베이컨(베이컨/관찰레)을 바삭하게 볶습니다.\n2. 노른자와 치즈를 섞어 소스를 만듭니다.\n3. 불을 끄고 면과 소스를 빠르게 섞어줍니다."},
        "고수": {"name": "비프 스튜", "time": 720, "recipe": "1. 소고기 겉면을 바삭하게 구워냅니다.\n2. 채소와 토마토 페이스트, 와인을 넣습니다.\n3. 약불에서 1시간 이상 뭉근하게 끓여냅니다."}
    },
    "중식": {
        "초보": {"name": "계란볶음밥", "time": 150, "recipe": "1. 파기름을 먼저 냅니다.\n2. 계란을 스크램블하고 밥을 넣어 강불에 볶습니다.\n3. 굴소스나 간장으로 간을 맞춥니다."},
        "중수": {"name": "마파두부", "time": 300, "recipe": "1. 다진 고기를 두반장에 볶습니다.\n2. 육수를 넣고 깍둑썰기한 두부를 넣습니다.\n3. 전분물로 농도를 맞추고 화조유를 뿌립니다."},
        "고수": {"name": "동파육", "time": 900, "recipe": "1. 통삼겹살을 삶은 뒤 겉면을 구워냅니다.\n2. 간장, 팔각, 노추 등을 넣은 조림물에 조립니다.\n3. 청경채를 데쳐 함께 올려냅니다."}
    }
}

# 인기 요리 빠른 선택 데이터 (음식 이름, 요리 종류, 난이도)
POPULAR_DISHES = [
    ("🔥 인기: 김치볶음밥 (한식/초보)", "한식", "초보"),
    ("🔥 인기: 알리오 올리오 (양식/초보)", "양식", "초보"),
    ("🔥 인기: 마파두부 (중식/중수)", "중식", "중수")
]


# -----------------------------------------------------------------------------
# 3. 세션 상태(Session State) 초기화 (오류 방지 및 버튼 중복 클릭 제어)
# -----------------------------------------------------------------------------
if "category" not in st.session_state:
    st.session_state.category = None  # 한식, 양식, 중식 중 선택된 카테고리
if "level" not in st.session_state:
    st.session_state.level = None        # 초보, 중수, 고수 중 선택된 난이도
if "time_left" not in st.session_state:
    st.session_state.time_left = 0      # 남은 시간(초)
if "total_time" not in st.session_state:
    st.session_state.total_time = 0    # 전체 타이머 시간(초)
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False # 타이머 동작 여부


# -----------------------------------------------------------------------------
# 4. 리셋 및 선택 핸들러 함수
# -----------------------------------------------------------------------------
def reset_all():
    """모든 선택 상태와 타이머를 초기화하는 함수"""
    st.session_state.category = None
    st.session_state.level = None
    st.session_state.time_left = 0
    st.session_state.total_time = 0
    st.session_state.timer_running = False

def select_dish(cat, lvl):
    """요리와 난이도를 한 번에 설정하는 함수 (인기 요리용)"""
    st.session_state.category = cat
    st.session_state.level = lvl
    dish_info = RECIPE_DB[cat][lvl]
    st.session_state.total_time = dish_info["time"]
    st.session_state.time_left = dish_info["time"]
    st.session_state.timer_running = False


# -----------------------------------------------------------------------------
# 5. 메인 UI 화면 구성
# -----------------------------------------------------------------------------
st.markdown("<div class='chef-card'><h1>⏱️ 인공지능 요리사</h1><p>스마트 맞춤 요리 타이머 & 레시피</p></div>", unsafe_allow_html=True)

# [Step 1] 요리 종류 선택
if st.session_state.category is None:
    st.subheader("1. 어떤 종류의 요리를 원하시나요?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍚 한식"):
            st.session_state.category = "한식"
            st.rerun()
    with col2:
        if st.button("🍝 양식"):
            st.session_state.category = "양식"
            st.rerun()
    with col3:
        if st.button("🥢 중식"):
            st.session_state.category = "중식"
            st.rerun()
            
    st.markdown("---")
    st.write("🔥 **사람들이 많이 찾는 인기 메뉴 바로가기**")
    for label, cat, lvl in POPULAR_DISHES:
        if st.button(label):
            select_dish(cat, lvl)
            st.rerun()

# [Step 2] 난이도(급) 선택
elif st.session_state.level is None:
    st.info(f"선택한 요리 종류: **{st.session_state.category}**")
    st.subheader("2. 요리 실력(난이도)을 선택해 주세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌱 초보"):
            select_dish(st.session_state.category, "초보")
            st.rerun()
    with col2:
        if st.button("🍳 중수"):
            select_dish(st.session_state.category, "중수")
            st.rerun()
    with col3:
        if st.button("👨‍🍳 고수"):
            select_dish(st.session_state.category, "고수")
            st.rerun()
            
    if st.button("⬅️ 다시 선택하기"):
        reset_all()
        st.rerun()

# [Step 3] 레시피 제공 및 카운트다운 타이머 실행
else:
    current_recipe = RECIPE_DB[st.session_state.category][st.session_state.level]
    
    st.success(f"**선택한 메뉴:** [{st.session_state.category}] {current_recipe['name']} ({st.session_state.level} 단계)")
    
    # 레시피 안내 상자
    with st.expander("📖 맞춤 레시피 보기", expanded=True):
        st.markdown(f"<div class='recipe-box'>{current_recipe['recipe'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # 시간 분/초 계산
    mins, secs = divmod(st.session_state.time_left, 60)
    time_format = f"{mins:02d}:{secs:02d}"
    
    # 타이머 및 진행률 막대 UI 표시 영역
    st.markdown(f"<div class='responsive-timer'>{time_format}</div>", unsafe_allow_html=True)
    
    # 진행률(Progress Bar) 계산 (0.0 ~ 1.0)
    progress_val = st.session_state.time_left / st.session_state.total_time if st.session_state.total_time > 0 else 0
    st.progress(progress_val)
    
    # 제어 버튼 UI
    b_col1, b_col2, b_col3 = st.columns(3)
    
    with b_col1:
        if not st.session_state.timer_running:
            if st.button("▶️ 시작"):
                st.session_state.timer_running = True
                st.rerun()
        else:
            if st.button("⏸️ 일시정지"):
                st.session_state.timer_running = False
                st.rerun()
                
    with b_col2:
        if st.button("🔄 리셋"):
            st.session_state.time_left = st.session_state.total_time
            st.session_state.timer_running = False
            st.rerun()
            
    with b_col3:
        if st.button("🏠 처음으로"):
            reset_all()
            st.rerun()

    # -------------------------------------------------------------------------
    # 6. 루프 기반 카운트다운 제어 (Streamlit 표준 구현 방식)
    # -------------------------------------------------------------------------
    if st.session_state.timer_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()
    elif st.session_state.timer_running and st.session_state.time_left == 0:
        st.session_state.timer_running = False
        st.balloons()
        st.success("🎉 요리 시간이 완료되었습니다! 맛있게 드세요!")
