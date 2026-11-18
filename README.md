# StudyBuddy: AI Learning Chatbot

A simple chatbot that explains AI and machine learning concepts to beginners.
Built for the µLearn CHN AI IG Lead selection task.

**Live demo:** <add your GitHub Pages link here, e.g. https://your-username.github.io/studybuddy-chatbot/>

## Two versions
- `index.html`: web version (rule-based) that runs in any browser and is hosted free on GitHub Pages. No install needed.
- `app.py`: Gradio version with optional Gemini AI mode, run locally (see below).

## Features
- Chat interface built with Gradio
- Two modes: Gemini AI (when an API key is set) and a rule-based fallback (no key needed)
- Handles empty input, very long input, unknown questions and API failures

## Run locally
1. Install Python 3.10 or newer.
2. Clone the repo and open the folder:
   ```
   git clone <your-repo-link>
   cd <repo-folder>
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. (Optional) Enable AI mode: get a free key at https://aistudio.google.com, copy `.env.example` to `.env`, and paste your key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
   Without a key the bot still works in rule-based mode.
5. Start the app:
   ```
   python app.py
   ```
6. Open the link shown in the terminal (usually http://127.0.0.1:7860).

## Approach
StudyBuddy combines two approaches:
- **API-based:** Gemini with a custom system prompt that makes it a short, simple tutor for AI beginners.
- **Rule-based fallback:** keyword matching over a small set of AI topics, used when there is no key or the API is busy.

**What makes it unique:** it never fully breaks. If the AI service fails or hits a rate limit, the user still gets a useful answer instead of an error.

## Challenges and how I solved them
(Edit this section to match your own experience.)
- **API rate limits on the free tier:** added a try/except that falls back to rule-based answers.
- **Keeping the API key safe:** stored it in a `.env` file listed in `.gitignore`, with a `.env.example` for others.
- **Odd inputs:** added checks for empty and overly long messages.
- **Staying on topic:** used a system prompt to steer off-topic questions back to AI.

## Project structure
```
app.py            # chatbot logic + web interface
requirements.txt  # dependencies
.env.example      # template for the API key
.gitignore        # keeps .env out of GitHub
README.md
leadership_plan.md
```
