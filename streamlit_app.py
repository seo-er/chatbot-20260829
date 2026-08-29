import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💡 AI 창업 상담소")
st.write(
    "아이디어부터 사업계획, 타깃 고객, 수익모델까지 "
    "AI와 함께 창업 아이디어를 구체화해보세요."
)

# Ask user for their OpenAI API key.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("OpenAI API Key를 입력해주세요.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create chat input.
    if prompt := st.chat_input("창업 아이디어를 입력해보세요."):

        # Store and display the current prompt.
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # Store the response.
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
