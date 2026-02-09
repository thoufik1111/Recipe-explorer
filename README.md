# Recipe Explorer API

FastAPI backend for Recipe Explorer application.

## Features

- Get paginated recipes
- Search recipes by title, cuisine, rating, time, and calories
- Filter recipes with operators (>=, <=, =)
- JSON response with recipe details and nutrition information

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure `recipes.db` database file is present

3. Run the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Render Deployment

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Environment:**
- Python 3.9+

## API Endpoints

### GET /api/recipes
Get paginated list of recipes

**Query Parameters:**
- `page` (int, default: 1)
- `limit` (int, default: 10)

### GET /api/recipes/search
Search and filter recipes

**Query Parameters:**
- `title` (str): Search by recipe title
- `cuisine` (str): Filter by cuisine type
- `rating` (str): Filter by rating (e.g., ">=4.5")
- `total_time` (str): Filter by cooking time (e.g., "<=60")
- `calories` (str): Filter by calories (e.g., ">=200")
- `page` (int, default: 1)
- `limit` (int, default: 10)

## Database Schema

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuisine TEXT,
    title TEXT,
    rating REAL,
    prep_time INTEGER,
    cook_time INTEGER,
    total_time INTEGER,
    description TEXT,
    nutrients TEXT,
    serves TEXT,
    url TEXT
)
```

## Technologies

- FastAPI
- SQLite3
- Uvicorn
- CORS enabled for frontend integration