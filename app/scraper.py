import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import time

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "newsdb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
            )
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) UNIQUE NOT NULL,
            link TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def scrape_tech_news():
    init_db()
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    titles = soup.find_all('span', class_='titleline')
    for item in titles[:10]: # دریافت ۱۰ خبر اول
        a_tag = item.find('a')
        title = a_tag.text
        link = a_tag['href']
        
        cur.execute("""
            INSERT INTO articles (title, link) 
            VALUES (%s, %s) 
            ON CONFLICT (title) DO NOTHING;
        """, (title, link))
        
    conn.commit()
    cur.close()
    conn.close()