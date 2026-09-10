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

2. **Create your environment file:**

```bash
cp .env.example .env
```

Then open `.env` and set a real, strong value for `POSTGRES_PASSWORD` (don't leave the default in place).

3. **Build and start all containers:**

```bash
docker compose up -d --build
```

This starts three containers:

| Service    | Container name  | Host port | Purpose                  |
|------------|------------------|-----------|---------------------------|
| `api`      | `news_api`       | `8000`    | FastAPI backend           |
| `db`       | `news_db`        | *(internal only)* | PostgreSQL database |
| `frontend` | `news_frontend`  | `8081`    | Static web UI (Nginx)     |

4. **Open the frontend:**

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

Set via a `.env` file (copied from `.env.example`) that `docker-compose.yml` reads automatically:

| Variable            | Description         | Default in `.env.example`      |
|----------------------|----------------------|----------------------------------|
| `POSTGRES_DB`        | Database name        | `newsdb`                         |
| `POSTGRES_USER`      | Database user        | `postgres`                       |
| `POSTGRES_PASSWORD`  | Database password    | *(you must set your own)*        |

`DB_HOST` is set directly in `docker-compose.yml` to `db` (the internal Docker network name of the database container) and doesn't need to be in `.env`.

✅ **Fixed:** credentials are no longer hardcoded in `docker-compose.yml`, `.env` is excluded via `.gitignore` (so it's never committed), and the Postgres port (`5432`) is no longer published to the host by default — the `db` container is only reachable from the `api` container over the internal Docker network. Uncomment the `ports:` line under the `db` service only if you specifically need to connect from a local DB client.

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
├── .env.example           # Copy to .env and fill in your own values
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
