# AI Career Assistant Chatbot

## Overview
AI Career Assistant is a web-based application designed to help users with career planning and preparation through AI-powered assistance. It brings career guidance, resume review, and interview preparation features together in one platform.

## Features
- **Career Guidance:** Assist users with career-related questions and planning.
- **Resume Review:** Help users review their resumes.
- **Interview Preparation:** Support interview practice and preparation.
- **Chatbot Interface:** Provide an interactive interface for career-related assistance.

## Tech Stack
- Python
- Flask
- HTML
- CSS
- JavaScript
- Google Gemini API
- SQLite

## Project Structure
- `app.py` — Application entry point
- `routes/` — Application routes
- `models/` — Data models
- `services/` — AI and resume-related services
- `templates/` — HTML templates
- `static/` — CSS, JavaScript, and image assets
- `database/` — Database-related code

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/hari10ni/career-assistant-ai.git
cd career-assistant-ai
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

Activate it on Windows:
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file and add the required environment variables, including your Gemini API key, using the variable names expected by the application. Never upload your actual API key.

### 5. Run the application
```bash
python app.py
```

Open the local URL printed in the terminal.

## Security
API keys, uploaded documents, and local database files should not be committed to the repository.

## Author
Harini
