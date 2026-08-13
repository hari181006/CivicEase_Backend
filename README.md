# CivicEase Backend

## Setup
1. Create PostgreSQL database `civicease`.
2. Copy `.env.example` to `.env` and update the database password and JWT secret.
3. Install: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload`
5. API docs: http://127.0.0.1:8000/docs

## Database
Run `database/schema.sql` in PostgreSQL if you want to create the complete schema manually.
