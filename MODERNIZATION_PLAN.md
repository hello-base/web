# Hello! Base Modernization Plan: Headless Architecture

**Date**: 2025-10-28
**Architecture**: Django API + Astro Frontend
**Timeline**: 10-15 weeks
**Branch Strategy**: See below

---

## Architecture Overview

- **Backend**: Django 4.2 + Django Ninja (pure REST API)
- **Frontend**: Astro 5.x + React islands + TanStack Query
- **Data Flow**: Astro fetches from Django API at build time → generates static HTML
- **URL Structure**: Flat (preserved from original - idols/groups at root level)
- **Deployment**:
  - Frontend: Vercel/Netlify (static hosting)
  - Backend: Railway (API + Django Admin)

---

## Why This Architecture?

1. **Content-driven site** (like Wikipedia) - minimal interaction beyond show/hide
2. **Rare updates** - idols don't change daily, perfect for static generation
3. **SEO critical** - need 207 idol pages indexed by Google
4. **Flat URL structure** - Already built, Astro handles this cleaner than Django multiurl
5. **Performance** - Pre-rendered HTML, ~0KB JS for content pages
6. **Modern DX** - TypeScript, hot reload, component-based

---

## Phase 0: API Foundation (2-3 weeks)

**Goal**: Build complete REST API while existing Django app runs unchanged

### Tasks:

1. **Install Django Ninja**
   ```bash
   pip install django-ninja pydantic
   pip install django-cors-headers
   ```

2. **Create API Structure**
   ```bash
   mkdir -p apps/api
   touch apps/api/__init__.py
   touch apps/api/api.py
   touch apps/api/schemas.py
   ```

3. **Define Pydantic Schemas** (`apps/api/schemas.py`)
   - IdolSchema
   - GroupSchema
   - AlbumSchema
   - SingleSchema
   - TrackSchema
   - EventSchema
   - NewsSchema

4. **Build API Endpoints** (`apps/api/api.py`)
   - GET /api/idols/ - List all idols
   - GET /api/idols/{slug}/ - Idol detail
   - GET /api/groups/ - List all groups
   - GET /api/groups/{slug}/ - Group detail
   - GET /api/albums/ - List all albums
   - GET /api/albums/{slug}/ - Album detail
   - GET /api/singles/ - List all singles
   - GET /api/singles/{slug}/ - Single detail
   - GET /api/tracks/{slug}/ - Track detail
   - GET /api/events/ - List events
   - GET /api/happenings/ - Timeline data
   - GET /api/search/?q={query} - Search

5. **Configure CORS** (for Astro dev server)
   - Add corsheaders to INSTALLED_APPS
   - Allow http://localhost:4321

6. **Register API in URLs** (`base/urls.py`)
   ```python
   re_path(r'^api/', api.urls),
   ```

7. **Test API**
   ```bash
   curl http://localhost:8000/api/idols/ | jq
   curl http://localhost:8000/api/idols/shinoda-miho/ | jq
   ```

**Deliverable**: Complete REST API with OpenAPI docs at `/api/docs`

---

## Phase 1: Astro Setup + Proof of Concept (1-2 weeks)

**Goal**: Initialize Astro frontend and build ONE working page

### Tasks:

1. **Initialize Astro**
   ```bash
   cd /Users/Avalonstar/Code/hello-base
   npm create astro@latest frontend
   cd frontend
   npm install @astrojs/react @astrojs/tailwind
   npm install react react-dom @tanstack/react-query
   npx astro add react tailwind
   ```

2. **Create API Client Library** (`frontend/src/lib/api.ts`)
   - TypeScript interfaces for all models
   - Fetch functions for all endpoints

3. **Create Layout** (`frontend/src/layouts/Layout.astro`)
   - Base HTML structure
   - Meta tags for SEO
   - OpenGraph tags

4. **Build Proof of Concept** (`frontend/src/pages/[slug].astro`)
   - Flat URL structure (idols + groups at root)
   - getStaticPaths() fetches both idols and groups
   - Slug collision detection at build time
   - Static HTML generation for all 207 idols + 91 groups

5. **Environment Variables**
   - `.env`: PUBLIC_API_URL=http://localhost:8000
   - `.env.production`: PUBLIC_API_URL=https://api.hello-base.com

6. **Test Locally**
   ```bash
   # Terminal 1: Django API
   docker-compose up

   # Terminal 2: Astro dev
   cd frontend
   npm run dev
   # Visit http://localhost:4321/shinoda-miho/
   ```

**Deliverable**: One working page (idol/group detail) fetching from Django API

---

## Phase 2: Core Content Pages (3-4 weeks)

**Goal**: Build all main content pages

### Pages to Build:

1. **Homepage** (`src/pages/index.astro`)
   - Happenings feed
   - On This Day
   - Statistics

2. **Music Pages** (`src/pages/music/[slug].astro`)
   - Albums + Singles at same path (like multiurl)
   - Build-time slug collision detection

3. **Track Pages** (`src/pages/music/tracks/[slug].astro`)
   - Track details
   - Lyrics display

4. **Optional List Pages**
   - `/idols/` - Browse all idols
   - `/groups/` - Browse all groups
   - `/music/` - Browse music

**Deliverable**: All core content pages working

---

## Phase 3: Interactive Features (2 weeks)

**Goal**: Add search and interactive components with React islands

### Components to Build:

1. **Search Component** (`src/components/Search.tsx`)
   - React island with TanStack Query
   - Real-time search with debouncing
   - Fetches from Django API

2. **Timeline Graphs** (`src/components/Timeline.tsx`)
   - React island with D3.js v7
   - Happenings visualization
   - Convert existing D3 v3 code

