import streamlit as st
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import os
import requests

st.set_page_config(page_title="Support Chat", page_icon="💬", layout="centered")

# ---------------- Helper: Download from Google Drive ----------------
def download_file_from_google_drive(file_id, dest_path):
    if not os.path.exists(dest_path):
        try:
            st.info(f"📥 Downloading {dest_path} ... (first run only)")
            url = f"https://drive.google.com/file/d/110kqwva3rwpIZauCrzwytOga3ZK1HB3L/view?usp=drive_link"
            response = requests.get(url)
            with open(dest_path, "wb") as f:
                f.write(response.content)
            st.success(f"✅ Downloaded {dest_path}")
        except Exception as e:
            st.error(f"⚠️ Failed to download {dest_path}: {e}")

# ---------------- Load System ----------------
@st.cache_resource
def load_system():
    try:
        # Replace with your own Google Drive file IDs
        drive_files = {
            "knowledge_base.pkl": "YOUR_KB_FILE_ID",
            "ecommerce_index.faiss": "YOUR_FAISS_FILE_ID",
            "model_name.txt": "YOUR_MODEL_FILE_ID"
        }

        # Download missing files
        for fname, fid in drive_files.items():
            download_file_from_google_drive(fid, fname)

        # Load model name
        with open("model_name.txt", "r") as f:
            model_name = f.read().strip()

        model = SentenceTransformer(model_name)

        # Load knowledge base
        with open("knowledge_base.pkl", "rb") as f:
            knowledge_base = pickle.load(f)

        # Load FAISS index
        index = faiss.read_index("ecommerce_index.faiss")

        return model, knowledge_base, index

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        return None, None, None

# ---------------- Fallback ----------------
def get_fallback(query):
    query_lower = query.lower()
    responses = {
        "track": "📦 Track your order in 'My Account' > 'Order History'.",
        "return": "🔄 We offer 30-day returns. Start in your account.",
        "refund": "💵 Refunds process in 5-7 business days.",
        "cancel": "❌ Cancel orders within 1 hour in your account.",
        "shipping": "🚚 Standard: 3-5 days, Express: 1-2 days",
        "payment": "💳 We accept cards, PayPal, Apple Pay, Google Pay",
    }

    for keyword, response in responses.items():
        if keyword in query_lower:
            return {"answer": response, "confidence": "Medium"}

    return {
        "answer": "🤖 I'm here to help! Ask about orders, shipping, returns, or payments.",
        "confidence": "Low",
    }

# ---------------- Get Answer ----------------
def get_answer(query, model, knowledge_base, index):
    try:
        query_embedding = model.encode([query])
        faiss.normalize_L2(query_embedding)

        scores, indices = index.search(query_embedding.astype("float32"), 3)
        best_idx = indices[0][0]
        best_score = scores[0][0]

        if best_score < 0.3:
            return get_fallback(query)

        best_match = knowledge_base[best_idx]

        return {
            "answer": best_match["answer"],
            "confidence": "High" if best_score > 0.7 else "Medium",
        }

    except Exception as e:
        return {"answer": f"⚠️ Error: {str(e)}", "confidence": "Low"}

# ---------------- Main App ----------------
def main():
    st.title("💬 Customer Support Assistant")
    st.markdown("Welcome! Ask me anything about **orders, returns, payments, or shipping.**")

    model, knowledge_base, index = load_system()
    if not all([model, knowledge_base, index]):
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        role, content = message["role"], message["content"]
        if role == "user":
            st.markdown(f"<div style='background:#DCF8C6;padding:10px;border-radius:10px;margin:5px;'>👤 {content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#FFF;border:1px solid #eee;padding:10px;border-radius:10px;margin:5px;'>🤖 {content}</div>", unsafe_allow_html=True)
            if "confidence" in message:
                st.markdown(f"<p style='font-size:12px;color:gray;margin-top:-10px;'>Confidence: {message['confidence']}</p>", unsafe_allow_html=True)

    if prompt := st.chat_input("💡 Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_answer(prompt, model, knowledge_base, index)
        st.session_state.messages.append({"role": "assistant", "content": response["answer"], "confidence": response["confidence"]})
        st.rerun()

if __name__ == "__main__":
    main()
