import streamlit as st
import pdfplumber
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

# =========================
# LOAD GEMINI API
# =========================
load_dotenv()

# Check if API key exists
if not os.getenv("GOOGLE_API_KEY"):
    st.error("⚠️ GOOGLE_API_KEY not found in .env file")
    st.stop()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SmartDoc Assistant",
    page_icon="📚",
    layout="wide"
)

# =========================
# CUSTOM CSS - GOLDEN/BLACK THEME
# =========================
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    color: white !important;
}

/* Global Text */
html, body, [class*="css"] {
    color: #E0E0E0 !important;
}

/* Headers - Golden */
h1, h2, h3, h4, h5, h6 {
    color: #FFD700 !important;
}

/* Title Glow */
.glow-text {
    color: #FFD700;
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    text-shadow: 0 0 10px #FFD700,
                 0 0 20px #FFA500,
                 0 0 30px #FF4500;
}

/* Sidebar - Dark Golden */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a0a 0%, #1a0a0a 100%);
    border-right: 2px solid #FFD700;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: #E0E0E0 !important;
}

/* ========================================== */
/* FILE UPLOADER - GREY BACKGROUND           */
/* ========================================== */

/* File Uploader Container - Grey */
[data-testid="stFileUploader"] {
    background: #2a2a2a !important;
    border: 2px dashed #FFD700 !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin-bottom: 15px !important;
}

/* File Uploader Label - Golden */
[data-testid="stFileUploader"] label {
    color: #FFD700 !important;
    font-weight: bold !important;
    font-size: 16px !important;
}

/* Drag & Drop Text */
[data-testid="stFileUploader"] p {
    color: #CCCCCC !important;
    font-size: 14px !important;
}

/* Helper text */
[data-testid="stFileUploader"] small {
    color: #999999 !important;
}

/* File name - Golden */
[data-testid="stFileUploaderFileName"] {
    color: #FFD700 !important;
    font-weight: bold !important;
    background: #3a3a3a !important;
    padding: 5px 10px !important;
    border-radius: 8px !important;
}

/* File list container */
[data-testid="stFileUploader"] ul {
    background: #2a2a2a !important;
    padding: 10px !important;
    border-radius: 10px !important;
}

/* Each file row */
[data-testid="stFileUploader"] li {
    color: #FFD700 !important;
    background: #353535 !important;
    margin: 5px 0 !important;
    padding: 8px !important;
    border-radius: 8px !important;
}

/* File name text */
[data-testid="stFileUploader"] li span {
    color: #FFD700 !important;
    font-weight: 600 !important;
}

/* File size text */
[data-testid="stFileUploader"] li small {
    color: #AAAAAA !important;
}

/* Browse button */
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #8B6914, #FFD700) !important;
    color: black !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    border: none !important;
    padding: 8px 20px !important;
}

