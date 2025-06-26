# Knowledge Capsules

Минималистичное приложение для сохранения "капсул знаний" и получения напоминаний по расписанию.

## Запуск через Docker Compose

1. Создайте файл `.env` в корне проекта и укажите переменные:

```bash
SECRET_KEY=changeme
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/knowledge
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
SENDGRID_API_KEY=your-sendgrid-key
EMAILS_FROM_EMAIL=noreply@example.com
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

2. Соберите и запустите сервисы:

```bash
docker-compose up --build
```

Backend будет доступен на `http://localhost:8000`, Frontend — на `http://localhost:3000`.
