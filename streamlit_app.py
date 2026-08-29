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
# 기본 설정
# --------------------------------------------------

st.title("✈️ AI 여행 플래너")
st.caption("여행 계획부터 일정 추천까지, 나만의 여행을 함께 설계해보세요.")

# --------------------------------------------------
# 사이드바
# --------------------------------------------------

with st.sidebar:
    st.header("⚙️ 여행 정보")

    destination = st.text_input(
        "여행지",
        placeholder="예: 제주도"
    )

    days = st.number_input(
        "여행 기간",
        min_value=1,
        max_value=30,
        value=3
    )

    travel_style = st.selectbox(
        "여행 스타일",
        [
            "맛집 중심",
            "관광 중심",
            "힐링 중심",
            "액티비티 중심",
            "카페 중심",
            "쇼핑 중심",
            "균형 있게"
        ]
    )

    budget = st.selectbox(
        "예산",
        [
            "가성비 여행",
            "보통",
            "여유롭게",
            "상관없음"
        ]
    )

    companion = st.selectbox(
        "동행",
        [
            "혼자",
            "친구",
            "연인",
            "가족",
            "아이와 함께"
        ]
    )

    st.divider()

    if st.button("🗑️ 새 여행 시작", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# OpenAI API Key
# --------------------------------------------------

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="API Key를 입력해주세요."
)

if not openai_api_key:
    st.info(
        "🔑 OpenAI API Key를 입력하면 AI 여행 플래너를 사용할 수 있어요."
    )

else:

    # --------------------------------------------------
    # OpenAI 클라이언트
    # --------------------------------------------------

    client = OpenAI(api_key=openai_api_key)

    # --------------------------------------------------
    # 대화 기록
    # --------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --------------------------------------------------
    # AI 역할 설정
    # --------------------------------------------------

    system_message = f"""
    너는 전문 여행 플래너 AI다.

    사용자의 여행 목적과 취향을 파악하고
    실제 여행에 도움이 되는 구체적인 여행 계획을 제안한다.

    현재 여행 정보:
    - 여행지: {destination if destination else "미정"}
    - 기간: {days}일
    - 여행 스타일: {travel_style}
    - 예산: {budget}
    - 동행: {companion}

    답변 원칙:
    1. 사용자의 조건을 우선적으로 반영한다.
    2. 여행 일정을 시간 순서대로 보기 쉽게 정리한다.
    3. 이동 동선을 고려한다.
    4. 맛집, 관광지, 카페 등을 적절하게 조합한다.
    5. 사용자가 조건을 충분히 제공하지 않았다면 필요한 정보를 질문한다.
    6. 답변은 너무 길지 않게 핵심 위주로 작성한다.
    7. 일정 추천 시 'Day 1, Day 2' 형식으로 구분한다.
    """

    # --------------------------------------------------
    # 환영 메시지
    # --------------------------------------------------

    if len(st.session_state.messages) == 0:
        st.markdown("### 👋 어떤 여행을 계획하고 계신가요?")
        st.write(
            "왼쪽에서 여행 정보를 설정하거나 "
            "아래에서 원하는 것을 바로 선택해보세요."
        )

        # --------------------------------------------------
        # 대화 스타터
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "🗺️ 여행 일정 짜기",
                use_container_width=True
            ):
                prompt = "내 여행 조건에 맞춰 전체 여행 일정을 짜줘."

            if st.button(
                "🍴 맛집 중심 코스",
                use_container_width=True
            ):
                prompt = "맛집을 중심으로 여행 코스를 추천해줘."

        with col2:
            if st.button(
                "📸 인생샷 여행지",
                use_container_width=True
            ):
                prompt = "사진 찍기 좋은 여행지를 중심으로 코스를 추천해줘."

            if st.button(
                "💰 가성비 여행",
                use_container_width=True
            ):
                prompt = "예산을 아끼면서 여행할 수 있는 코스를 추천해줘."

    else:
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

        # API 요청
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                }
            ] + [
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # AI 응답 표시
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # AI 응답 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )
