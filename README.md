# Full-Stack Text-to-SQL Application

A seamless, local-first web application that translates natural language questions into executable PostgreSQL queries using the local Ollama LLM (`qwen2.5:3b`). 

## 🚀 Features

- **Local Privacy**: 100% of the AI processing happens locally on your machine via Ollama. No data is sent to external APIs.
- **Automated Schema Awareness**: Automatically extracts the database schema from PostgreSQL to context-feed the LLM for accurate SQL generation.
- **Premium Glassmorphic UI**: Beautiful, modern React frontend built with Vite and TypeScript.
- **Portable Architecture**: Self-contained PostgreSQL and Node.js instances for zero-configuration startup.

## 🛠 Tech Stack

- **Frontend**: React, TypeScript, Vite, Axios, Vanilla CSS (Glassmorphism design)
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Python 3.11
- **Database**: PostgreSQL 16 (Portable)
- **AI/LLM**: Ollama (`qwen2.5:3b` model)

## 📂 Project Structure

```
text2sql-app/
├── backend/          # FastAPI Python server
│   ├── main.py       # API routes and entry point
│   ├── llm.py        # Ollama integration and prompt engineering
│   ├── database.py   # SQLAlchemy connection setup
│   ├── models.py     # Database schema definitions
│   └── setup_db.py   # Script to initialize database and seed dummy data
├── frontend/         # Vite React TypeScript application
│   ├── src/
│   │   ├── App.tsx   # Main application component and chat interface
│   │   └── index.css # Premium UI styles
│   └── package.json  # Node dependencies
├── node/             # Portable Node.js binaries
└── pgsql/            # Portable PostgreSQL cluster and data
```

## 💻 Running the Application

Because this project includes portable versions of the required infrastructure, you do not need to install PostgreSQL or Node.js globally. 

### 1. Start the Backend & Database

Open a terminal and run the backend startup script. This will seed the database if it's empty and start the FastAPI server:

```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload
```
*The API will be available at `http://localhost:8000`*

### 2. Start the Frontend

Open a second terminal, inject the portable Node.js into your PATH, and start the React app:

```powershell
# Add portable Node.js to your terminal's PATH
$env:PATH = "C:\Users\asus\.gemini\antigravity\scratch\text2sql-app\node;" + $env:PATH

cd frontend
npm run dev
```
*The UI will be available at `http://localhost:5173`*

## 🧑‍💻 Usage Example

Once both servers are running, open your browser to the frontend URL and try asking:
- *"Show me all employees in the Engineering department"*
- *"Who has a salary over 70000?"*
- *"List employees whose manager is the CEO"*
