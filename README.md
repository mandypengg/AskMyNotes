# 📝 AskMyNotes

A local RAG (Retrieval-Augmented Generation) chatbot that lets you upload documents and ask questions about them. Built with LangChain, ChromaDB, HuggingFace embeddings, and Groq's free LLaMA API.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![LangChain](https://img.shields.io/badge/LangChain-latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🧠 How It Works

AskMyNotes uses a RAG (Retrieval-Augmented Generation) pipeline under the hood:

```
1. LOAD      →  Your document is loaded and parsed
2. CHUNK     →  The text is split into small overlapping chunks
3. EMBED     →  Each chunk is converted into a vector (number representation)
4. STORE     →  Vectors are saved in a local ChromaDB database
5. RETRIEVE  →  Your question is matched against the most relevant chunks
6. ANSWER    →  The chunks + your question are sent to LLaMA via Groq for an answer
```

Embeddings run **entirely locally** on your machine via HuggingFace — no data is sent anywhere except your question and relevant context to Groq's API.

---

## ✨ Features

- 📄 **Multi-format support** — Upload PDF, TXT, MD, DOCX, CSV, HTML, JPG, PNG
- 💬 **Chat interface** — Clean conversational UI with full message history
- 🔒 **Privacy-friendly** — Embeddings run locally, only query context hits the API
- 🔄 **Swap documents** — Upload a new file mid-session without restarting
- ⚡ **Fast responses** — Powered by Groq's ultra-fast LLaMA inference
- 🆓 **Completely free** — Uses Groq's free tier and local HuggingFace embeddings

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Framework | [LangChain](https://langchain.com) |
| Embeddings | [HuggingFace sentence-transformers](https://huggingface.co) (local) |
| Vector Store | [ChromaDB](https://trychroma.com) (local) |
| LLM | [LLaMA 3.3 via Groq API](https://groq.com) |
| UI | [Streamlit](https://streamlit.io) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A free [Groq API key](https://console.groq.com)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-chatbot.git
cd rag-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal. You'll need to run this activation command every time you open a new terminal.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ This may take a few minutes the first time — `sentence-transformers` and `torch` are large packages.

### 4. Set Up Your API Key

Create a `.env` file in the root of the project:

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

To get a free Groq API key:
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Click **API Keys** in the left sidebar
4. Click **Create API Key** and copy it

### 5. Run the App

```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501`.

---

## 📖 Usage

1. **Upload a document** using the sidebar on the left
2. **Wait** for the "Ready!" confirmation (processing time depends on document size)
3. **Ask questions** about your document in the chat input at the bottom
4. Use the **Upload New Document** button to switch files

---

## 📁 Project Structure

```
rag-chatbot/
│
├── app.py              # Streamlit UI
├── rag.py              # RAG pipeline logic
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .env                # Your actual API key (never committed to git)
├── .gitignore          # Excludes venv, .env, cache files
└── README.md
```

---

## ⚙️ Supported File Types

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Plain Text | `.txt` |
| Markdown | `.md` |
| Word Document | `.docx` |
| CSV | `.csv` |
| HTML | `.html` |
| Images (OCR) | `.jpg`, `.jpeg`, `.png` |

> 📸 Image support uses OCR (Optical Character Recognition) to extract text from images. Works best on screenshots, scanned documents, and images containing text.

---

## 🔧 Configuration

You can tweak the following settings in `rag.py` to adjust performance:

| Setting | Default | Description |
|---|---|---|
| `chunk_size` | `500` | Max characters per chunk. Larger = more context per chunk |
| `chunk_overlap` | `50` | Characters shared between chunks. Helps avoid cutting answers mid-sentence |
| `k` (retrieval) | `4` | Number of chunks retrieved per question. Higher = more context |
| `model` | `llama-3.3-70b-versatile` | Groq model used for generation |

---

## 🐛 Common Issues

**`ModuleNotFoundError`** — Make sure your virtual environment is activated (`source venv/bin/activate`) before running.

**`GROQ_API_KEY not found`** — Make sure your `.env` file exists in the project root and contains your key.

**Slow first response** — The HuggingFace embedding model downloads on first run (~90MB). Subsequent runs are fast.

**Image files not working** — Make sure Tesseract is installed on your system:
- Mac: `brew install tesseract`
- Windows: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt install tesseract-ocr`

---
