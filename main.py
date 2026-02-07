from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json

from database import get_connection
from utils import parse_operator

app = FastAPI(title="Recipe API")


# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================
# API 1 - Get Recipes
# ===========================

@app.get("/api/recipes")
def get_recipes(page: int = 1, limit: int = 10):

    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor()

    total = cursor.execute(
        "SELECT COUNT(*) FROM recipes"
    ).fetchone()[0]

    query = """
        SELECT * FROM recipes
        ORDER BY rating DESC
        LIMIT ? OFFSET ?
    """

    rows = cursor.execute(query, (limit, offset)).fetchall()

    data = []
    for row in rows:
        recipe = dict(row)

        if recipe["nutrients"]:
            recipe["nutrients"] = json.loads(recipe["nutrients"])
        else:
            recipe["nutrients"] = None

        data.append(recipe)

    conn.close()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": data
    }


# ===========================
# API 2 - Search Recipes
# ===========================

@app.get("/api/recipes/search")
def search_recipes(
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    rating: Optional[str] = None,
    total_time: Optional[str] = None,
    calories: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")

    if cuisine:
        query += " AND cuisine = ?"
        params.append(cuisine)

    if rating:
        op, val = parse_operator(rating)
        query += f" AND rating {op} ?"
        params.append(float(val))

    if total_time:
        op, val = parse_operator(total_time)
        query += f" AND total_time {op} ?"
        params.append(int(val))

    if calories:
        op, val = parse_operator(calories)
        query += f"""
        AND nutrients IS NOT NULL
        AND CAST(
            REPLACE(
                json_extract(nutrients, '$.calories'),
                ' kcal',
                ''
            ) AS INTEGER
        ) {op} ?
        """
        params.append(int(val))

    # ===== COUNT TOTAL =====
    total_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total = cursor.execute(total_query, params).fetchone()[0]

    # ⭐ SORT RESULTS BY RATING
    query += " ORDER BY rating DESC"

    # ===== ADD PAGINATION =====
    offset = (page - 1) * limit
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = cursor.execute(query, params).fetchall()

    data = []
    for row in rows:
        recipe = dict(row)

        if recipe["nutrients"]:
            recipe["nutrients"] = json.loads(recipe["nutrients"])
        else:
            recipe["nutrients"] = None

        data.append(recipe)

    conn.close()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": data
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
