# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hello! Base is a Django-based database and web application for Hello! Project idol information. It uses PostgreSQL, Elasticsearch for search, and is deployed on Heroku.

## Technology Stack

- **Framework**: Django 1.8.2 with django-configurations
- **Database**: PostgreSQL (via django-heroku-postgresify)
- **Search**: Elasticsearch with django-haystack 2.4.0rc1
- **Task Queue**: Celery 3.1.18
- **Static Files**: WhiteNoise for serving, Compass for Sass, CoffeeScript for JS
- **Image Processing**: django-imagekit
- **Authentication**: Custom OAuth backend (HelloBaseIDBackend)

## Development Environment

### Docker (Recommended for 2025)

See [DOCKER.md](DOCKER.md) for full Docker setup instructions.

```bash
# Quick start
cp .env.example .env
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Run tests
docker-compose exec web py.test tests/
```

### Legacy Development Server (Pre-Docker)

```fish
# Start all development processes (web, elasticsearch, compass, coffee)
invoke server
# Or directly:
foreman start -f Procfile.dev
```

The development server runs on `http://0.0.0.0:8001`.

### Testing

```fish
# Run tests
invoke test
# Or directly:
py.test tests/

# Run tests with coverage report
invoke test --coverage

# Run specific test file
py.test tests/people/test_managers.py
```

Tests use pytest with `--nomigrations` flag. Configuration in setup.cfg.

### Code Quality

```fish
# Run flake8 linting
invoke flake
# Or directly:
flake8 --max-complexity 6 > flake8.txt
```

Flake8 config: excludes migrations, ignores E125/E128/E501, max complexity 6.

### Database Management

```fish
# Run migrations
python manage.py migrate

# Pull production database to local
invoke heroku.pull --database=hello-base

# Create database snapshot
invoke heroku.capture
```

### Heroku Deployment

```fish
# Deploy to Heroku (runs tests first)
invoke deploy

# Deploy with migrations (disables preboot, runs migrations, re-enables preboot)
invoke deploy --migrate

# Generate ImageKit thumbnails on Heroku
invoke heroku.imagekit
```

## Architecture

### Settings Configuration

Uses django-configurations for class-based settings. Settings are in `base/settings/`:
- `base.py`: Base configuration for all environments
- `development.py`: Local development settings
- `testing.py`: Test environment settings

Environment is controlled via `DJANGO_CONFIGURATION` environment variable. Uses python-dotenv for `.env` file support.

### Application Structure

Django apps are organized in the `apps/` directory:

**Core Domain Models**:
- `people`: Idol and Group models, the central entities
- `merchandise`: Parent app for all merchandise-related models
  - `merchandise.music`: Albums, singles, tracks
  - `merchandise.goods`: Physical goods
  - `merchandise.media`: Media products
  - `merchandise.stores`: Store information
- `appearances`: Idol appearances in media
- `events`: Events and performances
- `correlations`: Timeline system for "what happened on this day" functionality

**Supporting Apps**:
- `accounts`: Custom user model (Editor) with OAuth authentication
- `history`: Historical tracking
- `news`: News articles
- `prose`: Content/articles
- `social.twitter`: Twitter integration
- `social.youtube`: YouTube integration

### Key Patterns

**Custom Managers and QuerySets**: The codebase extensively uses PassThroughManager from django-model-utils to provide chainable custom QuerySet methods. See `people/managers.py` and `correlations/managers.py`.

**Person Abstract Base Class**: `people.models.Person` is an abstract base class that handles Japanese name rendering (family name + given name, with optional romanization and aliases). Both `Idol` and `Group` inherit from this.

**Correlations System**: The `correlations` app uses Django's GenericForeignKey to create a universal timeline of dated events across different model types. This enables queries like "what happened on this day in history" and "what's coming up".

**ContributorMixin**: Models inherit from `ContributorMixin` (`apps.accounts.models`) to track which editor created/modified records.

**Special Date Handling**: Uses the `ohashi` library for birthday fields and birthday managers, allowing queries like "birthdays this month" without year consideration.

### URL Structure

Main URLs defined in `base/urls.py`. Most apps have their own `urls.py` included at root level (not prefixed). For example:
- People: `/idols/`, `/groups/`
- Music: `/albums/`, `/singles/`, `/tracks/`
- Search: `/search/`, `/search/autocomplete/`

### Search Implementation

Uses django-haystack with Elasticsearch backend. Search indexes defined per-app (e.g., `people/search_indexes.py`). Faceted search is enabled with results faceted by model type.

### Image Management

Uses django-imagekit for image processing. Images are processed into various sizes defined as ImageSpecField on models. Use `python manage.py generateimages` to generate thumbnails.

### Static Assets

- Source assets: `base/assets/`
- Compiled output: `static/`
- Compass (Sass) watches and compiles to `static/stylesheets/`
- CoffeeScript compiles to `static/javascripts/application/`

## Development Notes

- **Time Zone**: Asia/Tokyo (TIME_ZONE setting)
- **Custom User Model**: `accounts.editor` (AUTH_USER_MODEL)
- **Admin Interface**: Uses django-grappelli for enhanced admin UI
- **Deployment**: Heroku with Procfile, uses Gunicorn in production
- **Static Files**: Collected to `staticfiles/`, served via WhiteNoise with GzipManifest
