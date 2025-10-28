# Docker Development Environment

## Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

3. **Run migrations (in another terminal):**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create superuser (optional):**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application:**
   - Web: http://localhost:8001
   - Admin: http://localhost:8001/admin/
   - Elasticsearch: http://localhost:9200

## Services

- **web**: Django application (Python 2.7 + Django 1.8)
- **db**: PostgreSQL 12
- **redis**: Redis 6 (for Celery)
- **elasticsearch**: Elasticsearch 1.7.6 (matching original version)

## Common Commands

### Start services
```bash
docker-compose up
```

### Start in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f web
```

### Run Django commands
```bash
docker-compose exec web python manage.py <command>
```

### Run tests
```bash
docker-compose exec web py.test tests/
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Rebuild after dependency changes
```bash
docker-compose build web
docker-compose up
```

### Access database directly
```bash
docker-compose exec db psql -U hellobase -d hellobase
```

## Troubleshooting

### Port already in use
If port 8001, 5432, 6379, or 9200 is already in use, edit `docker-compose.yml` to change the port mapping.

### Database connection issues
Ensure the DATABASE_URL in `.env` matches the docker-compose.yml configuration.

### Elasticsearch not starting
Elasticsearch 1.7.6 may require more memory. Increase Docker's memory limit in Docker Desktop settings.

## Upgrade Process

As we progress through Django upgrades, the Dockerfile will be updated to reflect:
- Hop 1: Still Python 2.7, Django 1.11
- Hop 2: Python 3.11+, Django 1.11
- Hop 3+: Python 3.11+, Django 2.2 → 4.2

Each hop will be tested in this Docker environment before committing changes.
