import streamlit as st
import random

# -----------------------------
# 페이지/세션 초기화
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
# 문제 생성
# -----------------------------
def new_question(level:int):
    """
    3학년 눈높이: L <-> mL 변환 위주.
    level이 올라가면 숫자 범위를 살짝 확장.
    """
    pool = []
    # 기본(쉬움)
    pool += [
        ("1 L는 몇 mL일까요?", 1000),
        ("2 L는 몇 mL일까요?", 2000),
        ("3 L는 몇 mL일까요?", 3000),
        ("500 mL는 몇 L일까요?", 0.5),
        ("250 mL는 몇 L일까요?", 0.25),
        ("750 mL는 몇 L일까요?", 0.75),
    ]
    # 레벨에 따른 가벼운 확장
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

# 첫 진입 시 문제 준비
if not st.session_state.question:
    new_question(st.session_state.level)

# -----------------------------
# 헤더/상태 표시
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
# 테트리스 느낌의 진행도(레벨당 10칸)
# -----------------------------
total_cells = 10
filled = min(st.session_state.score // 10 % (total_cells + 1), total_cells)
grid = st.columns(total_cells)
for i, c in enumerate(grid):
    c.markdown("🟩" if i < filled else "⬜", help="정답을 맞히면 칸이 채워져요!")

st.caption("칸을 모두 채우면 레벨 업!")

# -----------------------------
# 안내 메시지 (콜백 밖에서만 띄움)
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
# 문제/정답 입력 (폼으로 안정 처리)
# -----------------------------
with st.form("quiz_form", clear_on_submit=False):
    st.subheader("문제")
    st.write(st.session_state.question)
    st.text_input("정답을 숫자로 입력하세요", key="user_answer")
    submitted = st.form_submit_button("제출하기 ✅")

if submitted:
    # 콜백 대신 여기서만 상태 변경 및 메시지 갱신 (DOM 에러 방지)
    user_raw = st.session_state.user_answer.strip()
    try:
        user_value = float(user_raw)
        correct = abs(user_value - float(s_
