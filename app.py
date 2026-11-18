"""StudyBuddy - a beginner-friendly AI tutor chatbot.

Two modes:
1. Gemini mode: used when GEMINI_API_KEY is set (free key from Google AI Studio).
2. Rule-based mode: keyword answers, used when there is no key or the API fails.
"""

import os

import gradio as gr
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_INPUT_CHARS = 1000
MAX_HISTORY_TURNS = 10

SYSTEM_PROMPT = (
    "You are StudyBuddy, a friendly tutor for students new to AI and machine "
    "learning. Explain ideas simply with short examples. Keep answers under "
    "120 words. If a question is unrelated to AI, tech or studying, politely "
    "steer back to those topics."
)

# ---------- Rule-based knowledge (fallback) ----------
KNOWLEDGE = {
    ("hello", "hi", "hey"): "Hi! I'm StudyBuddy. Ask me about AI, machine learning, chatbots or LLMs.",
    ("what is ai", "artificial intelligence"): "AI is software that does tasks that normally need human intelligence, like understanding language, recognising images or making decisions.",
    ("machine learning", "what is ml"): "Machine learning is a way of teaching computers using data instead of fixed rules. The model finds patterns and improves with examples.",
    ("deep learning", "neural network"): "Neural networks are layers of simple connected units loosely inspired by the brain. Deep learning means using many layers to learn complex patterns.",
    ("llm", "large language model", "gpt", "gemini"): "An LLM is a neural network trained on huge amounts of text to predict the next word. That skill lets it write, answer questions and chat.",
    ("rag", "retrieval"): "RAG (Retrieval-Augmented Generation) lets a model look up relevant documents first, then answer using them. That reduces made-up answers.",
    ("prompt",): "A prompt is the instruction you give an AI model. Clear, specific prompts with examples give better results.",
    ("fine tune", "fine-tune"): "Fine-tuning means training an existing model a bit more on your own data so it specialises in your task.",
    ("chatbot",): "A chatbot is a program that talks with users. It can be rule-based (fixed replies) or AI-based (generated replies).",
    ("python",): "Python is the most popular language for AI because of libraries like NumPy, PyTorch and scikit-learn.",
    ("joke",): "Why did the neural network fail class? It kept overfitting to the practice questions!",
    ("thanks", "thank you"): "You're welcome! Ask me anything else.",
    ("bye", "goodbye"): "Bye! Keep learning!",
}

FALLBACK = (
    "I'm not sure about that one. Try asking about AI, machine learning, "
    "LLMs, RAG, prompts or chatbots."
)


def rule_based_reply(message: str) -> str:
    text = message.lower()
    for keywords, answer in KNOWLEDGE.items():
        if any(k in text for k in keywords):
            return answer
    return FALLBACK


# ---------- Gemini mode ----------
def gemini_reply(message: str, history: list) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=API_KEY)
    contents = []
    for turn in history[-MAX_HISTORY_TURNS * 2:]:
        role = "user" if turn["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=str(turn["content"]))]))
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return (response.text or "").strip() or FALLBACK


# ---------- Chat function used by the UI ----------
def respond(message, history):
    message = (message or "").strip()
    if not message:
        return "Please type a question first."
    if len(message) > MAX_INPUT_CHARS:
        return f"That message is too long. Please keep it under {MAX_INPUT_CHARS} characters."

    if API_KEY:
        try:
            return gemini_reply(message, history)
        except Exception as error:  # rate limit, network error, bad key...
            print(f"[warning] API failed, using rule-based reply: {error}")
            return rule_based_reply(message) + "\n\n(AI service is busy, so this is a basic answer.)"
    return rule_based_reply(message)


demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    title="StudyBuddy: your AI learning companion",
    description="Ask me anything about AI, machine learning and chatbots.",
    examples=["What is machine learning?", "Explain RAG simply", "What is an LLM?", "Tell me a joke"],
)

if __name__ == "__main__":
    demo.launch()
