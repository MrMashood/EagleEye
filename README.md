# 🦅 EagleEye: Product Image Verification System

> [!IMPORTANT]
> **PROTOTYPE**: This project is a functional prototype and proof-of-concept for an AI-powered e-commerce fraud detection system. It is not intended for production use without further development and security enhancements.

## Project Overview

**EagleEye** is an AI-driven tool designed to protect e-commerce platforms from fraud. It leverages the **Google Gemini API** to analyze product images and verify if they match their provided titles and categories.

This system helps identify mismatches between what a seller describes and what the image actually shows, providing a confidence score and detailed reasoning for its verdict.

## Key Features

- 🔍 **Automated Image Analysis**: Uses Google Gemini Pro Vision to "see" and evaluate product images.
- 📉 **Confidence Scoring**: Provides a 0-100% confidence score based on the match quality.
- 🚦 **Visual Verdicts**: Clear color-coded results (Green/Yellow/Red) for quick decision making.
- 📝 **AI Reasoning**: Detailed explanations from the AI explaining why a product was flagged or approved.
- 💻 **Streamlit UI**: Simple and intuitive web interface for uploading and testing images.

## Project Structure

- `app.py`: The main Streamlit web application.
- `image_verifier.py`: The core logic for interacting with the Google Gemini API.
- `requirements.txt`: Python dependencies.
- `.env`: Configuration for API keys (to be created from template).

## Getting Started

### Prerequisites

- Python 3.9 or higher
- A Google Gemini API Key (get one at [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. Clone or download this repository.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Locate the `.env` file in the project root.
2. Replace `your_api_key_here` with your actual Google API key.

### Running the App

Start the Streamlit server:
```bash
streamlit run app.py
```
The app should automatically open in your default web browser.

## Disclaimer

This prototype uses AI to make judgments. While powerful, AI can make mistakes (hallucinations or misidentifications). Always use human oversight for final fraud determinations.
