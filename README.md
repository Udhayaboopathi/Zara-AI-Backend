# Zara AI — Backend API

A production-ready FastAPI backend powering **Zara AI**, an enterprise-grade multi-model AI assistant with chat, document analysis, image generation, diagram rendering, and exam preparation capabilities.

---

## Features

- **Multi-Model AI Routing** — Intelligently routes requests across Gemini, Groq, and OpenRouter based on task type
- **Authentication** — JWT (access + refresh tokens), Google OAuth2, Magic Link, OTP email verification
- **Chat with Memory** — Session-based conversation history with auto-delete privacy controls
- **File Analysis** — PDF, DOCX, Excel, ZIP, image (Gemini Vision) analysis
- **Image Generation** — Stability AI integration
- **Diagram Rendering** — Mermaid diagram generation
- **Reports** — AI-generated report creation
- **Email** — Dual provider support (Brevo SMTP + Resend)
- **Database** — PostgreSQL via SQLAlchemy + Alembic migrations

---

## Tech Stack

| Layer      | Technology                 |
| ---------- | -------------------------- |
| Framework  | FastAPI                    |
| Server     | Gunicorn + Uvicorn workers |
| Database   | PostgreSQL (Neon)          |
| ORM        | SQLAlchemy + Alembic       |
| AI — PRO   | Google Gemini 1.5 Flash    |
| AI — ECO   | OpenRouter                 |
| AI — CODE  | Groq                       |
| Image Gen  | Stability AI               |
| Auth       | JWT + Google OAuth2        |
| Email      | Brevo SMTP / Resend        |
| Deployment | Docker / Render            |

---

## Project Structure

```
app/
├── api/            # Route handlers (auth, users, ai, analysis, diagram, reports, image)
├── core/           # Config, JWT, security
├── email/          # Email providers (Brevo, Resend)
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
└── services/
    ├── models/     # LLM service wrappers (Gemini, Groq, OpenRouter)
    ├── llm_router.py       # Intelligent AI routing logic
    ├── chat_memory.py      # Session memory management
    ├── file_analysis.py    # File parsing and AI analysis
    ├── diagram_service.py  # Mermaid diagram rendering
    └── background_tasks.py # Auto-delete scheduler
alembic/            # Database migrations
```

---

## AI Routing Strategy

| Module           | Primary | Fallback 1 | Fallback 2 |
| ---------------- | ------- | ---------- | ---------- |
| `chat`           | Gemini  | —          | —          |
| `file_analyze`   | Gemini  | —          | —          |
| `tutor`          | Gemini  | Groq       | OpenRouter |
| `exam_prep`      | Gemini  | Groq       | OpenRouter |
| `code_architect` | Groq    | OpenRouter | Gemini     |

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database (or Neon cloud DB)
- API keys (see Environment Variables)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/Udhayaboopathi/Zara-AI-Backend.git
cd Zara-AI-Backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Copy env file and fill in values
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit **`http://localhost:8000/docs`** for the interactive Swagger UI.

---

## Docker

```bash
# Build
docker build -t zara-ai-backend .

# Run
docker run --env-file .env -p 8000:8000 zara-ai-backend
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
# App
PROJECT_NAME="Zara AI"
API_V1_STR=/api/v1
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Google / Gemini
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_CALLBACK_URL=https://yourdomain.com/api/v1/auth/google/callback

# AI Providers
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
STABILITY_API_KEY=your_stability_api_key

# Email — Brevo
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_USER=apikey
BREVO_SMTP_PASS=your_brevo_key

# Email — Resend
RESEND_API_KEY=your_resend_key
EMAILS_FROM_EMAIL=you@example.com
EMAILS_FROM_NAME="Zara AI"

# Frontend
FRONTEND_URL=https://your-frontend.netlify.app
```

---

## API Reference

| Method | Endpoint                                  | Description              |
| ------ | ----------------------------------------- | ------------------------ |
| `GET`  | `/`                                       | Health check             |
| `GET`  | `/docs`                                   | Swagger UI               |
| `POST` | `/api/v1/auth/register`                   | Register with email      |
| `POST` | `/api/v1/auth/login`                      | Login                    |
| `GET`  | `/api/v1/auth/google/login`               | Google OAuth             |
| `POST` | `/api/v1/auth/magic-link`                 | Send magic login link    |
| `GET`  | `/api/v1/users/me`                        | Get current user         |
| `POST` | `/api/v1/ai/chat`                         | Send AI chat message     |
| `POST` | `/api/v1/analysis/analyze_files`          | Upload and analyze files |
| `POST` | `/api/v1/image-generation/generate-image` | Generate image           |
| `POST` | `/api/v1/diagram/render`                  | Render Mermaid diagram   |
| `POST` | `/api/v1/reports/`                        | Generate AI report       |

---

## Deployment

This project is configured to deploy on **Render** using the `Procfile`:

```
web: gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --workers 2 --bind 0.0.0.0:$PORT --timeout 120
```

Set all environment variables in your Render dashboard under **Environment**.

---

## License

MIT — Built by [Mohammed Majeed](https://github.com/majeed74905)
