# 🧠 PrepMind

> **AI-powered mock interview preparation for top tech companies.**
> Research companies, generate tailored questions, run real-time interviews, and get a detailed performance report — all from a single dashboard.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contributing)

---

## 🎬 Demo

> _Drop a GIF or screenshot here_

```
[ demo.gif — show: upload JD → research → generate questions → live interview → report ]
```

---

## ✨ Features

- 🔍 **Live company research** — Tavily web search + Groq synthesis pulls fresh, role-specific intel.
- 🧩 **RAG-powered question generation** — ChromaDB-backed bank of 60+ curated questions, tailored to the JD *and* the candidate's resume.
- 💬 **Real-time WebSocket interview** — answer, ask for hints, or request the full reveal — the AI adapts.
- 📊 **Automatic scoring** (0–10 per question) with detailed feedback and encouragement.
- 📈 **Final performance report** — strengths, weaknesses, topic breakdown, and a 7-day study plan.
- 📄 **Resume parsing** — drop a PDF or paste text; the system uses it to personalize every question.
- 🔁 **Resume-anywhere interviews** — disconnect and reconnect; your progress is persisted.
- 🌱 **Self-improving vector DB** — every new question added to ChromaDB improves future generations.
- 🔐 **JWT auth + bcrypt** password hashing.
- 🖥️ **Single-file frontend** — zero build step, served straight from FastAPI.

---

## 🏗️ Architecture

```
                                ┌────────────────────────┐
                                │   Frontend (HTML/JS)   │
                                │  Tailwind • WebSocket  │
                                └───────────┬────────────┘
                                            │ REST + WS
                                ┌───────────▼────────────┐
                                │      FastAPI App       │
                                │      (app/main.py)     │
                                └───────────┬────────────┘
        ┌──────────────┬─────────────┬──────┴──────┬────────────────┬─────────────┐
        ▼              ▼             ▼             ▼                ▼             ▼
  ┌──────────┐  ┌────────────┐ ┌─────────────┐ ┌──────────┐ ┌────────────┐  ┌──────────┐
  │   Auth   │  │  JD Mgmt   │ │  Research   │ │ Question │ │ Interview  │  │  Report  │
  │  (JWT)   │  │            │ │   Agent     │ │   Agent  │ │   Agent    │  │  Agent   │
  └────┬─────┘  └─────┬──────┘ └──────┬──────┘ └─────┬────┘ └──────┬─────┘  └────┬─────┘
       │              │               │              │              │             │
       │              │               ▼              ▼              │             │
       │              │        ┌──────────┐    ┌──────────┐         │             │
       │              │        │  Tavily  │    │ ChromaDB │         │             │
       │              │        │  Search  │    │   (RAG)  │         │             │
       │              │        └────┬─────┘    └─────┬────┘         │             │
       │              │             └─────┬──────────┘              │             │
       │              │                   ▼                         ▼             │
       │              │           ┌────────────────────────────────────┐          │
       │              │           │     Groq • llama-3.3-70b           │          │
       │              │           └────────────────────────────────────┘          │
       └──────────────┴────────────────────────┬────────────────────────────────-─┘
                                               ▼
                                  ┌────────────────────────┐
                                  │  PostgreSQL (8 tables) │
                                  │  + Redis cache         │
                                  └────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer            | Technology                                        |
| ---------------- | ------------------------------------------------- |
| **Backend**      | FastAPI (Python 3.9+)                             |
| **Database**     | PostgreSQL + SQLAlchemy ORM                       |
| **Migrations**   | Alembic                                           |
| **Auth**         | JWT (HS256) + bcrypt                              |
| **LLM**          | Groq — `llama-3.3-70b-versatile`                  |
| **Web Search**   | Tavily API                                        |
| **Vector DB**    | ChromaDB (persistent)                             |
| **Embeddings**   | `sentence-transformers/all-MiniLM-L6-v2`          |
| **Real-time**    | WebSockets (FastAPI)                              |
| **Resume**       | `pdfplumber`                                      |
| **Cache**        | Redis                                             |
| **Frontend**     | Single-file HTML + Tailwind (CDN) + vanilla JS    |

---

## 📦 Prerequisites

- **Python 3.9+**
- **PostgreSQL 14+**
- **Redis** (running locally on default port)
- **Node.js** (optional — for `wscat` WebSocket testing)
- API keys for **Groq** and **Tavily**

---

## 🚀 Installation

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/prepmind.git
cd prepmind
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the database
```bash
createdb prepmind
```

### 5. Configure environment variables
Create a `.env` file in the project root (see [table below](#-environment-variables)).

### 6. Run migrations
```bash
alembic upgrade head
```

### 7. Seed the question bank into ChromaDB
```bash
python -m app.rag.seeder
```

### 8. Start the server
```bash
uvicorn app.main:app --reload
```

Open **http://localhost:8000** — the frontend is served directly. 🎉

---

## 🔑 Environment Variables

| Variable                       | Description                                      | Example                              |
| ------------------------------ | ------------------------------------------------ | ------------------------------------ |
| `DATABASE_URL`                 | PostgreSQL connection string                     | `postgresql://localhost/prepmind`    |
| `SECRET_KEY`                   | JWT signing secret (use a long random string)    | `openssl rand -hex 32`               |
| `ALGORITHM`                    | JWT algorithm                                    | `HS256`                              |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | Token lifetime in minutes                        | `30`                                 |
| `GROQ_API_KEY`                 | Groq API key for the LLM                         | `gsk_...`                            |
| `TAVILY_API_KEY`               | Tavily API key for web search                    | `tvly-...`                           |

