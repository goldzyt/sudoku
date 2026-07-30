import random
import time
import streamlit as st

# ==========================================
# 1. 페이지 설정 및 사진 스타일 기반 CSS
# ==========================================
st.set_page_config(
    page_title="클래식 스도쿠",
    page_icon="🧩",
    layout="centered"
)

# 첨부된 이미지 스타일을 반영한 CSS (명확한 3x3 굵은 테두리와 정갈한 숫자)
CSS_STYLE = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #F9F9F9;
        color: #111111;
    }

    /* 타이틀 영역 */
    .title-text {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #111111;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        font-size: 1rem;
        color: #666666;
        margin-bottom: 25px;
    }

    /* 상단 정보 및 버튼 */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding: 10px 5px;
        font-weight: 600;
    }

    /* 스도쿠 그리드 레이아웃 */
    div[data-testid="column"] {
        padding: 0px !important;
    }
    
    /* Streamlit Number Input 셀 디자인 */
    div[data-testid="stNumberInput"] {
        margin: 0 !important;
    }
    
    div[data-testid="stNumberInput"] input {
        text-align: center !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        border-radius: 0px !important;
        border: 1px solid #CCCCCC !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        height: 48px !important;
        padding: 0 !important;
    }

    /* 3x3 구역 분리를 위한 굵은 테두리 시각화 */
    /* 3열, 6열 우측 굵은 선 효과를 위한 마진 조정 */
    .border-right-thick input {
        border-right: 3px solid #000000 !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        border-radius: 8px !important;
        border: 1px solid #222222 !important;
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #111111 !important;
        color: #FFFFFF !important;
    }

    /* 이미 주어진 힌트 셀 스타일 */
    .given-cell input {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }
</style>
"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)


# ==========================================
# 2. 백트래킹 스도쿠 알고리즘
# ==========================================
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku(hints_count):
    solution = [[0] * 9 for _ in range(9)]
    solve_sudoku(solution)
    puzzle = [row[:] for row in solution]
    
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    
    for i in range(81 - hints_count):
        r, c = cells[i]
        puzzle[r][c] = 0
        
    return solution, puzzle


# ==========================================
# 3. 세션 상태 관리
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "start"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = ""
if "solution" not in st.session_state:
    st.session_state.solution = []
if "initial_board" not in st.session_state:
    st.session_state.initial_board = []
if "user_board" not in st.session_state:
    st.session_state.user_board = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None


def start_game(diff_label, hints):
    sol, puz = generate_sudoku(hints)
    st.session_state.solution = sol
    st.session_state.initial_board = [r[:] for r in puz]
    st.session_state.user_board = [r[:] for r in puz]
    st.session_state.difficulty = diff_label
    st.session_state.start_time = time.time()
    st.session_state.page = "game"


# ==========================================
# 4. 화면 구현
# ==========================================

# ---------------- 메인/시작 화면 ----------------
if st.session_state.page == "start":
    st.markdown('<div class="title-text">SUDOKU</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">원하는 난이도를 선택하여 퍼즐을 시작하세요</div>', unsafe_allow_html=True)
    
    levels = [
        ("하 (Easy)", 48, "힌트 약 45~50개"),
        ("중 (Medium)", 39, "힌트 약 36~42개"),
        ("상 (Hard)", 33, "힌트 약 30~35개"),
        ("최상 (Very Hard)", 27, "힌트 약 25~29개"),
        ("전문가 (Expert)", 22, "힌트 약 20~24개")
    ]
    
    st.write("---")
    for label, hints, desc in levels:
        c1, c2 = st.columns([1, 2])
        with c1:
            if st.button(f"▶ {label}", key=f"btn_{label}"):
                start_game(label, hints)
                st.rerun() # 최신 Streamlit 재실행 함수
        with c2:
            st.write(f"<div style='padding-top:8px; color:#555;'>{desc}</div>", unsafe_allow_html=True)

# ---------------- 게임 진행 화면 ----------------
elif st.session_state.page == "game":
    # 상단 정보바
    elapsed = int(time.time() - st.session_state.start_time)
    m, s = divmod(elapsed, 60)
    
    col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
    with col_t1:
        st.markdown(f"**난이도:** {st.session_state.difficulty} | **시간:** {m:02d}:{s:02d}")
    with col_t2:
        if st.button("새 게임", use_container_width=True):
            hints_map = {"하 (Easy)": 48, "중 (Medium)": 39, "상 (Hard)": 33, "최상 (Very Hard)": 27, "전문가 (Expert)": 22}
            h = hints_map.get(st.session_state.difficulty, 39)
            start_game(st.session_state.difficulty, h)
            st.rerun()
    with col_t3:
        if st.button("메인으로", use_container_width=True):
            st.session_state.page = "start"
            st.rerun()

    st.write("")

    # 9x9 스도쿠 그리드 (사진과 유사한 굵은 바운더리 선 적용)
    # 3x3 구역 구분을 위해 3행/6행 아래에 구분용 구분선 적용
    for r in range(9):
        cols = st.columns(9)
        for c in range(9):
            val = st.session_state.initial_board[r][c]
            key = f"cell_{r}_{c}"
            
            with cols[c]:
                if val != 0:
                    # 초기 힌트 셀
                    st.number_input(
                        label=f"r{r}c{c}",
                        min_value=1,
                        max_value=9,
                        value=val,
                        key=key,
                        disabled=True,
                        label_visibility="collapsed"
                    )
                else:
                    # 유저 입력 셀
                    u_val = st.session_state.user_board[r][c]
                    input_val = st.number_input(
                        label=f"r{r}c{c}",
                        min_value=0,
                        max_value=9,
                        value=u_val if u_val != 0 else None,
                        key=key,
                        label_visibility="collapsed",
                        placeholder=""
                    )
                    st.session_state.user_board[r][c] = input_val if input_val is not None else 0
        
        # 3행, 6행 뒤에 구분 라인을 주어 3x3 블록 분리 (이미지 스타일 반영)
        if r in [2, 5]:
            st.markdown("<div style='border-bottom: 2px solid #000000; margin: 2px 0 6px 0;'></div>", unsafe_allow_html=True)

    st.write("")

    # 하단 조작 버튼
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("정답 확인", use_container_width=True):
            if st.session_state.user_board == st.session_state.solution:
                st.balloons()
                st.success("🎉 정답입니다! 축하합니다!")
            else:
                st.error("틀린 부분이 있거나 아직 비어있는 칸이 있습니다.")
    with b2:
        if st.button("힌트 보기", use_container_width=True):
            empty_cells = [(r, c) for r in range(9) for c in range(9) if st.session_state.user_board[r][c] == 0]
            if empty_cells:
                hr, hc = random.choice(empty_cells)
                st.session_state.user_board[hr][hc] = st.session_state.solution[hr][hc]
                st.rerun()
            else:
                st.info("빈 칸이 없습니다.")
    with b3:
        if st.button("초기화", use_container_width=True):
            st.session_state.user_board = [r[:] for r in st.session_state.initial_board]
            st.rerun()
