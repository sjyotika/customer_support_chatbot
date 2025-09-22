

---

# 💬 Customer Support Chatbot

An AI-powered customer support chatbot built with **Streamlit**, **SentenceTransformers**, and **FAISS**.
It can answer customer queries about **orders, returns, payments, shipping, refunds, and cancellations**, using a **semantic search knowledge base** with fallback rules for common queries.

---

## 🚀 Features

* 🔍 **Semantic Search**: Finds the most relevant answer using FAISS similarity search.
* 🧠 **Transformer-based Embeddings**: Uses `sentence-transformers` for accurate intent matching.
* 🛠 **Fallback Responses**: Smart default answers for common queries (e.g., "track order", "refund").
* 💡 **Interactive UI**: Built with **Streamlit chat components** and styled chat bubbles.
* ☁️ **Lightweight Deployment**: Large files are hosted on Google Drive and auto-downloaded at runtime.

---

## 📂 Project Structure

```
.
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

⚠️ Large files (`.faiss`, `.pkl`, `model_name.txt`) are stored on **Google Drive**, not GitHub.
They are automatically downloaded when the app starts.

---

## ⚡ Installation & Setup

### 1️⃣ Clone the repo

```bash
git clone https://github.com/sjyotika/customer-support-chatbot.git
cd customer-support-chatbot
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push this repo to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your GitHub repo.
3. Set the entry point to `app.py`.
4. App will install dependencies from `requirements.txt` and run automatically.

---

## 📥 Large File Handling

Since `.faiss` and `.pkl` files are too large for GitHub:

* They are hosted on **Google Drive**.
* `app.py` automatically downloads them on first run.

🔑 To make it work:

* Upload your files to Google Drive.
* Get their **file IDs** (from share links).
* Replace them in `app.py`:

```python
drive_files = {
    "knowledge_base.pkl": "YOUR_KB_FILE_ID",
    "ecommerce_index.faiss": "YOUR_FAISS_FILE_ID",
    "model_name.txt": "YOUR_MODEL_FILE_ID"
}
```

---

## 🛠 Requirements

* Python 3.8+
* [Streamlit](https://streamlit.io/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Sentence Transformers](https://www.sbert.net/)

---

## 🎯 Example Queries

* "How do I track my order?"
* "What is the refund policy?"
* "Which payment methods are supported?"
* "Tell me about shipping times."

---

✨ Built with [Streamlit](https://streamlit.io/) and ❤️

---

