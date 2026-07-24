from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_tech_news, get_db_connection
import psycopg2.extras

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scrape")
def trigger_scrape():
    scrape_tech_news()
    return {"message": "Scraping completed and database updated!"}

@app.get("/api/news")
def get_news():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM articles ORDER BY id DESC LIMIT 10;")
    articles = cur.fetchall()
    cur.close()
    conn.close()
    return articles