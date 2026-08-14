

import streamlit as st

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 가독성 높은 CSS 디자인
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="⏱️ 인공지능 요리사",
    page_icon="⏱️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 글씨와 버튼이 잘 보이도록 선명한 색상 대비(Dark Gray / Black) 적용
st.markdown("""
<style>
    /* 전체 배경을 깔끔한 연한 회색으로 고정 */
    .stApp {
        background-color: #F3F4F6 !important;
    }
    
    /* 카드 디자인 및 타이틀 텍스트 색상 강제 지정 */
    .chef-card {
        background-color: #FFFFFF;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.08);
        border: 2px solid #E5E7EB;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chef-card h1 {
        color: #111827 !important; /* 진한 검은색으로 고정 */
        font-weight: 800;
        font-size: clamp(2rem, 5vw, 2.8rem);
        margin-bottom: 0.5rem;
    }
    
    .chef-card p {
        color: #4B5563 !important; /* 선명한 짙은 회색 */
        font-size: clamp(1rem, 3vw, 1.2rem);
        font-weight: 600;
    }

    /* 모든 기본 텍스트 및 제목 글꼴 색상 강화 */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #1F2937 !important;
    }

    /* 버튼 스타일링 - 시인성이 뛰어난 오렌지/다크 민트 계열 */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        background-color: #0D9488 !important; /* 선명한 딥 틸(Mint Green) */
        color: #FFFFFF !important; /* 명확한 흰색 글씨 */
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
    }
    
    div.stButton > button:hover {
        background-color: #0F766E !important;
        transform: translateY(-2px);
    }

    /* 레시피 출력 박스 디자인 */
    .recipe-box {
        background-color: #FFFFFF;
        border: 2px solid #F59E0B;
        border-radius: 12px;
        padding: 20px;
        color: #1F2937 !important;
        font-size: 1.1rem;
        line-height: 1.8;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.1);
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. 레시피 데이터베이스 (타이머 시간 제거됨)
# -----------------------------------------------------------------------------
RECIPE_DB = {
    "한식": {
        "초보": {"name": "김치볶음밥", "recipe": "1. 김치와 밥을 준비합니다.\n2. 팬에 식용유를 두르고 잘게 썬 김치를 달달 볶습니다.\n3. 밥을 넣고 양념이 골고루 섞이도록 함께 볶아줍니다.\n4. 기호에 따라 계란후라이나 김가루를 올려 완성합니다."},
        "중수": {"name": "된장찌개", "recipe": "1. 냄비에 멸치 육수를 우려냅니다.\n2. 된장을 1~2스푼 듬뿍 풀어줍니다.\n3. 두부, 애호박, 버섯을 깍둑썰기하여 넣습니다.\n4. 파와 청양고추를 넣고 중불에서 보글보글 끓여냅니다."},
        "고수": {"name": "갈비찜", "recipe": "1. 소갈비/돼지갈비의 핏물을 30분 이상 빼줍니다.\n2. 간장, 마늘, 양파, 설탕 등으로 맛있는 양념장을 만듭니다.\n3. 갈비에 양념을 재운 뒤 무, 당근과 함께 푹 삶습니다.\n4. 국물이 자작해질 때까지 약불에서 은근히 조려줍니다."}
    },
    "양식": {
        "초보": {"name": "알리오 올리오", "recipe": "1. 냄비에 소금을 넣고 파스타 면을 삶습니다.\n2. 프라이팬에 올리브유를 넉넉히 두르고 편마늘을 볶습니다.\n3. 마늘향이 올라오면 페페론치노를 부수어 넣습니다.\n4. 삶은 면과 면수를 살짝 넣어 잘 섞어주면 완성!"},
        "중수": {"name": "까르보나라", "recipe": "1. 베이컨이나 관찰레를 바삭하게 볶아냅니다.\n2. 볼에 계란 노른자와 파마산 치즈, 후추를 섞어 소스를 만듭니다.\n3. 불을 끈 상태에서 면과 베이컨, 치즈 소스를 빠르게 비벼줍니다."},
        "고수": {"name": "비프 스튜", "recipe": "1. 소고기 겉면을 강불에 노릇하게 구워냅니다.\n2. 볶은 채소와 토마토 페이스트, 와인을 넣고 볶습니다.\n3. 육수를 붓고 약불에서 1시간 이상 고기가 부드러워질 때까지 푹 끓입니다."}
    },
    "중식": {
        "초보": {"name": "계란볶음밥", "recipe": "1. 팬에 기름을 둘러 대파를 볶아 파기름을 만듭니다.\n2. 계란을 깨넣고 부드럽게 스크램블을 만듭니다.\n3. 밥을 넣고 강불에 날려가며 볶다가 굴소스로 간을 맞춥니다."},
        "중수": {"name": "마파두부", "recipe": "1. 팬에 다진 돼지고기와 두반장을 함께 볶습니다.\n2. 물과 깍둑썰기한 두부를 넣고 끓여줍니다.\n3. 전분물을 조금씩 넣어가며 농도를 맞추고 화조유를 살짝 뿌립니다."},
        "고수": {"name": "동파육", "recipe": "1. 통삼겹살을 삶은 후 겉면을 바삭하게 구워냅니다.\n2. 간장, 팔각, 굴소스 등을 넣은 양념물에 고기를 넣습니다.\n3. 약불에서 2시간 이상 양념이 쏙 베어들 때까지 부드럽게 조립니다."}
    }
}

# 인기 요리 데이터
POPULAR_DISHES = [
    ("🔥 인기: 김치볶음밥 (한식/초보)", "한식", "초보"),
    ("🔥 인기: 알리오 올리오 (양식/초보)", "양식", "초보"),
    ("🔥 인기: 마파두부 (중식/중수)", "중식", "중수")
]


# -----------------------------------------------------------------------------
# 3. 세션 상태(Session State) 관리
# -----------------------------------------------------------------------------
if "category" not in st.session_state:
    st.session_state.category = None
if "level" not in st.session_state:
    st.session_state.level = None

def reset_all():
    st.session_state.category = None
    st.session_state.level = None

def select_dish(cat, lvl):
    st.session_state.category = cat
    st.session_state.level = lvl


# -----------------------------------------------------------------------------
# 4. 메인 화면 UI
# -----------------------------------------------------------------------------
st.markdown("""
<div class='chef-card'>
    <h1>⏱️ 인공지능 요리사</h1>
    <p>원하는 요리와 난이도를 선택해 맞춤 레시피를 확인하세요!</p>
</div>
""", unsafe_allow_html=True)

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
    st.subheader("🔥 많은 사람들이 찾는 인기 메뉴")
    for label, cat, lvl in POPULAR_DISHES:
        if st.button(label):
            select_dish(cat, lvl)
            st.rerun()

# [Step 2] 난이도 선택
elif st.session_state.level is None:
    st.info(f"선택한 요리: **{st.session_state.category}**")
    st.subheader("2. 요리 난이도(급)를 선택해 주세요.")
    
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
            
    st.write("")
    if st.button("⬅️ 다시 선택하기"):
        reset_all()
        st.rerun()

# [Step 3] 레시피 출력 (타이머 기능 제거)
else:
    current_recipe = RECIPE_DB[st.session_state.category][st.session_state.level]
    
    st.success(f"**선택한 메뉴:** [{st.session_state.category}] **{current_recipe['name']}** ({st.session_state.level} 단계)")
    
    st.subheader("📖 맞춤 레시피")
    # 레시피 내용을 줄바꿈 처리하여 보여줌
    formatted_recipe = current_recipe['recipe'].replace("\n", "<br>")
    st.markdown(f"<div class='recipe-box'>{formatted_recipe}</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("---")
    if st.button("🏠 처음으로 돌아가기"):
        reset_all()
        st.rerun()
