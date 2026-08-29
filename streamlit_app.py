import streamlit as st
from openai import OpenAI

# 제목과 설명
st.title("✈️ AI 여행 플래너")
st.write(
    "여행지, 일정, 취향을 알려주면 "
    "AI가 나에게 맞는 여행 코스를 추천해드립니다."
)

# OpenAI API Key 입력
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("OpenAI API Key를 입력해주세요.", icon="🗝️")

else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 대화 내용 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 대화 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("어디로 여행 가고 싶으신가요?"):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
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
            {"role": "assistant", "content": response}
        )
