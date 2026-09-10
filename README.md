# Python Tech News Scraper & Aggregator

A multi-container web application that scrapes tech news headlines, stores them in **PostgreSQL**, and serves them through a **FastAPI** backend and a lightweight static frontend.

---

## 🚀 Features

- Scrapes the top 10 headlines from [Hacker News](https://news.ycombinator.com/)
- Stores articles in PostgreSQL, deduplicated by title (`ON CONFLICT DO NOTHING`)
- REST API (FastAPI) to trigger a scrape and fetch the latest stored articles
- Minimal static frontend (HTML/CSS/JS) served via Nginx, with a "Refresh News" button

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Web Scraping:** BeautifulSoup4 & Requests
- **API Framework:** FastAPI (served with Uvicorn)
- **Database:** PostgreSQL 15 (Alpine)
- **Frontend:** Static HTML/CSS/JS served by Nginx (Alpine)
- **Orchestration:** Docker & Docker Compose

---

## 📦 Getting Started

### Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

### Installation & Running

1. **Clone the repository:**

```bash
git clone https://github.com/sina-mansouri/python-news-scraper.git
cd python-news-scraper
```

2. **Build and start all containers:**

```bash
docker compose up -d --build
```

This starts three containers:

| Service    | Container name  | Host port | Purpose                  |
|------------|------------------|-----------|---------------------------|
| `api`      | `news_api`       | `8000`    | FastAPI backend           |
| `db`       | `news_db`        | `5432`    | PostgreSQL database       |
| `frontend` | `news_frontend`  | `8081`    | Static web UI (Nginx)     |

3. **Open the frontend:**

```
http://localhost:8081
```

Click **"Refresh News"** to trigger a scrape and load the latest headlines.

---

## 🔌 API Endpoints

| Method | Endpoint      | Description                                                        |
|--------|---------------|----------------------------------------------------------------------|
| GET    | `/api/scrape` | Scrapes the top 10 Hacker News headlines and inserts new ones      |
| GET    | `/api/news`   | Returns the 10 most recently stored articles (`id`, `title`, `link`) |

The API is available directly at `http://localhost:8000`.

---

## ⚙️ Configuration

Set via environment variables in `docker-compose.yml` (`api` and `db` services):

| Variable            | Description         | Default    |
|----------------------|----------------------|------------|
| `DB_HOST`            | Postgres hostname    | `db`       |
| `POSTGRES_DB`        | Database name        | `newsdb`   |
| `POSTGRES_USER`      | Database user        | `postgres` |
| `POSTGRES_PASSWORD`  | Database password    | `postgres` |

> ⚠️ **Security note:** The default credentials (`postgres` / `postgres`) are hardcoded directly in `docker-compose.yml`, and the Postgres port (`5432`) is published to the host. That's fine for local development, but **before deploying anywhere reachable from the internet**: move these values into a `.env` file (already excluded via `.gitignore`), set a strong password, and remove the public `5432:5432` port mapping unless external DB access is specifically needed.

---

## 🛑 Stopping

```bash
docker compose down
```

Add `-v` (`docker compose down -v`) to also delete the PostgreSQL data volume.

---

## 📂 Project Structure

```
python-news-scraper/
├── app/
│   ├── main.py           # FastAPI app: /api/scrape, /api/news
│   ├── scraper.py        # Scraping logic + DB access
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── style.css
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🐞 Known Issues / Notes

- The frontend hardcodes `http://localhost:8000` for API calls (in `frontend/index.html`) — it only works when you browse from the same machine the containers run on. For any other deployment, this URL needs to be made configurable.
- CORS is fully open (`allow_origins=["*"]`) in `app/main.py` — fine for local use, but should be restricted before any public deployment.
- `/api/scrape` has no authentication or rate limiting — anyone with network access to the API can trigger a scrape at will.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## 👤 Author

**Sina Mansouri**
GitHub: [@sina-mansouri](https://github.com/sina-mansouri)
