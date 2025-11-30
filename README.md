# FastAPI Project Template

A production-ready FastAPI project template with best practices, structured logging, error handling, and a scalable architecture ready for authentication. I left authentication out of this verstion, but added documentation on implementing application based authentication. I rarely use app based authentitcation system as generally SAML/OAuth.

## Features

- ✅ **Layered Architecture**: Clear separation of concerns (API, business logic, data access)
- ✅ **Structured Logging**: JSON logging with correlation IDs for request tracking
- ✅ **Error Handling**: Global exception handling with custom error types
- ✅ **Configuration Management**: Environment-based configuration with Pydantic Settings
- ✅ **Health Checks**: Ready, live, and health check endpoints
- ✅ **Type Safety**: Full type hints throughout
- ✅ **Testing**: Pytest setup with example tests
- ✅ **Documentation**: MkDocs configuration included
- ✅ **Development Tools**: Black, Ruff, Pylint, MyPy configured
- ✅ **Authentication Ready**: Structure prepared for adding authentication layer
- ✅ **HTMX Templating**: Jinja2 templates with HTMX for dynamic web interfaces

## Project Structure

```
.
├── app/
│   ├── api/              # API routes and endpoints
│   │   └── v1/
│   │       ├── endpoints/ # Individual endpoint modules
│   │       └── router.py  # API router configuration
│   ├── core/             # Core configuration and utilities
│   │   ├── config.py     # Application settings
│   │   ├── exceptions.py # Custom exceptions
│   │   └── logging.py    # Logging configuration
│   ├── db/               # Database configuration (ready for ORM)
│   ├── middleware/       # Custom middleware
│   ├── models/           # Domain models (Pydantic)
│   ├── repositories/     # Data access layer (abstraction)
│   ├── schemas/          # API schemas and response models
│   └── main.py           # Application entry point
├── templates/            # Jinja2 templates
│   ├── base.html        # Base template with HTMX
│   ├── index.html       # Main index page
│   └── htmx/            # HTMX partial templates
├── tests/                # Test suite
├── docs/                 # Documentation
├── pyproject.toml        # Project configuration
└── README.md
```

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment file
cp .env.example .env
# Edit .env with your project-specific values
```

### 2. Update Project Information

1. Update `pyproject.toml`:

   - Change `CHANGEME_PROJECT_NAME` to your project name
   - Update description and other metadata

2. Update `.env`:

   - Set `PROJECT_NAME` and `PROJECT_DESCRIPTION`
   - Change `SECRET_KEY` to a secure random value
   - Adjust other settings as needed

3. Update `mkdocs.yml`:

   - Change site name, description, and author

4. Remove or replace example code:
   - Replace `app/api/v1/endpoints/items.py` with your domain logic
   - Update `app/models/item.py` with your domain models

### 3. Run the Application

```bash
uvicorn app.main:app --reload --port 8910
```

The API will be available at:

- API: http://localhost:8910/api/v1
- HTMX UI: http://localhost:8910/ (redirects to http://localhost:8910/api/v1/htmx/)
- Docs: http://localhost:8910/docs
- ReDoc: http://localhost:8910/redoc

### 4. Run Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=app --cov-report=html
```

## HTMX Templating

The template includes full HTMX support for building dynamic web interfaces. See the [HTMX Templating Guide](docs/development/guides/htmx_templating.md) for detailed documentation.

### Quick Example

```python
from fastapi import Request
from fastapi.responses import HTMLResponse
from app.core.templates import render_template

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return render_template(
        request=request,
        template_name="index.html",
        context={"project_name": "My App"},
    )
```

```html
<!-- templates/index.html -->
<button hx-get="/api/v1/htmx/data" hx-target="#result" hx-swap="innerHTML">
  Load Data
</button>
<div id="result"></div>
```

Visit http://localhost:8910/api/v1/htmx/ to see working examples.

## Adding Authentication

The project structure is ready for authentication. Here's how to add it:

### 1. Add Authentication Dependencies

The template already includes `python-jose[cryptography]` for JWT tokens. You may also want:

- `passlib[bcrypt]` for password hashing
- `python-multipart` (already included) for form data

### 2. Create Authentication Module

Create `app/core/security.py`:

- Password hashing functions
- JWT token creation/verification
- Token decoding utilities

### 3. Create User Models

Create `app/models/user.py`:

- User domain model
- User creation/update schemas

### 4. Add Authentication Endpoints

Create `app/api/v1/endpoints/auth.py`:

- Login endpoint
- Token refresh endpoint
- Registration endpoint (if needed)

### 5. Add Authentication Dependencies

Create `app/api/dependencies.py`:

- `get_current_user` dependency
- `get_current_active_user` dependency
- Permission checking dependencies

### 6. Protect Routes

Update routers to require authentication:

```python
from app.api.dependencies import get_current_active_user

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": "This is protected"}
```

### 7. Add Database

When ready, add SQLAlchemy or your preferred ORM:

- Update `app/db/base.py` with database configuration
- Create database models in `app/models/db/`
- Update repositories to use database sessions

## Development

### Code Quality

```bash
# Format code
black app tests

# Lint code
ruff check app tests
pylint app tests

# Type checking
mypy app
```

### Documentation

```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## Configuration

All configuration is managed through environment variables (see `.env.example`). Key settings:

- `ENVIRONMENT`: development, staging, production
- `DEBUG`: Enable/disable debug mode
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `LOG_FORMAT`: json (production) or console (development)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `SECRET_KEY`: Secret key for cryptographic operations (change in production!)

## Best Practices

This template follows:

- **Separation of Concerns**: Clear layer boundaries
- **Dependency Injection**: FastAPI's dependency system
- **Error Handling**: Custom exceptions with proper HTTP status codes
- **Logging**: Structured logging with correlation IDs
- **Type Safety**: Full type hints
- **Testing**: Comprehensive test coverage
- **Security**: Ready for authentication, input validation

## Next Steps

1. Replace example code with your domain logic
2. Add database models and repositories
3. Implement authentication (see guide above)
4. Add your business logic
5. Deploy!

## License

[Add your license here]
