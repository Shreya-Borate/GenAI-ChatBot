import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = "You are a helpful AI assistant! Your name is Kiki."

st.set_page_config(page_title="Kiki AI", page_icon="🤖")
st.title("🤖 Chat with Kiki")


@st.cache_resource
def get_llm():
    return ChatGroq(model="openai/gpt-oss-120b")


llm = get_llm()

# Keep chat history across Streamlit reruns
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]

# Sidebar
with st.sidebar:
    st.header("Options")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]
        st.rerun()

# Render previous messages (skip the system message)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)


def stream_response(messages):
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content


# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            full_response = st.write_stream(stream_response(st.session_state.messages))
            st.session_state.messages.append(AIMessage(content=full_response))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.session_state.messages.pop()