---

## 🌐 API Endpoints

| Method | Endpoint                              | Purpose                                  |
| ------ | ------------------------------------- | ---------------------------------------- |
| POST   | `/auth/register`                      | Create a new account                     |
| POST   | `/auth/login`                         | Get a JWT access token                   |
| GET    | `/auth/me`                            | Current user                             |
| POST   | `/resume/upload`                      | Upload resume (PDF or text)              |
| GET    | `/resume`                             | Get parsed resume                        |
| POST   | `/jd/upload`                          | Save a job description                   |
| GET    | `/jd/list`                            | List the user's JDs                      |
| GET    | `/jd/{id}`                            | Fetch a single JD                        |
| DELETE | `/jd/{id}`                            | Delete a JD (cascades children)          |
| POST   | `/research/company`                   | Run company research for a JD            |
| POST   | `/questions/generate`                 | Generate tailored interview questions    |
| GET    | `/questions/list`                     | List generated questions                 |
| POST   | `/interview/start`                    | Start a new interview session            |
| WS     | `/interview/chat/{session_id}`        | Real-time interview channel              |
| POST   | `/evaluation/report/{session_id}`     | Generate the final performance report    |

---

## 🔄 How It Works

### Phase 1 — Onboarding
Register, sign in, and upload your resume. The resume is parsed once and reused throughout.

### Phase 2 — Job Description
Paste a JD (company, role, full text). It's stored under your account and used as the spine of every downstream agent.

### Phase 3 — Company Research
The **Research Agent** queries Tavily for current articles, blog posts, and engineering content about the company, then asks Groq to synthesize a structured brief: tech stack, culture, interview process, and prep tips.

### Phase 4 — Question Generation
The **Question Agent** runs a RAG lookup against ChromaDB's curated bank, blends in the JD + resume + research, and asks Groq to produce 15 personalized questions across the categories below.

### Phase 5 — Live Interview
Open a WebSocket to `/interview/chat/{session_id}`. The **Interview Agent** asks one question at a time. You can:
- **Answer** it — get a 0–10 score and detailed feedback.
- **Ask a hint** — stay on the same question with a nudge.
- **Request a reveal** — see the ideal answer and move on.

Every answer is persisted, so you can disconnect and pick up where you left off.

### Phase 6 — Report
Hit **"End & get report"**. The **Evaluation Agent** computes overall score, strengths, weaknesses, per-topic breakdown, and a 7-day study plan tailored to your weak areas.

---

## 📁 Project Structure

