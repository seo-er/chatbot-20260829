import streamlit as st
from openai import OpenAI
import json

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="AI 여행 플래너",
    page_icon="✈️",
    layout="centered"
)

# --------------------------------------------------
# 기본 스타일
# --------------------------------------------------

st.markdown("""
<style>

    /* 전체 */
    .stApp {
        background-color: #ffffff;
    }

    /* 상단 제목 */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .main-description {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 28px;
    }

    /* 빠른 질문 카드 */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* 버튼 */
    div.stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 500;
    }

    /* 채팅 메시지 */
    [data-testid="stChatMessage"] {
        padding: 10px 0;
    }

    /* 입력창 */
    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        border-right: 1px solid #eeeeee;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 세션 상태
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None


# --------------------------------------------------
# API Key
# --------------------------------------------------

with st.sidebar:

    st.markdown("### ⚙️ 설정")

    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="API Key 입력"
    )

    st.divider()

    st.markdown("### ✈️ 여행 설정")

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
        "💰 예산",
        [
            "가성비",
            "보통",
            "여유롭게",
            "상관없음"
        ]
    )

    st.divider()

    # 새 여행
    if st.button(
        "🗑️ 새 여행 시작",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.uploaded_file = None
        st.rerun()


# --------------------------------------------------
# API Key 체크
# --------------------------------------------------

if not openai_api_key:

    st.markdown(
        '<div class="main-title">✈️ AI 여행 플래너</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-description">'
        '나에게 맞는 여행을 AI와 함께 계획해보세요.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "🔑 왼쪽 설정에서 OpenAI API Key를 입력해주세요."
    )

    st.stop()


# --------------------------------------------------
# OpenAI
# --------------------------------------------------

client = OpenAI(api_key=openai_api_key)


# --------------------------------------------------
# AI 역할
# --------------------------------------------------

system_message = f"""
너는 전문 여행 플래너 AI야.

사용자의 여행 목적과 취향을 파악하고
실제로 사용할 수 있는 여행 계획을 만들어줘.

현재 여행 설정:

- 여행지: {destination if destination else "미정"}
- 여행 기간: {days}일
- 동행: {companion}
- 여행 스타일: {travel_style}
- 예산: {budget}

답변 원칙:

1. 사용자의 여행 조건을 최대한 반영한다.
2. 이동 동선을 고려해서 일정을 구성한다.
3. Day 1, Day 2, Day 3 형식으로 정리한다.
4. 각 일정에 장소와 추천 이유를 함께 설명한다.
5. 맛집, 카페, 관광지를 적절하게 조합한다.
6. 너무 긴 설명보다 실제 여행에 바로 사용할 수 있도록 정리한다.
7. 사용자의 질문에 필요한 정보가 부족하면 먼저 질문한다.
8. 친절하고 자연스럽게 대화한다.
"""


# --------------------------------------------------
# 헤더
# --------------------------------------------------

st.markdown(
    '<div class="main-title">✈️ AI 여행 플래너</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-description">'
    '여행지와 취향을 알려주면 나에게 맞는 여행을 함께 계획해드려요.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# 공유하기 기능
# --------------------------------------------------

def share_conversation():

    if not st.session_state.messages:
        st.warning("먼저 AI와 여행 계획을 만들어보세요.")
        return

    conversation_text = "✈️ AI 여행 플래너\n\n"

    for message in st.session_state.messages:

        if message["role"] == "user":
            conversation_text += "🙋 나\n"
        else:
            conversation_text += "✈️ AI 여행 플래너\n"

        conversation_text += message["content"]
        conversation_text += "\n\n"

    # HTML을 이용해서 클립보드 복사
    escaped_text = json.dumps(conversation_text)

    st.markdown(
        f"""
        <script>
        navigator.clipboard.writeText({escaped_text});
        </script>
        """,
        unsafe_allow_html=True
    )

    st.success("여행 계획이 클립보드에 복사됐어요!")


# --------------------------------------------------
# 첫 화면
# --------------------------------------------------

prompt = None

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="section-title">👋 무엇을 도와드릴까요?</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "아래에서 원하는 여행 계획을 선택하거나 직접 질문해보세요."
    )

    # 빠른 질문
    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗺️ 여행 일정 짜기",
            use_container_width=True
        ):
            prompt = "내 여행 조건에 맞춰 전체 여행 일정을 짜줘."

        if st.button(
            "🍴 맛집 중심 여행",
            use_container_width=True
        ):
            prompt = "맛집을 중심으로 여행 코스를 추천해줘."

        if st.button(
            "🌿 힐링 여행",
            use_container_width=True
        ):
            prompt = "휴식과 힐링을 중심으로 여행 코스를 추천해줘."

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
            prompt = "비용을 아끼면서 여행할 수 있는 코스를 추천해줘."

        if st.button(
            "☕ 카페 여행",
            use_container_width=True
        ):
            prompt = "분위기 좋은 카페를 중심으로 여행 코스를 추천해줘."


# --------------------------------------------------
# 기존 대화 표시
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# 하단 버튼 영역
# --------------------------------------------------

st.divider()

col1, col2 = st.columns([1, 5])

with col1:

    # + 버튼
    with st.popover("＋"):

        st.markdown("### 추가하기")

        uploaded_file = st.file_uploader(
            "여행 관련 파일을 추가하세요.",
            type=[
                "txt",
                "pdf",
                "png",
                "jpg",
                "jpeg"
            ]
        )

        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.success(
                f"{uploaded_file.name} 추가됨"
            )

with col2:

    # 공유 버튼
    if st.button(
        "↗ 공유하기",
        use_container_width=True
    ):
        share_conversation()


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

    # --------------------------------------------------
    # 파일 정보
    # --------------------------------------------------

    file_info = ""

    if st.session_state.uploaded_file:

        file_info = f"""

사용자가 다음 파일을 추가했습니다:

파일명:
{st.session_state.uploaded_file.name}

파일 형식:
{st.session_state.uploaded_file.type}

파일이 있다는 점을 고려해서 답변해줘.
"""


    # --------------------------------------------------
    # 사용자 메시지 저장
    # --------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # --------------------------------------------------
    # 사용자 메시지 표시
    # --------------------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)

        if st.session_state.uploaded_file:

            st.caption(
                f"📎 {st.session_state.uploaded_file.name}"
            )


    # --------------------------------------------------
    # AI 요청
    # --------------------------------------------------

    try:

        messages_for_api = [
            {
                "role": "system",
                "content": system_message + file_info
            }
        ]

        messages_for_api.extend(
            st.session_state.messages
        )

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_for_api,
            stream=True
        )


        # --------------------------------------------------
        # AI 답변
        # --------------------------------------------------

        with st.chat_message("assistant"):

            response = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
                if chunk.choices
            )


        # --------------------------------------------------
        # 답변 저장
        # --------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # 파일 초기화
        st.session_state.uploaded_file = None

    except Exception:

        # 실패한 사용자 메시지 제거
        st.session_state.messages.pop()

        st.error(
            "AI 응답을 가져오지 못했어요. "
            "API Key를 확인해주세요."
        )
