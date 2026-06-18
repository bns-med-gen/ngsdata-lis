# LIS Project - AI Agent Instructions

## Project Overview
Laboratory Information System (LIS) - Single-page web application with Django REST API backend and jQuery frontend. Server-side pagination using SQLite database (`lis.db`).

**Tech Stack:**
- **Backend:** Django + Django REST Framework
- **Frontend:** jQuery (single-page application)
- **Database:** SQLite (`lis.db`) with SQLAlchemy ORM
- **Pagination:** Server-side implementation

---

## Key Files & Architecture

### Database & ORM
- **`lis.db`** - SQLite database file (primary data store)
- **`orm.py`** - SQLAlchemy ORM models (auto-generated from database schema)
- **`orm_gen.py`** - Script to regenerate ORM models using sqlacodegen

**Important:** The ORM is auto-generated. To update models after schema changes, run `orm_gen.py` which requires `sqlacodegen` in conda environment.

### Core Database Tables
Key entities in the LIS system:
- `Biomaterial` - Biological material samples with versioning/history tracking (🔒 **READ-ONLY**)
- `LisSampleMetadata` - Lab sample metadata and associations
- `LisProtocols` - DNA extraction protocols
- `MedicalFiles` - Patient medical records (🔒 **READ-ONLY**)
- `MedicalReports` - Test results and diagnoses (🔒 **READ-ONLY**)
- `MedicalTests` - Medical tests (🔒 **READ-ONLY**)
- `Patients` - Patient information (🔒 **READ-ONLY**)
- `TestSamples` - Test and sample associations (🔒 **READ-ONLY**)
- `LisDictionaryItems` - Lookup/reference data
- `LisSettings` - System configuration
- `LisTechprocesses` - Test type processes

---

## Backend Setup (Django)

### Structure
```
backend/
  manage.py
  requirements.txt
  lis_api/
    __init__.py
    settings.py
    urls.py
    wsgi.py
  api/
    __init__.py
    apps.py
    views.py (Django REST Framework ViewSets)
    serializers.py (DRF Serializers)
    urls.py
    migrations/
```

### API Endpoints (Read-Only)
All endpoints support server-side pagination with `?page=` and `?page_size=` query params:

- `GET /api/biomaterials/` - List/retrieve biological materials
- `GET /api/medical-files/` - List/retrieve medical files
- `GET /api/medical-reports/` - List/retrieve medical reports
- `GET /api/medical-tests/` - List/retrieve medical tests
- `GET /api/patients/` - List/retrieve patients
- `GET /api/test-samples/` - List/retrieve test samples

Each endpoint supports:
- **Pagination:** `?page=1&page_size=20`
- **Filtering:** Resource-specific filters (e.g., `?patientId=123` for biomaterials)
- **Search:** Full-text search via `?search=term`
- **Ordering:** Sort by fields via `?ordering=fieldname` (e.g., `?ordering=-ДатаОплаты`)

### Environment
- **Conda Environment:** `lis` (defined in `lis.yaml`)
- **Requirements file:** `backend/requirements.txt`
- **Key Dependencies:**
  - Django ≥ 5.2.15
  - Django REST Framework ≥ 3.17.1
  - django-cors-headers ≥ 4.0.0
  - djangorestframework_simplejwt
  - SQLAlchemy ≥ 2.0.48
  - PyJWT ≥ 2.8.0
  - SQLite
  - `sqlacodegen` for regenerating `orm.py`
  - Python ≥ 3.10

### API Conventions

**Server-Side Pagination:**
- Use `PageNumberPagination` from DRF
- Default page size: 20 items per page
- Query params: `?page=1&page_size=20`
- Response format includes `count`, `next`, `previous`, `page_size`, `total_pages`, `current_page`, `results`

**Authentication:**
- Default DRF permission class is `IsAuthenticated`
- Custom JWT auth is implemented in `backend/api/auth.py`
- Requests must send `Authorization: Bearer <token>`
- The signing key resolves from `JWT_PUBLIC_KEY`, `JWT_SECRET`, or `SECRET_KEY`

**CORS:**
- Allowed origins are configured in `backend/lis_api/settings.py`
- Local frontend ports include `http://localhost:8001` and `http://127.0.0.1:8001`

**ViewSet Pattern:**
```python
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class SQLAlchemyViewSet(viewsets.ViewSet):
    pagination_class = StandardResultsSetPagination
    # implementation uses SQLAlchemy sessions and manual list/retrieve logic
```

**URL Routing:**
- Top-level API path is `/api/` via `backend/lis_api/urls.py`
- Registered resource paths include `/api/biomaterials/`, `/api/medical-files/`, `/api/medical-reports/`, `/api/medical-tests/`, `/api/patients/`, `/api/test-samples/`
- List endpoints: GET `/api/{resource}/` (paginated)
- Detail endpoints: GET `/api/{resource}/{id}/`

