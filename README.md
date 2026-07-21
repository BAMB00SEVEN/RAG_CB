# RAG Chatbot (FastAPI + FAISS + Groq)

A beginner-friendly, production-structured **Retrieval-Augmented Generation (RAG) chatbot**.

- Answers questions using documents in `data/docs/` (sample demo docs included)
- Free & fast LLM via **Groq** (Llama 3 models)
- Free local embeddings via **sentence-transformers** (no API key needed for this part)
- **FAISS** vector database for retrieval
- **SQLite** database to log every question + answer
- Simple HTML/JS chat UI
- Deploys free on **Render**

---

## 1. Project Structure

```
rag-chatbot/
├── app/
│   ├── main.py              # FastAPI app (starts server, serves UI, routes)
│   ├── config.py            # Reads settings from environment variables
│   ├── database.py          # SQLite database connection + table setup
│   ├── models.py            # Request/response data shapes (Pydantic)
│   ├── rag/
│   │   ├── embeddings.py    # Converts text -> vectors
│   │   ├── vector_store.py  # Builds/loads/searches the FAISS index
│   │   ├── retriever.py     # Finds the most relevant chunks for a question
│   │   └── generator.py     # Calls Groq LLM to generate the final answer
│   ├── routers/
│   │   └── chat.py          # /api/chat and /api/history endpoints
│   └── utils/
│       └── text_splitter.py # Splits long documents into small chunks
├── data/
│   ├── docs/                # Knowledge base documents (.txt files)
│   └── faiss_index/         # Auto-generated vector index (created by script)
├── scripts/
│   └── build_index.py       # Run this whenever you add/change documents
├── static/
│   ├── index.html           # Chat UI
│   ├── style.css
│   └── script.js
├── tests/
│   └── test_chat.py
├── requirements.txt
├── .env.example
├── .gitignore
└── render.yaml               # Render deployment blueprint
```

---

## 2. How It Works (in plain English)

1. Documents live in `data/docs/` as `.txt` files (a few demo ones are already there).
2. `scripts/build_index.py` chops them into small overlapping chunks and converts each chunk
   into a vector (a list of numbers representing its meaning) using `sentence-transformers`.
   These vectors are stored in a FAISS index — a fast, searchable vector database, saved to disk.
3. When a user asks a question in the chat UI:
   - The question is converted into a vector the same way.
   - FAISS finds the most similar chunks from the documents (**Retrieval**).
   - Those chunks + the question are sent to Groq's Llama model, which writes a natural
     language answer using ONLY that retrieved context (**Generation**).
   - The question + answer are saved into `qna.db` (SQLite) for logging/history.
4. The answer is shown in the chat UI, along with which source chunks were used.

---

## 3. Run It Locally (Step by Step)

### Step 3.1 — Install Python
Python 3.10+ required. Check with:
```bash
python --version
```

### Step 3.2 — Get a FREE Groq API key
1. Go to https://console.groq.com
2. Sign up (free, no credit card).
3. Go to **API Keys** → **Create API Key** → copy it somewhere safe.

### Step 3.3 — Set up the project
```bash
cd rag-chatbot
python -m venv venv

# Activate venv:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3.4 — Add your Groq key
```bash
cp .env.example .env
```
Open `.env` in any text editor and paste your key:
```
GROQ_API_KEY=your_key_here
```

### Step 3.5 — Build the knowledge base index
(Sample docs are already included in `data/docs/` so you can test immediately.)
```bash
python scripts/build_index.py
```
You should see something like: `Index built: 24 chunks from 4 documents`

### Step 3.6 — Run the server
```bash
uvicorn app.main:app --reload
```
Open your browser at: **http://127.0.0.1:8000**

Try asking: *"What is RAG?"* or *"How does photosynthesis work?"* (based on the sample docs).

### Step 3.7 — Use your own documents
1. Delete or keep the sample `.txt` files in `data/docs/`.
2. Add your own `.txt` files there (convert PDFs/Word docs to `.txt` first).
3. Re-run `python scripts/build_index.py` every time you change the documents.
4. Restart the server.

---

## 4. Push the Project to GitHub

```bash
cd rag-chatbot
git init
git add .
git commit -m "Initial commit: RAG chatbot project"
```

1. Go to https://github.com/new
2. Create a new repository (e.g. `rag-chatbot`). **Do not** initialize it with a README/gitignore
   (we already have our own).
3. Copy the commands GitHub shows you under "…or push an existing repository", they'll look like:
```bash
git remote add origin https://github.com/YOUR_USERNAME/rag-chatbot.git
git branch -M main
git push -u origin main
```

⚠️ Your `.env` file (with your secret API key) is **never** pushed — it's excluded via `.gitignore`.

---

## 5. Deploy on Render (Step by Step)

### Step 5.1 — Create a Render account
Go to https://render.com → sign up (free) → connect your GitHub account.

### Step 5.2 — Create a new Web Service
1. Dashboard → **New** → **Web Service**
2. Select your `rag-chatbot` GitHub repo
3. Fill in:
   - **Name**: `rag-chatbot` (or anything)
   - **Region**: closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```
     pip install -r requirements.txt && python scripts/build_index.py
     ```
   - **Start Command**:
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: Free

   (Alternatively, if `render.yaml` is detected, Render can auto-fill all of this for you —
   just click "Apply" when prompted.)

### Step 5.3 — Add your environment variable
Under **Environment** (same page, or after creation):
- Key: `GROQ_API_KEY`
- Value: *your Groq key*

### Step 5.4 — Deploy
Click **Create Web Service**. Render installs dependencies, builds the FAISS index, and starts
the server. Wait for "Live" status (~3-6 min the first time — downloading the embedding model
takes a little while).

Your chatbot is now live at:
`https://rag-chatbot-xxxx.onrender.com`

### Step 5.5 — Updating later
Every `git push` to `main` triggers an automatic redeploy on Render.

> ⚠️ **Free tier notes**:
> - The service spins down after ~15 min of inactivity; the next request wakes it up (~30-50s cold start).
> - Disk is **ephemeral** — `qna.db` (Q&A history) and the FAISS index reset on every redeploy/restart.
>   The index rebuilds automatically via the Build Command. If you need permanent Q&A history,
>   swap SQLite for Render's free PostgreSQL later (optional — not needed to get this working).

---

## 6. Testing
```bash
pytest tests/
```

## 7. Tech Stack Summary
| Piece | Tool | Cost |
|---|---|---|
| Backend API | FastAPI | Free |
| Embeddings | sentence-transformers (local) | Free |
| Vector DB | FAISS (local file) | Free |
| LLM | Groq (Llama 3) | Free tier |
| Database | SQLite | Free |
| Hosting | Render | Free tier |

## 8. Common Issues
- **"GROQ_API_KEY not set"** → check your `.env` file locally, or Render's Environment tab in production.
- **Chatbot gives generic/wrong/"I don't know" answers** → your `data/docs/` may not contain
  relevant info for that question, or you forgot to re-run `build_index.py` after adding docs.
- **Render deploy fails on build** → open the "Logs" tab; usually a missing package in `requirements.txt`
  or the build timing out (retry — first build downloads a ~90MB embedding model).
- **`ModuleNotFoundError` locally** → make sure your virtual environment is activated before
  running `pip install` and `uvicorn`.
