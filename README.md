# Rank Mind AI

A Streamlit application that compares responses from multiple LLM APIs side by side.

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`

## Features

- Compare responses from Together AI, Cohere, and Hugging Face models
- Clean, responsive UI with side-by-side comparison
- Error handling for API requests
- Session state management for previous responses

## API Keys

The application uses the following API keys configured in `config.py`:
- Together AI
- Cohere
- Hugging Face

Note: Make sure to use free tier compatible models and monitor your API usage.