---

## Frontend Setup (jQuery)

### Structure
```
frontend/
  index.html
  css/
    style.css
  js/
    app.js (main application logic)
```

### jQuery Conventions

**API Client Pattern:**
```javascript
const API_BASE = 'http://localhost:8000/api';

function fetchData(endpoint, page = 1, pageSize = 20) {
  return $.ajax({
    url: `${API_BASE}/${endpoint}/?page=${page}&page_size=${pageSize}`,
    type: 'GET',
    dataType: 'json'
  });
}
```

**Pagination UI:**
- Display current page info (e.g., "Page 1 of 5")
- Show "Previous" / "Next" buttons
- Update table/list on page change
- Handle loading states

**Error Handling:**
- Show user-friendly error messages
- Log errors to console for debugging
- Implement retry mechanisms for failed requests

---

## Common Development Workflows

### Adding a New API Endpoint
1. Define serializer in `api/serializers.py`
2. Create ViewSet in `api/views.py` with pagination
3. Register in `api/urls.py` with router
4. Test with: `curl http://localhost:8000/api/endpoint/?page=1`

### Updating Database Schema
1. Modify database schema directly (or via migration tool)
2. Run `orm_gen.py` to regenerate `orm.py`
3. Create new serializers if needed
4. Add corresponding API endpoints

### Frontend Data Display
1. Use `fetchData()` to get paginated data
2. Render results in table/list
3. Implement pagination controls from DRF response metadata
4. Handle empty states gracefully

---

## Setup & Execution

### Backend
```bash
# Create conda environment from lis.yaml
conda env create -f lis.yaml

# Activate environment
conda activate lis

# Navigate to backend directory
cd backend

# Install Python dependencies if needed
pip install -r requirements.txt

# Run server (default: http://localhost:8000)
python manage.py runserver
```

### Frontend
```bash
# Serve static files
python -m http.server 8001 --directory frontend

# Access at http://localhost:8001
```

### API Testing
```bash
# List all biomaterials (paginated)
curl http://localhost:8000/api/biomaterials/?page=1&page_size=20

# Get specific patient
curl http://localhost:8000/api/patients/PATIENT_ID/

# Filter medical tests by type
curl http://localhost:8000/api/medical-tests/?ТипОплаты=paid

# Search for medical reports
curl "http://localhost:8000/api/medical-reports/?search=diagnosis_name"
```

### Regenerate ORM (if database schema changes)
```bash
# Must run with lis conda environment activated
conda activate lis
python orm_gen.py
```

---

## Key Considerations

- **CORS:** Configure Django CORS middleware for jQuery requests from different domain/port
- **Pagination:** Always use server-side pagination; frontend receives only current page
- **SQL Indexes:** Database has indexes on frequently queried fields (see `__table_args__` in orm.py)
- **History Tracking:** `Biomaterial` table has `history` field for audit trail
- **Soft Deletes:** `Biomaterial` has `isDeleted` field for soft delete pattern
- **Cyrillic Columns:** Database column names may use Cyrillic. Preserve exact names in ORM mappings, serializers, and API source mappings when exposing fields.
- **Read-Only Tables:** The following tables support only GET (list/retrieve) operations:
  - `Biomaterial`, `MedicalFiles`, `MedicalReports`, `MedicalTests`, `Patients`, `TestSamples`
  - Use `rest_framework.permissions.IsAuthenticatedReadOnly` or custom read-only ViewSets
  - Do NOT create POST/PUT/PATCH/DELETE endpoints for these tables

---

## Available AI Skills

- `/skill create-api-endpoint <resource>`: scaffold a new Django REST endpoint with serializer, paginated ViewSet, router registration, and optional tests.
- `/skill update-orm`: regenerate `orm.py` from `lis.db` using `orm_gen.py`, then verify the new models and fields.
- `/skill frontend-page <resource>`: scaffold a jQuery single-page UI for a paginated resource, including table rendering, previous/next controls, and error handling.
- `/skill explain-cyrillic-schema`: describe how to map Cyrillic database column names safely into Django serializers and JSON field names.

---

## Common Commands & Debugging

| Task | Command |
|------|---------|
| View ORM models | Open `orm.py` and inspect class definitions |
| Database queries | Use Django ORM: `Biomaterial.objects.filter(...)` |
| API test | `curl http://localhost:8000/api/biomaterials/?page=1` |
| ORM regeneration | `python orm_gen.py` |
| Frontend debug | Browser console (F12) for jQuery logs and network requests |

---

## Questions for AI Agents

**Before implementing features:**
1. Which API endpoint(s) are needed?
2. Does the response need pagination?
3. Is this a new table or existing one in the schema?
4. Should frontend pre-fetch next page for better UX?

