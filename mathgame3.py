import streamlit as st
import random

# -----------------------------
# 페이지 및 세션 초기화
# -----------------------------
st.set_page_config(page_title="들이변환 테트리스", page_icon="🎮", layout="centered")

def init_state():
    defaults = dict(
        score=0,
        lives=3,
        level=1,
        question="",
        answer=None,
        user_answer="",
        msg="",
        msg_type="info",  # info/success/warning/error
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# -----------------------------
# 문제 생성 함수
# -----------------------------
def new_question(level: int):
    pool = [
        ("1 L는 몇 mL일까요?", 1000),
        ("2 L는 몇 mL일까요?", 2000),
        ("3 L는 몇 mL일까요?", 3000),
        ("500 mL는 몇 L일까요?", 0.5),
        ("250 mL는 몇 L일까요?", 0.25),
        ("750 mL는 몇 L일까요?", 0.75),
    ]
    if level >= 2:
        pool += [
            ("4 L는 몇 mL일까요?", 4000),
            ("6 L는 몇 mL일까요?", 6000),
            ("125 mL는 몇 L일까요?", 0.125),
        ]
    if level >= 3:
        pool += [
            ("8 L는 몇 mL일까요?", 8000),
            ("0.25 L는 몇 mL일까요?", 250),
            ("1.5 L는 몇 mL일까요?", 1500),
        ]
    q, a = random.choice(pool)
    st.session_state.question = q
    st.session_state.answer = a
    st.session_state.user_answer = ""

# 첫 진입 시 문제 세팅
if not st.session_state.question:
    new_question(st.session_state.level)

# -----------------------------
# 상단 상태 영역
# -----------------------------
st.title("🎮 들이변환 테트리스")
st.caption("문제를 맞히면 블록이 채워져요! 3번 틀리면 처음부터 다시 시작됩니다.")

stat_cols = st.columns(3)
with stat_cols[0]:
    st.metric("점수", st.session_state.score)
with stat_cols[1]:
    st.metric("남은 기회", st.session_state.lives)
with stat_cols[2]:
    st.metric("레벨", st.session_state.level)

st.divider()

# -----------------------------
# 테트리스 모양 진행도
# -----------------------------
total_cells = 10
filled = min(st.session_state.score // 10 % (total_cells + 1), total_cells)
grid = st.columns(total_cells)
for i, c in enumerate(grid):
    c.markdown("🟩" if i < filled else "⬜", help="정답을 맞히면 칸이 채워져요!")

st.caption("칸을 모두 채우면 레벨 업!")

# -----------------------------
# 메시지 출력
# -----------------------------
msg_area = st.empty()
if st.session_state.msg:
    if st.session_state.msg_type == "success":
        msg_area.success(st.session_state.msg)
    elif st.session_state.msg_type == "warning":
        msg_area.warning(st.session_state.msg)
    elif st.session_state.msg_type == "error":
        msg_area.error(st.session_state.msg)
    else:
        msg_area.info(st.session_state.msg)

# -----------------------------
# 퀴즈 폼
# -----------------------------
with st.form("quiz_form", clear_on_submit=False):
    st.subheader("문제")
    st.write(st.session_state.question)
    st.text_input("정답을 숫자로 입력하세요", key="user_answer")
    submitted = st.form_submit_button("제출하기 ✅")

if submitted:
    user_raw = st.session_state.user_answer.strip()
    try:
        user_value = float(user_raw)
        correct = abs(user_value - float(st.session_state.answer)) < 1e-6
    except ValueError:
        correct = False

    if correct:
        st.session_state.score += 10
        st.session_state.msg = "정답이에요! 블록이 내려옵니다 ⬇️"
        st.session_state.msg_type = "success"

        # 레벨업
        if (st.session_state.score % 100) == 0:
            st.session_state.level += 1
            st.session_state.msg += "  ⭐ 레벨 업!"
        new_question(st.session_state.level)

    else:
        st.session_state.lives -= 1
        if st.session_state.lives <= 0:
            st.session_state.msg = "3번 틀렸어요! 게임이 처음부터 다시 시작됩니다 💥"
            st.session_state.msg_type = "error"
            st.session_state.score = 0
            st.session_state.lives = 3
            st.session_state.level = 1
            new_question(st.session_state.level)
        else:
            st.session_state.msg = f"틀렸어요! 남은 기회: {st.session_state.lives}회"
            st.session_state.msg_type = "warning"
            new_question(st.session_state.level)

    if st.session_state.msg_type == "success":
        msg_area.success(st.session_state.msg)
    elif st.session_state.msg_type == "warning":
        msg_area.warning(st.session_state.msg)
    elif st.session_state.msg_type == "error":
        msg_area.error(st.session_state.msg)
    else:
        msg_area.info(st.session_state.msg)

st.divider()

# -----------------------------
# 다시 시작 버튼
# -----------------------------
cols = st.columns(2)
with cols[0]:
    if st.button("🔄 게임 다시 시작"):
        st.session_state.score = 0
        st.session_state.lives = 3
        st.session_state.level = 1
        st.session_state.msg = "게임이 초기화되었어요. 다시 도전!"
        st.session_state.msg_type = "info"
        new_question(st.session_state.level)

with cols[1]:
    st.caption("💡 팁: 1L = 1000mL 를 기억하세요!")
