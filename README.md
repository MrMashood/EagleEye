# EagleEye: Product Image Verification System

> [!IMPORTANT]
> **PROTOTYPE**: This project is a functional prototype and proof-of-concept for an AI-powered e-commerce fraud detection system. It is not intended for production use without further development and security enhancements.

## Project Overview

**EagleEye** is an AI-driven REST API designed to protect e-commerce platforms from fraud. It leverages the **Google Gemini API** to analyze product images and verify if they match their provided titles and categories.

This system helps identify mismatches between what a seller describes and what the image actually shows, providing a confidence score and detailed reasoning for its verdict.

## Key Features

- **Automated Image Analysis**: Uses Google Gemini to evaluate product images fetched directly from URLs.
- **Confidence Scoring**: Provides a 0-100% confidence score based on the match quality.
- **Clear Verdicts**: Match, Uncertain, or Mismatch with an aggregate result across multiple images.
- **AI Reasoning**: Detailed explanation from the AI for why a product was flagged or approved.
- **Concurrent Processing**: All images in a request are analyzed simultaneously for fast responses.
- **Request Logging**: Every API call, image fetch, and Gemini request is logged to console and daily log files.
- **REST API**: Clean FastAPI interface -- easily integrated into any e-commerce backend.

## Project Structure

```
.
app.py               - Initializes environment and shared verifier instance
api.py               - FastAPI routes and request/response logic
image_verifier.py    - Core logic for interacting with the Google Gemini API
logger.py            - Structured logging to console and daily log files
requirements.txt     - Python dependencies
.env                 - API key configuration (create from template below)
logs/                - Auto-created, one log file per day
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A Google Gemini API Key (get one at https://aistudio.google.com/app/apikey)

### Installation

1. Clone or download this repository.
2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
```

### Running the API

```bash
uvicorn api:app --reload
```

The API will be available at http://127.0.0.1:8000. Visit http://127.0.0.1:8000/docs for the interactive Swagger UI.

## API Reference

### POST /verify

Accepts a product payload, fetches each image from its URL, and returns per-image and aggregate verification results.

**Request Body:**
```json
{
  "id": 1,
  "title": "The 3 Piece",
  "description": "This is a three piece for ceremonies",
  "catgoryName": "Clothing",
  "media": [
    {
      "id": 1,
      "mediaUrl": "https://example.com/image1.jpeg",
      "mediaType": "jpeg"
    }
  ]
}
```

**Response:**
```json
{
  "productId": 1,
  "title": "The 3 Piece",
  "category": "Clothing",
  "overallVerdict": "Match",
  "overallConfidence": 88,
  "results": [
    {
      "mediaId": 1,
      "mediaUrl": "https://example.com/image1.jpeg",
      "confidence": 88,
      "verdict": "Match",
      "reasoning": "The image clearly shows a three-piece suit...",
      "success": true,
      "error": null
    }
  ]
}
```

**Confidence Levels:**

| Range | Verdict | Meaning |
|-------|---------|---------|
| 70-100% | Match | Image likely matches the listing |
| 30-70% | Uncertain | Partial match or ambiguous |
| 0-30% | Mismatch | Image likely does not match -- possible fraud |

### GET /health

Returns `{status: ok}` -- use this to confirm the server is running.