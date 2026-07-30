import random
import time
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 Custom CSS
# ==========================================
st.set_page_config(
    page_title="말랑말랑 스도쿠",
    page_icon="🧩",
    layout="centered"
)

# 감성적인 파스텔톤 스타일링
CSS_STYLE = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        background-color: #FAF7F2;
        color: #5A524C;
    }

    /* 메인 타이틀 감성 스타일ing */
    .main-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 700;
        color: #7B6D61;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.05rem;
        color: #A3968A;
        margin-bottom: 25px;
    }

    /* 카드형 컨테이너 */
    .stCard {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(180, 165, 150, 0.15);
        border: 1px solid #F0EAE1;
    }

    /* 버튼 스타일 override */
    .stButton > button {
        border-radius: 15px !important;
        border: none !important;
        background-color: #E8DFD8 !important;
        color: #5A524C !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
    }

    .stButton > button:hover {
        background-color: #D3C5B9 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.08) !important;
    }

    /* 메인 화면 난이도 버튼 강조 */
    div[data-testid="column"] .stButton > button {
        width: 100%;
        height: 52px;
        font-size: 1.05rem !important;
    }

    /* 스도쿠 그리드 전용 스타일 */
    .sudoku-container {
        display: flex;
        justify-content: center;
        margin: 15px 0;
    }

    /* Streamlit Number Input 커스텀 */
    div[data-testid="stNumberInput"] {
        margin-bottom: 0px;
    }
    div[data-testid="stNumberInput"] input {
        text-align: center;
        font-weight: 700;
        font-size: 1.2rem;
        border-radius: 8px;
        border: 1px solid #E6DFD5;
        background-color: #FFFDF9;
        color: #4A423A;
        height: 42px;
        transition: all 0.2s ease;
    }
    div[data-testid="stNumberInput"] input:focus {
        border-color: #C3B1A1;
        box-shadow: 0 0 0 2px rgba(195, 177, 161, 0.25);
    }

    /* 고정 숫자(원래 힌트) 배경 다르게 */
    .given-cell input {
        background-color: #F2ECE4 !important;
        color: #7A6959 !important;
        font-weight: 800 !important;
    }

    /* 정보 뱃지 */
    .info-badge {
        background-color: #F3EDE6;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #6E6156;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)


# ==========================================
# 2. 스도쿠 생성 및 해결 백트래킹 알고리즘
# ==========================================
def is_valid(board, row, col, num):
    """현재 위치에 숫자를 놓을 수 있는지 검증"""
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
    """완성된 스도쿠 보드 생성 (백트래킹)"""
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


def generate_sudoku_board(hints_count):
    """지정된 힌트 개수만큼 남기고 퍼즐 생성"""
    solution = [[0] * 9 for _ in range(9)]
    solve_sudoku(solution)

    puzzle = [row[:] for row in solution]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    remove_count = 81 - hints_count
    for i in range(remove_count):
        r, c = cells[i]
        puzzle[r][c] = 0

    return solution, puzzle


# ==========================================
# 3. 세션 상태 (Session State) 초기화
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "start"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None
if "solution" not in st.session_state:
    st.session_state.solution = None
if "initial_board" not in st.session_state:
    st.session_state.initial_board = None
if "current_board" not in st.session_state:
    st.session_state.current_board = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None


def start_new_game(diff_name, hints):
    """새로운 난이도로 게임 시작"""
    sol, puz = generate_sudoku_board(hints)
    st.session_state.solution = sol
    st.session_state.initial_board = [row[:] for row in puz]
    st.session_state.current_board = [row[:] for row in puz]
    st.session_state.difficulty = diff_name
    st.session_state.start_time = time.time()
    st.session_state.page = "game"


# ==========================================
# 4. 화면 구현 (Start Screen / Game Screen)
# ==========================================

# ---------------- [1] 초기 화면 ----------------
if st.session_state.page == "start":
    st.markdown('<div class="main-title">🍃 말랑말랑 스도쿠</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">바쁜 일상 속, 차분하게 뇌를 깨우는 부드러운 시간</div>', unsafe_allow_html=True)

    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown("### 🎯 난이도를 선택해 주세요")
    st.caption("편안한 마음으로 즐길 수 있는 난이도를 골라보세요.")
    st.write("")

    difficulties = [
        ("🌱 하 (Easy)", 48, "처음 시작하기 좋은 편안한 난이도 (힌트 ~48개)"),
        ("🌿 중 (Medium)", 39, "적당한 몰입감을 주는 난이도 (힌트 ~39개)"),
        ("🌳 상 (Hard)", 33, "차근차근 논리력을 발휘할 난이도 (힌트 ~33개)"),
        ("❄️ 최상 (Very Hard)", 27, "깊은 집중력이 필요한 난이도 (힌트 ~27개)"),
        ("🔥 전문가 (Expert)", 22, "스도쿠 마니아를 위한 도전 난이도 (힌트 ~22개)"),
    ]

    for label, hints, desc in difficulties:
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button(label, key=f"btn_{hints}"):
                start_new_game(label, hints)
                st.rerun()
        with col2:
            st.write(f"<div style='padding-top: 12px; color: #8A7E74;'>{desc}</div>", unsafe_allow_html=True)
        st.write("")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- [2] 게임 화면 ----------------
elif st.session_state.page == "game":
    # 상단 메뉴바 (난이도, 타이머, 이동 버튼)
    col_head1, col_head2, col_head3 = st.columns([2, 1, 1])

    elapsed_time = int(time.time() - st.session_state.start_time)
    minutes, seconds = divmod(elapsed_time, 60)

    with col_head1:
        st.markdown(f'<span class="info-badge">{st.session_state.difficulty}</span> &nbsp; ⏱️ <b>{minutes:02d}:{seconds:02d}</b>', unsafe_allow_html=True)
    
    with col_head2:
        if st.button("🔄 새 게임"):
            # 동일 난이도로 재시작
            hints_map = {"🌱 하 (Easy)": 48, "🌿 중 (Medium)": 39, "🌳 상 (Hard)": 33, "❄️ 최상 (Very Hard)": 27, "🔥 전문가 (Expert)": 22}
            current_hints = hints_map.get(st.session_state.difficulty, 39)
            start_new_game(st.session_state.difficulty, current_hints)
            st.rerun()

    with col_head3:
        if st.button("🏠 메인으로"):
            st.session_state.page = "start"
            st.rerun()

    st.write("---")

    # 9x9 스도쿠 그리드 출력
    # 3x3 구역 구분을 위해 CSS 간격 및 테두리 시각화
    for row in range(9):
        cols = st.columns(9)
        for col in range(9):
            initial_val = st.session_state.initial_board[row][col]
            key = f"cell_{row}_{col}"

            with cols[col]:
                if initial_val != 0:
                    # 초기에 주어진 숫자는 읽기 전용 형태처럼 표현
                    st.number_input(
                        label=f"r{row}c{col}",
                        min_value=1,
                        max_value=9,
                        value=initial_val,
                        key=key,
                        disabled=True,
                        label_visibility="collapsed"
                    )
                else:
                    # 사용자 입력 셀
                    curr_val = st.session_state.current_board[row][col]
                    val = st.number_input(
                        label=f"r{row}c{col}",
                        min_value=0,
                        max_value=9,
                        value=curr_val if curr_val != 0 else None,
                        key=key,
                        label_visibility="collapsed",
                        placeholder=""
                    )
                    st.session_state.current_board[row][col] = val if val is not None else 0

        # 3행마다 구분선 역할을 할 여백 추가
        if row in [2, 5]:
            st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    st.write("")

    # 하단 조작 버튼 (정답 확인, 힌트, 초기화)
    b_col1, b_col2, b_col3 = st.columns(3)

    with b_col1:
        if st.button("✨ 정답 확인", use_container_width=True):
            if st.session_state.current_board == st.session_state.solution:
                st.balloons()
                st.success(f"🎉 축하합니다! {minutes}분 {seconds}초 만에 완벽하게 해결하셨어요!")
            else:
                st.warning("아직 채워지지 않은 칸이 있거나 틀린 부분이 있어요. 천천히 다시 확인해보세요 🌿")

    with b_col2:
        if st.button("💡 힌트 보기", use_container_width=True):
            # 빈 칸 중 하나를 채워줌
            empty_cells = [(r, c) for r in range(9) for c in range(9) if st.session_state.current_board[r][c] == 0]
            if empty_cells:
                hr, hc = random.choice(empty_cells)
                correct_val = st.session_state.solution[hr][hc]
                st.session_state.current_board[hr][hc] = correct_val
                st.info(f"💡 [{hr+1}행 {hc+1}열] 의 숫자는 **{correct_val}** 입니다.")
                st.rerun()
            else:
                st.info("이미 모든 칸이 채워져 있습니다!")

    with b_col3:
        if st.button("🧹 초기화", use_container_width=True):
            st.session_state.current_board = [row[:] for row in st.session_state.initial_board]
            st.rerun()
