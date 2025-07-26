# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## User communication
- ユーザーとのやり取りは日本語を使用してください
- .clinerulesの中に様々なルールを記載していますので確認してください

## Project Overview

This is a mechanism sharing platform - a web application for visualizing and sharing physical mechanisms with user interactions. Users can post, view, and rate mechanisms with reliability levels ranging from "fantasy model" (theoretical hypothesis) to "textbook listed" (academically established).

**Architecture**: FastAPI backend + React TypeScript frontend + PostgreSQL database

## Development Commands

### Quick Start (Windows)
```bash
# Start entire application (backend + frontend)
start_app.bat

# Stop application
stop_app.bat
```

### Manual Backend Commands
```bash
# Install dependencies
uv pip install -r backend/requirements.txt

# python environment
source .venv/bin/activate

# Start development server
uvicorn backend.app.main:app --reload

# Database migrations
alembic upgrade head
alembic current
alembic history
```

### Manual Frontend Commands
```bash
cd frontend
npm install
npm start
npm run build
```

### Testing Commands

**Backend Tests:**
```bash
# Run all backend unit tests
python -m pytest backend/tests/ -v

# Run integration tests
python tests/run_integration_tests.py
python -m pytest tests/integration/ -v

# Run specific test file
python -m pytest backend/tests/test_auth.py -v
```

**Frontend Tests:**
```bash
cd frontend
npm test
npm test -- --coverage --watchAll=false  # CI mode
```

## Architecture Overview

### Backend Structure (FastAPI)
**Clean layered architecture** with dependency injection:
- **Router Layer** (`/routers/`) - API endpoints
- **Service Layer** (`/services/`) - Business logic 
- **Model Layer** (`/models/`) - SQLAlchemy database models
- **Schema Layer** (`/schemas/`) - Pydantic validation/serialization
- **Middleware Layer** (`/middlewares/`) - Authentication middleware
- **Utils Layer** (`/utils/`) - Security utilities

**Key Patterns:**
- FastAPI dependency injection (`Depends()`)
- JWT authentication with Bearer tokens
- Static file serving for uploads
- Repository/Service pattern for business logic

### Frontend Structure (React)
**Feature-based organization**:
- **components/auth/** - Authentication components
- **components/common/** - Reusable UI components
- **pages/** - Top-level route components
- **services/** - API integration layer
- **contexts/** - Global state (AuthContext)
- **types/** - TypeScript definitions

**Key Patterns:**
- Context API for authentication state
- Service layer for API calls with Axios
- Protected routes with authentication
- Form handling with validation

### Database Models
**Core entities with relationships:**
- `User` (1:N with Mechanisms)
- `Mechanism` (M:N with Categories, 1:N with Views)
- `Category` (M:N with Mechanisms)
- `Like` (M:N User-Mechanism relationship)
- `MechanismView` (Analytics tracking)

## Key Files & Locations

### Configuration
- `backend/app/config.py` - Backend configuration
- `frontend/src/services/api.ts` - API client setup
- `alembic.ini` - Database migration config

### Authentication
- `backend/app/middlewares/auth.py` - JWT middleware
- `backend/app/utils/security.py` - Password hashing, token generation
- `frontend/src/contexts/AuthContext.tsx` - Authentication state management

### File Uploads
- **Backend**: `uploads/files/` (mechanism files), `uploads/thumbnails/` (thumbnails)
- **Frontend**: `FileUpload` component, `getFileUrl` utility

## Development Notes

### Authentication Flow
1. User submits credentials → `/api/auth/login`
2. Backend validates → returns JWT token
3. Frontend stores token → includes in Authorization header
4. Backend middleware validates token → injects user

### File Upload Process
1. Frontend creates FormData → POST to `/api/mechanisms/`
2. Backend handles file storage with UUID naming
3. Categories auto-created if they don't exist
4. Static files served at `/uploads/` endpoint

### Testing Infrastructure
- **Backend**: pytest with SQLite test databases
- **Frontend**: Jest + React Testing Library
- **Integration**: Full stack tests with temporary databases
- **Isolation**: Each test uses fresh database session

### Known Issues
- View count increments by 2 (React StrictMode effect)
- Some tests may need unique data generation to avoid conflicts

## Common Patterns

### Adding New API Endpoint
1. Create/update model in `models/`
2. Define schemas in `schemas/`
3. Implement service logic in `services/`
4. Add router endpoints in `routers/`
5. Include router in `main.py`

### Adding New UI Component
1. Create component in appropriate `components/` subdirectory
2. Add TypeScript interfaces in `types/`
3. Update service layer if API integration needed
4. Add to routing if it's a page component

### Error Handling
- **Backend**: FastAPI automatic validation + custom HTTP exceptions
- **Frontend**: Axios interceptors for global error handling
- **Authentication**: 401 errors trigger logout and redirect

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Mechanisms
- `GET /api/mechanisms/` - List mechanisms (with pagination)
- `GET /api/mechanisms/{id}` - Get mechanism details
- `POST /api/mechanisms/` - Create mechanism (with file upload)

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category

### Likes
- `POST /api/likes/{mechanism_id}` - Add like
- `DELETE /api/likes/{mechanism_id}` - Remove like

### Views
- `POST /api/mechanism-views/{mechanism_id}` - Record view
- `GET /api/mechanism-views/{mechanism_id}` - Get view count

## Database
- **Development**: PostgreSQL recommended
- **Testing**: SQLite with temporary files
- **Migrations**: Alembic for schema changes
- **Connection**: SQLAlchemy with connection pooling