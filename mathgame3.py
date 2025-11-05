import streamlit as st
import random
import time

# -----------------------------------
# 초기 설정
# -----------------------------------
st.set_page_config(page_title="들이변환 테트리스", layout="centered")

if "score" not in st.session_state:
    st.session_state.score = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "block_ready" not in st.session_state:
    st.session_state.block_ready = True
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = 0
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

# -----------------------------------
# 함수 정의
# -----------------------------------
def new_question():
    """새 들이변환 문제 생성"""
    problems = [
        ("1L는 몇 mL일까요?", 1000),
        ("2L는 몇 mL일까요?", 2000),
        ("500mL는 몇 L일까요?", 0.5),
        ("750mL는 몇 L일까요?", 0.75),
        ("3L는 몇 mL일까요?", 3000),
        ("0.25L는 몇 mL일까요?", 250),
    ]
    q, a = random.choice(problems)
    st.session_state.question = q
    st.session_state.answer = a
    st.session_state.user_answer = ""


def check_answer():
    """정답 확인 및 점수 반영"""
    try:
        user_value = float(st.session_state.user_answer)
    except ValueError:
        st.warning("숫자로 입력해주세요!")
        return

    if abs(user_value - st.session_state.answer) < 0.001:
        st.success("정답이에요! 블록이 내려옵니다 ⬇️")
        st.session_state.score += 10
        new_question()
    else:
        st.session_state.lives -= 1
        if st.session_state.lives <= 0:
            st.error("3번 틀렸어요! 게임이 다시 시작됩니다 💥")
            st.session_state.score = 0
            st.session_state.lives = 3
        else:
            st.warning(f"틀렸어요! 남은 기회: {st.session_state.lives}회")
        new_question()


# -----------------------------------
# UI 구성
# -----------------------------------
st.title("🎮 들이변환 테트리스 게임")
st.write("문제를 맞혀야 블록이 내려옵니다! 3번 틀리면 처음부터 시작돼요.")

st.markdown("---")
st.metric(label="점수", value=st.session_state.score)
st.metric(label="남은 기회", value=st.session_state.lives)
st.markdown("---")

# 문제 영역
if not st.session_state.question:
    new_question()

st.subheader("문제")
st.write(st.session_state.question)
st.text_input("정답을 입력하세요", key="user_answer", on_change=check_answer)

# 시각적 게임 흉내(단순 애니메이션 효과)
st.markdown("---")
cols = st.columns(10)
filled_cols = min(st.session_state.score // 10, 10)
for i, c in enumerate(cols):
    if i < filled_cols:
        c.markdown("🟩")
    else:
        c.markdown("⬜")

st.caption("블록이 가득 차면 다음 레벨로 이동!")

# -----------------------------------
# 레벨업 처리
# -----------------------------------
if st.session_state.score >= 100:
    st.balloons()
    st.success("🎉 축하해요! 모든 블록을 쌓았어요! 🎉")
    if st.button("다시 시작"):
        st.session_state.score = 0
        st.session_state.lives = 3
        new_question()