[data-testid="stFileUploader"] button:hover {
    transform: scale(1.02) !important;
    background: linear-gradient(135deg, #A0791A, #FFE44D) !important;
}

/* Remove file button */
[data-testid="stFileUploader"] button[aria-label="Remove"] {
    background: #8B0000 !important;
    color: white !important;
}

/* ========================================== */
/* INPUT FIELD - Golden Border               */
/* ========================================== */
.stTextInput input {
    background-color: #1a1a1a !important;
    color: #FFD700 !important;
    border: 2px solid #FFD700 !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 16px !important;
}

/* Input Placeholder */
.stTextInput input::placeholder {
    color: #888888 !important;
}

/* ========================================== */
/* BUTTONS - Golden Gradient                 */
/* ========================================== */
.stButton button {
    background: linear-gradient(135deg, #8B6914, #FFD700) !important;
    color: black !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 12px 25px !important;
    font-weight: bold !important;
    transition: 0.3s;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
}

.stButton button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #A0791A, #FFE44D) !important;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
}

/* ========================================== */
/* ANSWER BOX - Golden Border                */
/* ========================================== */
.answer-box {
    background: linear-gradient(135deg, #111111, #1a1a1a);
    border: 2px solid #FFD700;
    border-radius: 15px;
    padding: 25px;
    margin-top: 20px;
    color: white !important;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
}

/* Labels - Golden */
label {
    color: #FFD700 !important;
    font-weight: bold;
}

/* Success/Warning/Info boxes */
.stSuccess {
    background-color: #1a3a1a !important;
    color: #90EE90 !important;
    border-radius: 12px !important;
}

.stWarning {
    background-color: #3a2a1a !important;
    color: #FFD700 !important;
    border-radius: 12px !important;
}

.stError {
    background-color: #3a1a1a !important;
    color: #FF6B6B !important;
    border-radius: 12px !important;
}

.stInfo {
    background-color: #1a2a3a !important;
    color: #87CEEB !important;
    border-radius: 12px !important;
}

/* Progress Bar - Golden */
.stProgress > div > div {
    background-color: #FFD700 !important;
}

/* Scrollbar - Golden */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(#8B6914, #FFD700);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #FFD700;
}

/* Divider */
hr {
    border-color: #FFD700 !important;
    opacity: 0.3;
}

/* Code blocks */
code {
    background-color: #2a2a2a !important;
    color: #FFD700 !important;
    border-radius: 5px;
    padding: 2px 5px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# PDF TEXT EXTRACTION
# =========================
def get_pdf_text(pdf_docs):
    text = ""
    progress_bar = st.progress(0)

    for i, pdf in enumerate(pdf_docs):
        try:
            with pdfplumber.open(pdf) as pdf_reader:
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            progress_bar.progress((i + 1) / len(pdf_docs))
        except Exception as e:
            st.warning(f"⚠️ Error in {pdf.name}: {e}")

    progress_bar.empty()
    return text

# =========================
# TEXT CHUNKING
# =========================
def chunk_text(text, chunk_size=3000):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        current_size += len(sentence)
        if current_size > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_size = len(sentence)
        else:
            current_chunk.append(sentence)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# =========================
# GEMINI AI - UPDATED MODEL
# =========================
def ask_gemini(question, context):
    try:
        # ✅ FIXED: Using correct model name
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a helpful PDF assistant.

        Answer ONLY from the given context.

        If answer is not available, say:
        "Answer not available in the PDF."

        CONTEXT:
        {context[:15000]}

        QUESTION:
        {question}

        ANSWER:
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"

# =========================
# MAIN APP
# =========================
def main():
    # TITLE
    st.markdown(
        '<h1 class="glow-text">📚 SmartDoc Assistant 🤖</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center; color:#FFD700;'>Chat with your PDF Documents using Gemini AI</h3>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # SESSION STATE
    if "chunks" not in st.session_state:
        st.session_state.chunks = []

    # QUESTION INPUT
    user_question = st.text_input(
        "💬 Ask a Question",
        placeholder="e.g., What is this PDF about? Summarize the document."
    )

    # SIDEBAR
    with st.sidebar:
        st.markdown("## 📂 Document Manager")
        st.markdown("---")

        pdf_docs = st.file_uploader(
            "📎 Upload PDF Files",
            type=["pdf"],
            accept_multiple_files=True
        )

        if pdf_docs:
            st.success(f"✅ {len(pdf_docs)} PDF(s) selected")
            
            # Show file names
            st.markdown("**📄 Selected Files:**")
            for pdf in pdf_docs:
                st.markdown(f"- `{pdf.name}` ({(pdf.size/1024):.1f} KB)")

        st.markdown("---")

        if st.button("🔥 PROCESS PDFs", use_container_width=True):
            if pdf_docs:
                with st.spinner("📖 Reading PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                with st.spinner("✂️ Creating Chunks..."):
                    st.session_state.chunks = chunk_text(raw_text)
                st.success("✅ PDFs Processed Successfully!")
                st.balloons()
            else:
                st.warning("⚠️ Please upload PDF files first")

        st.markdown("---")

        if st.session_state.chunks:
            st.info(f"📄 **Total Chunks:** {len(st.session_state.chunks)}")
            
            # Show sample chunk
            with st.expander("🔍 View Sample Text"):
                st.write(st.session_state.chunks[0][:500] + "...")

    # QUESTION ANSWERING
    if user_question:
        if st.session_state.chunks:
            with st.spinner("🔍 Searching for relevant content..."):
                relevant_chunks = []
                for chunk in st.session_state.chunks:
                    if any(word.lower() in chunk.lower() for word in user_question.split()):
                        relevant_chunks.append(chunk)

                if not relevant_chunks:
                    relevant_chunks = st.session_state.chunks[:3]

                context = " ".join(relevant_chunks[:3])

            with st.spinner("🤖 Gemini is thinking..."):
                answer = ask_gemini(user_question, context)

            st.markdown("## 💡 Answer")

            st.markdown(
                f"""
                <div class="answer-box">
                <h4>❓ Your Question</h4>
                <p style="color:#FFD700; font-size:18px;">
                {user_question}
                </p>
                <hr style="margin: 15px 0;">
                <h4>✨ Gemini's Answer</h4>
                <p style="color:white; font-size:16px; line-height:1.6;">
                {answer}
                </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Please upload and process PDFs first before asking questions.")

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    main()

