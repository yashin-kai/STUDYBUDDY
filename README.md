# StudyBuddy: AI Chatbot for Students

A conversational AI chatbot built with Streamlit and Google Gemini.
Made for the µLearn CHN AI IG Lead selection task.

**Live demo:** <add your Streamlit app link here, e.g. https://your-app-name.streamlit.app>

## Features
- Real AI conversation (not scripted replies) that remembers the earlier messages in the chat
- Answers stream in word by word, like a modern chat app
- Clear chat button
- Friendly error messages if the AI service is busy, plus a check for overly long messages
- API key kept in secrets, never in the code

## Run locally
1. Install Python 3.10 or newer.
2. Clone the repo and go into the folder:
   ```
   git clone <your-repo-link>
   cd <repo-folder>
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Get a free API key from https://aistudio.google.com.
5. Create a file `.streamlit/secrets.toml` with:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```
6. Start the app:
   ```
   streamlit run streamlit_app.py
   ```
7. Open http://localhost:8501.

## Deploy for free
1. Push the repo to GitHub (never commit `secrets.toml`).
2. Sign in to https://share.streamlit.io with GitHub and create a new app from the repo, with `streamlit_app.py` as the main file.
3. In the app's Settings → Secrets, paste: `GEMINI_API_KEY = "your_key_here"`.

## Approach
**API-based generative AI.** The app sends the conversation history to the Gemini model together with a custom system prompt that makes it a friendly, concise tutor for students. Streamlit's chat components provide the interface.

**What makes it unique:** it is built for students, with a system prompt tuned to explain AI and programming topics simply, streaming replies, and graceful handling of failures.

## Challenges and how I solved them
(Edit this section to match your own experience.)
- **Free hosting for a Gradio app:** Hugging Face now requires a paid plan for Gradio Spaces, so I switched to Streamlit Community Cloud, which is free and deploys from GitHub.
- **Keeping the API key safe:** stored it in Streamlit secrets and listed secret files in `.gitignore`.
- **API rate limits on the free tier:** wrapped the call in error handling that shows a friendly message and keeps the chat usable.
- **Unusual inputs:** added a length limit and a limit on how much history is sent.

## Project structure
```
streamlit_app.py   # chatbot logic + web interface
requirements.txt   # dependencies
.gitignore         # keeps secrets out of GitHub
README.md
leadership_plan.md
```
