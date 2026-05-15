# 🧠 LLM RAG Platform

**Production-Ready Retrieval-Augmented Generation (RAG) System with Authentication, RBAC, and Document Intelligence**

---

## 🚀 Overview

This project is a backend system that implements a **Retrieval-Augmented Generation (RAG) pipeline** using modern backend engineering practices.

It allows authenticated users to:

* Ask questions to an AI system
* Retrieve answers grounded in uploaded documents
* Manage documents securely via admin controls
* Track query history with pagination and filtering

---

## 🎯 Key Features

### 🔐 Authentication & Security

* JWT-based authentication (Access + Refresh tokens)
* HttpOnly cookie-based refresh tokens
* Role-Based Access Control (RBAC)

  * `user` → query system
  * `admin` → upload documents & manage system
* Password hashing with bcrypt
* IP-based rate limiting

---

### 🧠 RAG Pipeline

* Language detection (EN, RU, ZH)
* Document ingestion (PDF, DOCX, TXT)
* Text chunking & embedding
* Vector search using FAISS
* Context-aware LLM responses (Ollama)
* Confidence scoring
* Source tracking

---

### 📄 Document Management

* Admin-only document upload
* File parsing: PDF, DOCX, TXT
* Metadata storage
* Automatic embedding + indexing

---

### 📊 Query System

* Ask AI questions via API
* Automatic fallback when no documents exist
* Query history storage
* Pagination & filtering

---

### ⚙️ Backend Engineering Features

* FastAPI (async high-performance API)
* SQLAlchemy ORM
* PostgreSQL database
* Modular architecture
* API versioning (`/api/v1`)
* Structured logging

---

## 🏗️ System Architecture

```
Client (Swagger / Postman)
        ↓
FastAPI (API Layer)
        ↓
Service Layer (Auth, RAG, Ingestion)
        ↓
PostgreSQL + FAISS
        ↓
LLM (Ollama - Local Model)
```

---

## 🧱 Tech Stack

### Backend

* FastAPI
* Python 3.11
* SQLAlchemy
* Pydantic

### Database

* PostgreSQL

### Machine Learning / RAG

* FAISS
* Sentence Transformers
* Ollama

### Security

* JWT (`python-jose`)
* bcrypt (`passlib`)

### Dev Tools

* Uvicorn
* Git & GitHub
* PyCharm / VS Code

---

## 📂 Project Structure

```
app/
├── api/v1/
├── core/
├── models/
├── schemas/
├── services/
├── db/
└── utils/
```

---

## ⚡ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/Eugenia20/retrieval-augmented-generation-pipeline.git
cd retrieval-augmented-generation-pipeline
```

### 2. Create virtual environment

```
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db
SECRET_KEY=your_secret_key

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

### 5. Run the server

```
uvicorn app.main:app --reload
```

---

### 6. Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 🔑 API Endpoints

### Authentication

* POST /api/v1/auth/register
* POST /api/v1/auth/login
* POST /api/v1/auth/refresh
* POST /api/v1/auth/logout

### RAG

* POST /api/v1/rag/query
* GET /api/v1/rag/history

### Admin

* POST /api/v1/rag/upload
* GET /api/v1/admin/users

---

## 🤖 RAG Behavior

| Scenario        | Behavior              |
| --------------- | --------------------- |
| No documents    | LLM fallback response |
| Documents exist | Context-aware answers |

---

## 🛡️ Security Features

* JWT authentication
* HttpOnly cookies
* RBAC
* Rate limiting
* Password hashing

---

## 📈 Future Improvements

* Frontend (React)
* Docker & Docker Compose
* CI/CD pipeline
* Monitoring & observability
* Advanced evaluation metrics

---

## 👨‍💻 Author
Wakama Eugenia 
Backend Engineer | ML Systems | API Development

---

## ⭐ Final Note

This project demonstrates:

* Real-world backend architecture
* Secure authentication design
* Applied machine learning integration
* Production-level API development
