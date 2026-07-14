# SmartDoc_AI
# 📚 SmartDoc Assistant

An AI-powered PDF Question Answering application built with **Streamlit**, **Google Gemini AI**, and **pdfplumber**. Upload one or multiple PDF files and ask questions in natural language to get accurate answers based on the uploaded documents.

---

## ✨ Features

- 📄 Upload multiple PDF documents
- 🤖 AI-powered question answering using Google Gemini
- 🔍 Extracts text from PDFs
- ✂️ Automatic text chunking for better context
- ⚡ Fast and interactive Streamlit interface
- 🎨 Premium Black & Gold UI
- 📊 Progress bar while processing PDFs
- 📚 Multiple PDF support
- 💬 Chat with your documents

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- pdfplumber
- python-dotenv
- Regular Expressions (re)

---

## 📂 Project Structure

```
SmartDoc-Assistant/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
├── assets/
│   ├── home.png
│   ├── upload.png
│   ├── answer.png
│   └── processing.png
└── screenshots/
    ├── home.png
    ├── upload.png
    ├── answer.png
```

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/SmartDoc-Assistant.git
```

```bash
cd SmartDoc-Assistant
```

### Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup API Key

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

> **Important:** Never upload your API key to GitHub.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

## 🚀 How It Works

1. Upload one or more PDF files.
2. Click **Process PDFs**.
3. The application extracts text from PDFs.
4. Text is divided into chunks.
5. Relevant chunks are selected based on the user's question.
6. Google Gemini generates an answer using the extracted context.
7. The answer is displayed in an attractive UI.

---

## 📦 Required Libraries

```
streamlit
google-generativeai
pdfplumber
python-dotenv
```

Or install using

```bash
pip install -r requirements.txt
```

## 💡 Future Improvements

- Chat history
- Vector Database (FAISS)
- Semantic Search
- OCR Support
- Multiple AI Models
- Export Chat
- Dark/Light Theme Toggle


## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!  

