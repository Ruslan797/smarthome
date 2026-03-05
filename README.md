# SmartHome Backend API

Backend service for a smart home platform: devices, sensors and automation scenarios.
Built with Django + Django REST Framework. Background tasks are handled with Celery + Redis.

---

## Features
- Devices CRUD
- Sensors CRUD (bind sensors to devices)
- Scenarios / automation rules (run actions based on sensor data)
- REST API with DRF
- Background tasks with Celery (e.g. periodic checks / automation)

---

## Tech Stack
- Python
- Django
- Django REST Framework
- Celery
- Redis
- Database: MySQL (see `mysqlclient` in requirements) / can be configured via env

---

## Project Structure

core/ - Django project settings, urls, celery config
devices/ - devices app (models/serializers/views/urls)
sensors/ - sensors app (models/serializers/views/urls)
scenarios/ - scenarios app (automation logic, tasks)
blog/ - optional blog app


---

## Installation (local)
1) Clone repository
```bash

git clone https://github.com/Ruslan797/smarthome.git
cd smarthome

Create virtual environment & install dependencies

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt

Create .env (recommended) and configure settings (DB/Redis)
Example:

DEBUG=1
SECRET_KEY=change-me
DB_NAME=smarthome
DB_USER=smarthome
DB_PASSWORD=smarthome
DB_HOST=localhost
DB_PORT=3306
REDIS_URL=redis://localhost:6379/0

Run migrations & start server

python manage.py migrate
python manage.py runserver

API will be available at:
http://127.0.0.1:8000/

Run Celery

In a separate terminal:

celery -A core worker -l info

(Optional) Celery Beat:

celery -A core beat -l info

Author
Ruslan Buievskyi — Python Backend Developer
