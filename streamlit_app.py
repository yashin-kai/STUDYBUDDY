"""StudyBuddy - an AI chatbot built with Streamlit and Google Gemini."""

import os

import streamlit as st
from google import genai
from google.genai import types

MAX_INPUT_CHARS = 1000
MAX_HISTORY_MESSAGES = 20

SYSTEM_PROMPT = (
    "You are StudyBuddy, a friendly and helpful AI assistant for students. "
    "You can chat about any topic, and you are especially good at explaining "
    "AI, programming and study topics in simple language with short examples. "
    "Be clear, honest and concise. If you are not sure about something, say so."
)

st.set_page_config(page_title="StudyBuddy", page_icon="💬")
st.title("💬 StudyBuddy")
st.caption("An AI chatbot for students. Ask me anything!")


def get_secret(name, default=None):
    """Read a setting from Streamlit secrets or environment variables."""
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, default)


API_KEY = get_secret("GEMINI_API_KEY")
MODEL = get_secret("GEMINI_MODEL", "gemini-flash-latest")

if not API_KEY:
    st.error("No API key found. Add GEMINI_API_KEY in the app's Secrets (see README).")
    st.stop()

client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm StudyBuddy. What would you like to talk about or learn today?"}
    ]

with st.sidebar:
    st.header("About")
    st.write("StudyBuddy is powered by Google Gemini and built with Streamlit.")
    if st.button("Clear chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()


def stream_reply(history):
    """Send the conversation to Gemini and yield the answer piece by piece."""
    contents = []
    for m in history[-MAX_HISTORY_MESSAGES:]:
        role = "user" if m["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    ):
        if chunk.text:
            yield chunk.text


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    prompt = prompt.strip()
    if len(prompt) > MAX_INPUT_CHARS:
        st.warning(f"That message is too long. Please keep it under {MAX_INPUT_CHARS} characters.")
    elif prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                reply = st.write_stream(stream_reply(st.session_state.messages))
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as error:  # rate limit, network problem, bad key...
                print(f"[warning] API error: {error}")
                st.session_state.messages.pop()  # remove the unanswered user message
                st.error("Sorry, the AI service is busy or unavailable right now. Please try again in a minute.")
                st.caption(f"Technical detail: {str(error)[:300]}")