3. **Photo Gallery** (if needed)
   - React island for interactive galleries

**Deliverable**: Search and interactive features working

---

## Phase 4: Secondary Content (1-2 weeks)

**Goal**: Build remaining pages

### Pages to Build:

1. Events (`/events/{slug}/`)
2. Venues (`/venues/{slug}/`)
3. News (`/news/{year}/{month}/{slug}/`)
4. Happenings (`/happenings/{year}/`)
5. Shows (`/show/{slug}/`)
6. Magazines (`/magazine/{slug}/`)
7. Static pages (`/about/`, `/privacy/`, `/terms/`)

**Deliverable**: Complete site with all pages

---

## Phase 5: Production Ready (1-2 weeks)

**Goal**: SEO, performance optimization, deployment

### Tasks:

1. **SEO Optimization**
   - Add JSON-LD structured data
   - OpenGraph meta tags
   - Twitter card tags
   - Sitemap generation

2. **Image Optimization**
   - Serve images via CDN
   - Or use Astro image optimization

3. **Deploy Frontend** (Vercel)
   ```bash
   vercel
   ```

4. **Deploy Backend** (Railway)
   - Create railway.json
   - Configure environment variables

5. **Rebuild Webhook**
   - Add webhook in Django admin
   - Trigger Vercel rebuild when content changes

**Deliverable**: Production deployment with automatic rebuilds

---

## Final Project Structure

```
hello-base/
├── backend/                    # Django API
│   ├── apps/
│   │   ├── api/
│   │   │   ├── api.py         # Django Ninja endpoints
│   │   │   └── schemas.py     # Pydantic schemas
│   │   ├── people/
│   │   ├── merchandise/
│   │   └── ...
│   ├── base/
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/                   # Astro app
    ├── src/
    │   ├── pages/
    │   │   ├── index.astro
    │   │   ├── [slug].astro   # Idols + Groups
    │   │   ├── search.astro
    │   │   ├── music/
    │   │   └── ...
    │   ├── components/
    │   │   ├── Search.tsx     # React island
    │   │   └── Timeline.tsx   # React island
    │   ├── layouts/
    │   │   └── Layout.astro
    │   └── lib/
    │       └── api.ts         # API client
    ├── astro.config.mjs
    ├── package.json
    └── tsconfig.json
```

---

## Timeline Summary

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Phase 0: API Foundation | 2-3 weeks | Complete REST API |
| Phase 1: Astro POC | 1-2 weeks | One working page |
| Phase 2: Core Pages | 3-4 weeks | Idols, groups, music |
| Phase 3: Interactive | 2 weeks | Search, React islands |
| Phase 4: Secondary | 1-2 weeks | Events, news, etc |
| Phase 5: Production | 1-2 weeks | Deployed & optimized |
| **Total** | **10-15 weeks** | **Full migration** |

---

## Technology Stack

### Backend (Keep)
- ✅ Django 4.2 LTS
- ✅ PostgreSQL 15
- ✅ django-model-utils
- ✅ django-imagekit
- ✅ Pillow
- ✅ pytest
- ✅ gunicorn
- ✅ WhiteNoise
- ✅ django-grappelli (admin)

### Backend (Add)
- ✨ Django Ninja (REST API)
- ✨ Pydantic (schemas)
- ✨ django-cors-headers

### Backend (Remove)
- ❌ All templates (templates/ directory)
- ❌ django-markdown-deux
- ❌ typogrify
- ❌ django-haystack (replace with direct Elasticsearch later)

### Frontend (New)
- ✨ Astro 5.x
- ✨ React 18 (islands only)
- ✨ TanStack Query
- ✨ TypeScript
- ✨ Tailwind CSS
- ✨ D3.js v7 (for graphs)

---

## Branch Strategy

**Option A: New Branch** (Recommended)
- Create `headless-migration` or `astro-frontend` branch
- Keep `fukkatsu` branch as working Django templates version
- Merge when Astro frontend is feature-complete

**Option B: Continue on fukkatsu**
- Add frontend as subdirectory
- Both versions coexist during migration

---

## Migration Strategy

1. **Build API alongside existing Django app** (no disruption)
2. **Build Astro frontend in parallel** (can preview at different URL)
3. **Test thoroughly** before cutover
4. **Deploy new frontend** to new URL initially
5. **Switch DNS** when ready
6. **Keep Django templates** as fallback initially
7. **Remove templates** after confidence period

---

## Success Metrics

### Performance
- Page load: <100ms (static HTML)
- Build time: <5 minutes (298 pages)
- JS bundle: <50KB (React islands only)

### SEO
- All 298 pages indexed by Google
- OpenGraph previews working
- Sitemap generated

### Developer Experience
- Hot reload: <50ms
- Type safety with TypeScript
- Clear API documentation

---

## Cost Estimate

- **Frontend hosting**: $0 (Vercel free tier)
- **Backend hosting**: $5-20/mo (Railway)
- **CDN**: $0-20/mo (Cloudflare)
- **Total**: $5-40/mo

---

## Risk Mitigation

1. **Build API first** - validate all data is accessible
2. **Proof of concept** - one page working before building rest
3. **Parallel development** - don't break existing site
4. **Gradual cutover** - can deploy to subdomain first
5. **Rollback plan** - keep Django templates until confident

---

## Next Steps

1. ✅ Document plan (this file)
2. ⏭️ Create branch for headless migration
3. ⏭️ Start Phase 0: Build Django API
4. ⏭️ Test API thoroughly
5. ⏭️ Move to Phase 1: Astro POC
