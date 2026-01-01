# Final Task Project

A Django-based web application designed for containerized environments, focusing on image processing and management. This project utilizes modern Python tooling and Docker to ensure a scalable and reproducible development workflow.

## Features

* **Image Management:** Dedicated structure for handling static and uploaded media assets.
* **Containerized Architecture:** Fully orchestrated using Docker and Docker Compose for consistent deployment.
* **Modern Dependency Management:** Uses `pyproject.toml` and `uv.lock` for fast and reliable package resolution.
* **Database Integration:** Pre-configured with SQLite for local development, with support for migration to PostgreSQL.

## Tech Stack

* **Language:** Python
* **Framework:** Django
* **Containerization:** Docker & Docker Compose
* **Dependency Manager:** uv (configured via `pyproject.toml`)
* **Database:** SQLite (default), PostgreSQL (compatible)

## Project Structure

```text
.
├── finaltask/            # Core Django configuration and settings
├── images/               # Directory for media assets and image processing
├── app.py                # Application entry point or utility script
├── manage.py             # Django command-line utility
├── Dockerfile            # Instructions for building the application image
├── docker-compose.yaml   # Service orchestration configuration
├── pyproject.toml        # Project metadata and dependencies
└── uv.lock               # Exact dependency versions for reproducible builds

```

## Getting Started

### Prerequisites

* Docker and Docker Compose installed.
* Python installed (if running locally without Docker).
* `uv` (recommended) or `pip` for dependency management.

### Running with Docker

1. Clone the repository:

```bash
git clone https://github.com/emilx01/final_task.git
cd final_task

```

2. Build and start the containers:

```bash
docker-compose up --build

```

### Running Locally

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate.fish  # For Fish shell users
# or
source .venv/bin/activate       # For Bash/Zsh users

```

2. Install dependencies:
If you are using `uv`:
```bash
uv sync

```


If you are using standard `pip`:
```bash
pip install .

```


3. Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver

```