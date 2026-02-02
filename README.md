# 🦅 EagleEye: Product Image Verification System (BLIP-based)

> [!IMPORTANT]
> **PROTOTYPE / FYP PROJECT**  
> This project is a functional prototype and proof-of-concept for an AI-powered e-commerce fraud detection system.  
> It is intended for **academic, research, and learning purposes**, not direct production use.

---

## 📌 Project Overview

**EagleEye** is an AI-driven tool designed to help detect potential fraud on e-commerce platforms by verifying whether a **product image matches the seller’s claimed title and category**.

Unlike API-based solutions, this system runs **fully offline** using an **open-source vision–language model (BLIP)**. This ensures:

- No API keys
- No usage costs
- Full reproducibility for academic evaluation

The system produces:
- A **confidence score**
- A **verdict** (Match / Uncertain / Mismatch)
- A short **natural-language explanation**

---

## 🧠 Model Used

- **Model**: `Salesforce/blip-vqa-base`
- **Type**: Vision–Language Question Answering (VQA)
- **Framework**: Hugging Face Transformers
- **Execution**: CPU-only, local inference
- **License**: Open-source (ungated)

The model is prompted with structured questions such as:

> *“Does this image show a PlayStation 5 that belongs to the Gaming Console category?”*

---

## ✨ Key Features

- 🔍 **Image–Text Consistency Check**  
  Verifies alignment between product image, title, and category.

- 📊 **Confidence Scoring**  
  Returns a confidence percentage (0–100%) derived from the model’s response.

- 🚦 **Clear Verdicts**  
  - ✅ Match  
  - ⚠️ Uncertain  
  - ❌ Mismatch  

- 📝 **Explainable Output**  
  Natural-language reasoning extracted from the BLIP model’s answer.

- 💻 **Streamlit Web Interface**  
  Simple UI for uploading images and testing product listings.

- 🔐 **No API / Offline Execution**  
  Runs entirely locally with no external service dependency.

---

## 🗂️ Project Structure

```

├── app.py               # Streamlit web application
├── image_verifier.py    # BLIP-based image verification logic
├── requirements.txt     # Pinned dependencies (uv / pip compatible)
└── README.md            # Project documentation

````

---

## ⚙️ Getting Started

### Prerequisites

- Python **3.11** (recommended)
- CPU (GPU not required)
- Internet access (first run only, to download model weights)

---

### Installation (Recommended with `uv`)

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd EagleEye
   ```

2. Create a virtual environment:

   ```bash
   uv venv --python 3.11
   .\.venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   ```

---

### Running the Application

```bash
streamlit run app.py
```

The app will be available at:

```
http://localhost:8501
```

---

## 🧪 How It Works (High Level)

1. User uploads a product image
2. User enters:

   * Product title
   * Product category
3. The system:

   * Asks a structured question to the BLIP VQA model
   * Parses the model’s answer
   * Assigns a confidence score and verdict
4. Results are displayed with visual indicators