```
prepmind/
├── app/
│   ├── auth/              # JWT authentication
│   ├── jd/                # Job description CRUD
│   ├── research/          # Company research agent (Tavily + Groq)
│   ├── questions/         # Question generation agent (RAG + Groq)
│   ├── interview/         # Real-time interview WebSocket + agent
│   ├── evaluation/        # Performance evaluation agent
│   ├── resume/            # Resume parsing (pdfplumber)
│   ├── rag/               # ChromaDB client, embedder, seeder
│   ├── models.py          # 8 SQLAlchemy tables
│   ├── database.py        # DB engine + session
│   └── main.py            # FastAPI app + frontend mount
├── frontend/
│   └── index.html         # Single-file dashboard (Tailwind + vanilla JS)
├── alembic/               # DB migrations
├── chroma_db/             # Persistent vector store (gitignored)
├── requirements.txt
└── README.md
```

---

## 🤖 Multi-Agent Architecture

PrepMind is built around **four specialized AI agents**, each with a single responsibility:

| Agent              | Inputs                                  | Outputs                                            | Stack                |
| ------------------ | --------------------------------------- | -------------------------------------------------- | -------------------- |
| **Research Agent** | Company name, role, JD                  | Tech stack, culture, interview process, tips       | Tavily + Groq        |
| **Question Agent** | JD, research brief, resume              | 15 categorized questions w/ hints + ideal answers  | ChromaDB (RAG) + Groq|
| **Interview Agent**| One question + the candidate's message  | `{type, score, feedback, encouragement, next}`     | Groq (per-turn)      |
| **Evaluation Agent**| All answers + scores                   | Strengths, weaknesses, topic breakdown, study plan | Groq                 |

The agents are stateless and composable — every interaction is reproducible from the data in PostgreSQL + ChromaDB.

---

## 🔬 RAG System

The Question Agent is **retrieval-augmented**:

1. **Seed set** — `app/rag/seeder.py` loads a curated bank of 60+ canonical questions into ChromaDB, embedded with `sentence-transformers/all-MiniLM-L6-v2`.
2. **Retrieve** — given the JD + role + tech stack, we pull the top-N most semantically similar questions from the bank.
3. **Generate** — Groq receives the retrieved questions as context and generates 15 *new* questions tailored to the candidate.
4. **Self-improve** — newly generated questions are added back to ChromaDB, so the bank grows with every interview.

### Question categories
| Category           | Count |
| ------------------ | ----- |
| DSA (algorithms / data structures) | 5 |
| System Design      | 4 |
| CS Fundamentals (OS / networking / DB) | 3 |
| Behavioural        | 2 |
| Language-Specific  | 1 |

---

## 🧠 Evaluation Response Types

The Interview Agent returns a typed JSON envelope on every turn:

| `type`     | Meaning                                              | Effect                              |
| ---------- | ---------------------------------------------------- | ----------------------------------- |
| `answer`   | Candidate answered the question                      | Score 0–10 + feedback, advance      |
| `question` | Candidate asked for a hint or clarification          | Hint returned, stay on question     |
| `reveal`   | Candidate explicitly asked for the full answer       | Show ideal answer, no score, advance|
| `complete` | All questions done                                   | Final stats + score                 |

---

## 🗄️ Database Schema (8 Tables)

| Table                  | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| `users`                | Authentication                                |
| `job_descriptions`     | Saved JDs per user                            |
| `company_research`     | Cached AI research per JD                     |
| `interview_questions`  | Generated questions per JD                    |
| `interview_sessions`   | Active / completed interview runs             |
| `interview_answers`    | Per-question answers + scores + feedback      |
| `interview_reports`    | Final aggregated reports                      |
| `resumes`              | Parsed resume content                         |

---

## 🧪 Running the Project

```bash
# Backend (auto-reload during development)
uvicorn app.main:app --reload

# Then open the dashboard
open http://localhost:8000
```

For WebSocket testing:
```bash
npm i -g wscat
wscat -c "ws://localhost:8000/interview/chat/<session_id>"
```

---

## 🤝 Contributing

PRs welcome! For substantial changes please open an issue first to discuss the direction.

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/amazing-thing`)
3. Commit with a clear message
4. Open a PR against `main`

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Shikhar Pandav**

- GitHub: [@Winger47](https://github.com/Winger47)
- LinkedIn: [linkedin.com/in/shikharpandav](https://linkedin.com/in/shikharpandav)

---

> _Built with ☕, ⚡, and a stubborn refusal to bomb another system design round._
