import streamlit as st
import numpy as np
from collections import defaultdict
import random
import time

# --- 스도쿠 생성 및 해결 알고리즘 ---
def create_sudoku(num_hints=30):
    """
    고유한 해를 가지는 스도쿠 퍼즐 생성
    """
    grid = [[0] * 9 for _ in range(9)]
    fill_grid(grid)  # 완성된 스도쿠 그리드 생성
    puzzle = [[cell for cell in row] for row in grid]
    remove_hints(puzzle, 81 - num_hints)  # 힌트 제외하고 채워진 숫자 제거
    return puzzle

def fill_grid(grid):
    """
    백트래킹을 이용하여 스도쿠 그리드 채우기
    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if fill_grid(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def is_valid(grid, row, col, num):
    """
    해당 위치에 숫자가 유효한지 확인
    """
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def remove_hints(grid, num_remove):
    """
    힌트 제외하고 채워진 숫자 제거
    """
    while num_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            num_remove -= 1

def solve_sudoku(grid):
    """
    스도쿠 퍼즐 해결 (정답 확인용)
    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

# --- Streamlit 앱 ---
def main():
    st.set_page_config(page_title="감성 스도쿠", layout="centered")

    # 세션 상태 초기화
    if 'current_screen' not in st.session_state:
        st.session_state['current_screen'] = 'start'
    if 'grid' not in st.session_state:
        st.session_state['grid'] = None
    if 'difficulty' not in st.session_state:
        st.session_state['difficulty'] = None
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = None
    if 'elapsed_time' not in st.session_state:
        st.session_state['elapsed_time'] = 0
    if 'user_grid' not in st.session_state:
        st.session_state['user_grid'] = None
    if 'correct_grid' not in st.session_state:
        st.session_state['correct_grid'] = None

    # Custom CSS
    st.markdown("""
        <style>
        .title {
            font-size: 3rem;
            color: #ff9a9e;
            text-align: center;
            margin-bottom: 2rem;
            font-family: 'Open Sans', sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .subtitle {
            font-size: 1.5rem;
            color: #fad0c4;
            text-align: center;
            margin-bottom: 1rem;
            font-family: 'Open Sans', sans-serif;
            font-style: italic;
        }
        .difficulty-button {
            background-image: linear-gradient(120deg, #ff9a9e 0%, #fad0c4 100%);
            border: none;
            border-radius: 20px;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 1.2rem;
            margin: 10px;
            cursor: pointer;
            box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .difficulty-button:hover {
            transform: translateY(-2px);
            box-shadow: 4px 4px 8px rgba(0,0,0,0.3);
        }
        .sudoku-grid {
            display: grid;
            grid-template-columns: repeat(9, 1fr);
            grid-gap: 5px;
            margin-top: 2rem;
        }
        .sudoku-cell {
            background-color: white;
            border: 1px solid #ccc;
            text-align: center;
            font-size: 1.5rem;
            padding: 10px;
            color: #333;
            transition: background-color 0.2s;
        }
        .sudoku-cell:hover {
            background-color: #f0f0f0;
        }
        .correct-cell {
            color: #4CAF50;
        }
        .wrong-cell {
            color: #F44336;
        }
        .main-button {
            background-image: linear-gradient(120deg, #ff9a9e 0%, #fad0c4 100%);
            border: none;
            border-radius: 20px;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 1.2rem;
            margin: 10px;
            cursor: pointer;
            box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .main-button:hover {
            transform: translateY(-2px);
            box-shadow: 4px 4px 8px rgba(0,0,0,0.3);
        }
        .timer {
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
            color: #fad0c4;
        }
        </style>
    """, unsafe_allow_html=True)

    # 초기 화면
    if st.session_state['current_screen'] == 'start':
        st.markdown("<h1 class='title'>감성 스도쿠</h1>", unsafe_allow_html=True)
        st.markdown("<h2 class='subtitle'>바쁜 일상 속, 차분하게 스도쿠를 즐겨보세요!</h2>", unsafe_allow_html=True)

        st.markdown("### 난이도를 선택해 주세요")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if st.button("하 (Easy)", key="easy"):
                st.session_state['difficulty'] = "Easy"
                st.session_state['grid'] = create_sudoku(num_hints=48)
                st.session_state['user_grid'] = [row[:] for row in st.session_state['grid']]
                st.session_state['current_screen'] = 'game'
                st.session_state['start_time'] = time.time()
                st.experimental_rerun()
        with col2:
            if st.button("중 (Medium)", key="medium"):
                st.session_state['difficulty'] = "Medium"
                st.session_state['grid'] = create_sudoku(num_hints=39)
                st.session_state['user_grid'] = [row[:] for row in st.session_state['grid']]
                st.session_state['current_screen'] = 'game'
                st.session_state['start_time'] = time.time()
                st.experimental_rerun()
        with col3:
            if st.button("상 (Hard)", key="hard"):
                st.session_state['difficulty'] = "Hard"
                st.session_state['grid'] = create_sudoku(num_hints=33)
                st.session_state['user_grid'] = [row[:] for row in st.session_state['grid']]
                st.session_state['current_screen'] = 'game'
                st.session_state['start_time'] = time.time()
                st.experimental_rerun()
        with col4:
            if st.button("최상 (Very Hard)", key="very_hard"):
                st.session_state['difficulty'] = "Very Hard"
                st.session_state['grid'] = create_sudoku(num_hints=27)
                st.session_state['user_grid'] = [row[:] for row in st.session_state['grid']]
                st.session_state['current_screen'] = 'game'
                st.session_state['start_time'] = time.time()
                st.experimental_rerun()
        with col5:
            if st.button("전문가 (Expert)", key="expert"):
                st.session_state['difficulty'] = "Expert"
                st.session_state['grid'] = create_sudoku(num_hints=22)
                st.session_state['user_grid'] = [row[:] for row in st.session_state['grid']]
                st.session_state['current_screen'] = 'game'
                st.session_state['start_time'] = time.time()
                st.experimental_rerun()

    # 게임 화면
    elif st.session_state['current_screen'] == 'game':
        st.markdown(f"<h2>난이도: {st.session_state['difficulty']}</h2>", unsafe_allow_html=True)

        if st.session_state['start_time'] is not None:
            st.session_state['elapsed_time'] = time.time() - st.session_state['start_time']
        
        minutes = int(st.session_state['elapsed_time'] // 60)
        seconds = int(st.session_state['elapsed_time'] % 60)
        st.markdown(f"<p class='timer'>시간: {minutes:02}:{seconds:02}</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("다른 난이도 선택(메인으로)", key="go_to_start"):
                st.session_state['current_screen'] = 'start'
                st.experimental_rerun()
        with col2:
            if st.button("새 게임", key="new_game"):
                if st.session_state['difficulty'] == "Easy":
                    num_hints = 48
                elif st.session_state['difficulty'] == "Medium":
                    num_hints = 39
                elif st.session_state['difficulty'] == "Hard":
                    num_hints = 33
                elif st.session_state['difficulty'] == "Very Hard":
                    num_hints = 27
                elif st.session_state['difficulty'] == "Expert":
                    num_hints = 22
                st.session_state['grid'] = create_sudoku(num_hints=num_hints)
                st.session_state['user_grid'] = [row[:] for row in st.session_state['grid']]
                st.session_state['start_time'] = time.time()
                st.experimental_rerun()

        # 스도쿠 그리드 출력
        grid_container = st.empty()
        with grid_container.container():
            st.markdown("<div class='sudoku-grid'>", unsafe_allow_html=True)
            for row in range(9):
                for col in range(9):
                    cell_key = f"cell_{row}_{col}"
                    if st.session_state['grid'][row][col] == 0:
                        cell_value = st.number_input("", value=st.session_state['user_grid'][row][col], min_value=0, max_value=9, key=cell_key, format="%d", label_visibility="collapsed")
                        st.session_state['user_grid'][row][col] = cell_value
                    else:
                        st.markdown(f"<div class='sudoku-cell'>{st.session_state['grid'][row][col]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 조작 버튼
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("정답 확인", key="check_solution"):
                correct_grid = [row[:] for row in st.session_state['grid']]
                if solve_sudoku(correct_grid):
                    if st.session_state['user_grid'] == correct_grid:
                        st.balloons()
                        st.success("축하합니다! 정답입니다.")
                    else:
                        st.error("틀린 부분이 있습니다. 다시 확인해 보세요.")
                else:
                    st.error("오류가 발생했습니다. 나중에 다시 시도해 주세요.")
        with col2:
            if st.button("힌트 보기", key="hint"):
                correct_grid = [row[:] for row in st.session_state['grid']]
                if solve_sudoku(correct_grid):
                    empty_cells = []
                    for row in range(9):
                        for col in range(9):
                            if st.session_state['user_grid'][row][col] == 0:
                                empty_cells.append((row, col))
                    if empty_cells:
                        row, col = random.choice(empty_cells)
                        st.session_state['user_grid'][row][col] = correct_grid[row][col]
                        st.experimental_rerun()
                    else:
                        st.success("모든 칸이 채워져 있습니다!")
                else:
                    st.error("오류가 발생했습니다. 나중에 다시 시도해 주세요.")
        with col3:
            if st.button("초기화", key="reset"):
                st.session_state['user_grid'] = [row[:] for row in st.session_state['grid']]
                st.experimental_rerun()

if __name__ == '__main__':
    main()
