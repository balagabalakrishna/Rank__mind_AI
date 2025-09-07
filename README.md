# Rank Mind AI
RankMind AI – Multi-Model LLM Answer Comparison & Ranking Tool

## Overview

RankMind AI is a cutting-edge web application that lets users input a single prompt and receive side-by-side answers from five major AI language models:

OpenAI's GPT-4

Google Gemini

Meta's LLaMA 3.1

Cohere Command R+

DeepSeek Chat

🔍 The app then automatically ranks the AI responses based on accuracy, relevance, and clarity, providing insights into which model performs best for different types of queries.

## My Role

Team Lead | Backend Developer (Flask) | API Integrator | Prompt Engineer

Led the backend development and designed the architecture to handle real-time API requests to multiple LLMs.

Integrated APIs from 5 different AI providers, handled authentication, token limits, and error handling.

Engineered smart prompt formats and post-processing logic to enable fair ranking.

Collaborated with frontend team to create a clean and intuitive comparison interface.

Used SQLite to store usage data and track model performance history.

🧠 Core Features

💬 Prompt once, get responses from 5 AI models

📊 Intelligent ranking algorithm based on relevance and accuracy

🧠 Prompt engineering logic to maintain consistency across models

🖥️ Clean React frontend for real-time, side-by-side comparisons

💾 Lightweight SQLite database for data logging and feedback

🔐 Secure API key management and error handling

## How It Works

User submits a prompt

Flask backend calls all 5 AI APIs simultaneously

Responses are normalized and passed through a ranking function

Frontend displays all responses side-by-side with a clear rank

Optional: Store data in SQLite for model performance tracking


## Future Improvements

✅ Feedback system to let users vote on rankings

✅ Auto-learning ranking logic via ML

🌐 Full user login & session history

📱 Mobile-friendly UI

💡 Chat history and follow-up prompt support
