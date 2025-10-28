# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hello! Base is a Django-based database and web application for Hello! Project idol information. It contains data on 207 idols, 91 groups, 615 singles, 219 albums, and 2,712 tracks spanning Hello! Project's history from 1997 to present.

**Current State (2025)**: Recently modernized from Python 2.7/Django 1.8 (2015) to Python 3.11/Django 4.2. Currently undergoing migration to headless architecture (see `MODERNIZATION_PLAN.md`).

## Technology Stack

### Backend (Current)
- **Framework**: Django 4.2.17 LTS with django-configurations
- **Python**: 3.11.11
- **Database**: PostgreSQL 15
- **Search**: Elasticsearch 8.16.0 (temporarily disabled during migration)
- **Task Queue**: Celery 5.4.0 (temporarily disabled during migration)
- **Static Files**: WhiteNoise 6.8.2 for serving
- **Image Processing**: django-imagekit 5.0.0 + Pillow 11.0.0
- **Authentication**: Custom OAuth backend (HelloBaseIDBackend)

### Infrastructure
- **Development**: Docker Compose (PostgreSQL 15, Redis 7, Elasticsearch 8)
- **Testing**: pytest 8.3.4 + pytest-django 4.9.0
- **Production**: Gunicorn 23.0.0 WSGI server

## Development Environment

### Docker Setup (Primary Method)

See [DOCKER.md](DOCKER.md) for full Docker setup instructions.

```bash
# Start all services (PostgreSQL, Redis, Elasticsearch, Django)
docker-compose up

# Run migrations
docker-compose exec web python manage.py migrate

# Access Django shell
docker-compose exec web python manage.py shell

# Run management commands
docker-compose exec web python manage.py <command>
```

The development server runs on `http://localhost:8001`.

### Testing

```bash
# Run all tests
docker-compose exec web pytest

# Run specific test file
docker-compose exec web pytest tests/people/test_managers.py

# Run with coverage
docker-compose exec web pytest --cov

# Or locally (if you have Python 3.11 installed)
pytest tests/
```

Tests use pytest with `--nomigrations` flag. Configuration in `setup.cfg`.

### Database Management

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create new migration
docker-compose exec web python manage.py makemigrations

# Load database dump (PostgreSQL custom format)
docker-compose exec -T db pg_restore -U hellobase -d hellobase --clean --if-exists < dump.dump

# Create database dump
docker-compose exec -T db pg_dump -U hellobase -Fc hellobase > dump.dump
```

### Admin Interface

Access the Django admin at `http://localhost:8001/admin/` using django-grappelli enhanced UI.

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

**Flat URL Design**: Hello! Base uses a carefully designed flat URL structure to maximize simplicity and SEO.

Main URLs defined in `base/urls.py`. Key patterns:
- **People**: `/{slug}/` - Both idols AND groups at root level using `django-multiurl`
  - Example: `/shinoda-miho/` (idol), `/morning-musume/` (group)
  - The multiurl pattern tries idol first, then falls back to group
- **Music**: `/music/{slug}/` - Both albums AND singles (multiurl pattern)
  - Tracks: `/music/tracks/{slug}/`
- **Events**: `/events/{slug}/`, `/venues/{slug}/`
- **News**: `/news/{year}/{month}/{slug}/`
- **Happenings**: `/happenings/{year}/`
- **Search**: `/search/`, `/search/autocomplete/`

This flat structure was painstakingly designed to avoid nested URLs and maximize URL clarity.

### Search Implementation

**Status**: Temporarily disabled during modernization.

Previously used django-haystack with Elasticsearch backend. Will be replaced with direct Elasticsearch integration using `elasticsearch-dsl-py` in the upcoming headless architecture migration.

### Image Management

Uses django-imagekit for image processing. Images are processed into various sizes defined as `ImageSpecField` on models:
- `optimized_square`: 300x300 smart crop
- `optimized_thumbnail`: 300px width

Images stored in `media/people/idols/` and `media/people/groups/`.

### Static Assets

**Status**: Being modernized as part of headless architecture migration.

Current state:
- Static files served via WhiteNoise
- CSS/JS in `static/` directory
- Django templates in `templates/`

**Future state** (see `MODERNIZATION_PLAN.md`):
- Django becomes pure API backend
- Astro frontend with modern build pipeline
- React islands for interactive features

## Development Notes

- **Time Zone**: Asia/Tokyo (TIME_ZONE setting)
- **Custom User Model**: `accounts.Editor` (AUTH_USER_MODEL)
- **Admin Interface**: Uses django-grappelli 4.0.1 for enhanced admin UI
- **Static Files**: Served via WhiteNoise 6.8.2 with CompressedManifestStaticFilesStorage
- **Deployment**: Container-ready (Docker), production uses Gunicorn WSGI server

## Data Model Highlights

The database contains 10 years of Hello! Project history:
- **207 idols** with birthdates, groups, career timelines
- **91 groups** with member relationships via many-to-many through Membership model
- **615 singles** + **219 albums** with full track listings
- **2,712 tracks** with metadata and lyrics
- **Events, venues, appearances** in magazines and TV shows
- **Correlations timeline** system for "on this day" functionality

## Modernization Roadmap

**Current Phase**: Django 4.2 + Python 3.11 modernization complete (fukkatsu branch)

**Next Phase**: Headless architecture migration (shinseiki branch)
- Django Ninja REST API backend
- Astro static site generator frontend
- React islands for interactive features
- See `MODERNIZATION_PLAN.md` for complete details

## Important Patterns

### Flat URL Structure with Multiurl

The codebase uses `django-multiurl` to achieve flat URLs where both idols and groups share the root path (`/{slug}/`). When implementing new features, preserve this pattern:

```python
from multiurl import multiurl, ContinueResolving
from django.http import Http404

urlpatterns = [
    multiurl(
        re_path(r'^(?P<slug>[-\w]+)/$', IdolDetailView.as_view(), name='idol-detail'),
        re_path(r'^(?P<slug>[-\w]+)/$', GroupDetailView.as_view(), name='group-detail'),
        catch=(Http404, ContinueResolving)
    ),
]
```

### Custom Ohashi Library

The `apps/ohashi` library provides special birthday field handling:

```python
from apps.ohashi.db.models import BirthdayField
from apps.ohashi.db.models.managers import BirthdayManager

class Idol(models.Model):
    birthdate = BirthdayField(blank=True, null=True, db_index=True)
    birthdays = BirthdayManager()  # Enables .this_month() queries
```

This automatically creates a `birthdate_dayofyear` field for querying birthdays regardless of year.
