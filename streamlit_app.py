import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="AI 여행 플래너",
    page_icon="✈️",
    layout="centered"
)

# --------------------------------------------------
# 제목
# --------------------------------------------------

st.title("✈️ AI 여행 플래너")
st.caption("나에게 맞는 여행을 AI와 함께 계획해보세요.")

# --------------------------------------------------
# API Key
# --------------------------------------------------

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="OpenAI API Key를 입력해주세요."
)

if not openai_api_key:
    st.info(
        "🔑 OpenAI API Key를 입력하면 여행 플래너를 사용할 수 있습니다."
    )
    st.stop()

# --------------------------------------------------
# OpenAI
# --------------------------------------------------

client = OpenAI(api_key=openai_api_key)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# 사이드바 - 여행 설정
# --------------------------------------------------

with st.sidebar:

    st.header("✈️ 여행 설정")
    st.caption("여행 정보를 입력하면 AI가 추천에 반영합니다.")

    destination = st.text_input(
        "📍 여행지",
        placeholder="예: 제주도"
    )

    days = st.number_input(
        "📅 여행 기간",
        min_value=1,
        max_value=30,
        value=3
    )

    companion = st.selectbox(
        "👥 누구와 함께 가나요?",
        [
            "혼자",
            "친구",
            "연인",
            "가족",
            "아이와 함께"
        ]
    )

    travel_style = st.selectbox(
        "✨ 여행 스타일",
        [
            "균형 있게",
            "맛집 중심",
            "관광 중심",
            "힐링 중심",
            "카페 중심",
            "액티비티 중심",
            "쇼핑 중심"
        ]
    )

    budget = st.selectbox(
        "💰 여행 예산",
        [
            "가성비",
            "보통",
            "여유롭게",
            "상관없음"
        ]
    )

    st.divider()

    # 새 대화 버튼
    if st.button(
        "🗑️ 새 여행 시작",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# AI 역할
# --------------------------------------------------

system_message = f"""
너는 전문 여행 플래너 AI야.

사용자의 여행 정보를 바탕으로
실제로 활용할 수 있는 여행 계획과 추천을 제공해.

현재 설정된 여행 정보:

- 여행지: {destination if destination else "아직 정하지 않음"}
- 여행 기간: {days}일
- 동행: {companion}
- 여행 스타일: {travel_style}
- 예산: {budget}

답변할 때 다음 원칙을 지켜.

1. 사용자가 입력한 여행 조건을 최대한 반영한다.
2. 여행 일정은 이동 동선을 고려한다.
3. 필요한 경우 일정에 관광지, 맛집, 카페 등을 적절하게 배치한다.
4. 일정은 Day 1, Day 2처럼 구분해서 보여준다.
5. 너무 긴 설명보다는 실제로 사용하기 쉬운 형태로 정리한다.
6. 사용자가 정보가 부족한 경우 필요한 질문을 먼저 한다.
7. 사용자가 특정 장소나 활동을 요청하면 그 요청을 우선한다.
8. 답변은 친절하고 이해하기 쉽게 작성한다.
"""

# --------------------------------------------------
# 첫 화면
# --------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown("### 👋 어떤 여행을 계획하고 계신가요?")

    st.write(
        "왼쪽에서 여행 정보를 설정하거나 "
        "아래의 빠른 시작 메뉴를 선택해보세요."
    )

    st.markdown("#### 🚀 빠른 시작")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗺️ 여행 일정 짜기",
            use_container_width=True
        ):
            prompt = "내 여행 조건에 맞춰 전체 여행 일정을 짜줘."

        if st.button(
            "🍴 맛집 여행",
            use_container_width=True
        ):
            prompt = "맛집을 중심으로 여행 코스를 짜줘."

        if st.button(
            "🌿 힐링 여행",
            use_container_width=True
        ):
            prompt = "힐링과 휴식을 중심으로 여행 코스를 짜줘."

    with col2:

        if st.button(
            "📸 인생샷 여행",
            use_container_width=True
        ):
            prompt = "사진 찍기 좋은 장소를 중심으로 여행 코스를 추천해줘."

        if st.button(
            "💰 가성비 여행",
            use_container_width=True
        ):
            prompt = "비용을 최대한 아끼면서 여행할 수 있는 코스를 추천해줘."

        if st.button(
            "☕ 카페 여행",
            use_container_width=True
        ):
            prompt = "분위기 좋은 카페를 중심으로 여행 코스를 추천해줘."

else:

    prompt = None

# --------------------------------------------------
# prompt 기본값
# --------------------------------------------------

if "prompt" not in locals():
    prompt = None

# --------------------------------------------------
# 기존 대화 표시
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# 채팅 입력
# --------------------------------------------------

chat_prompt = st.chat_input(
    "여행에 대해 무엇이든 물어보세요 ✈️"
)

if chat_prompt:
    prompt = chat_prompt

# --------------------------------------------------
# AI 응답
# --------------------------------------------------

if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI 요청
    try:

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                }
            ] + st.session_state.messages,
            stream=True
        )

        # AI 답변
        with st.chat_message("assistant"):

            response = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
                if chunk.choices
            )

        # AI 답변 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

    except Exception as e:

        st.error(
            "AI 응답을 가져오는 중 문제가 발생했습니다."
        )

        # 오류가 난 사용자 메시지는 삭제
        st.session_state.messages.pop()

        st.caption(
            "API Key가 올바른지 확인하거나 잠시 후 다시 시도해주세요."
        )
