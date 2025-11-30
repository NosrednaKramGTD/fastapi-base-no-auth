# Adding Authentication to Your FastAPI Project

This guide walks you through adding authentication to your FastAPI project template. The template is already structured to make this straightforward.

## Overview

The authentication layer will include:
- JWT token-based authentication
- Password hashing with bcrypt
- User management
- Protected routes with dependency injection
- Token refresh mechanism

## Step 1: Add Additional Dependencies

Update `pyproject.toml` to include password hashing:

```toml
dependencies = [
    # ... existing dependencies ...
    "passlib[bcrypt]>=1.7.4",
]
```

The template already includes:
- `python-jose[cryptography]` for JWT tokens
- `python-multipart` for form data

## Step 2: Create Security Module

Create `app/core/security.py`:

```python
"""Security utilities for authentication."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token data or None if invalid
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
```

## Step 3: Create User Models

Create `app/models/user.py`:

```python
"""User domain models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, description="User's full name", max_length=200)
    is_active: bool = Field(default=True, description="Whether user is active")
    is_superuser: bool = Field(default=False, description="Whether user is a superuser")


class UserCreate(UserBase):
    """Model for creating a new user."""

    password: str = Field(..., description="User password", min_length=8)


class UserUpdate(BaseModel):
    """Model for updating a user (all fields optional)."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class User(UserBase):
    """Complete user model with ID and timestamps."""

    id: int = Field(..., description="User identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
            }
        }
    }


class UserInDB(User):
    """User model with hashed password (for database storage)."""

    hashed_password: str
```

## Step 4: Create Authentication Schemas

Create `app/schemas/auth.py`:

```python
"""Authentication request/response schemas."""

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""

    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str
```

## Step 5: Create Authentication Dependencies

Create `app/api/dependencies.py`:

```python
"""FastAPI dependencies for authentication."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.models.user import User

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current authenticated user from JWT token.

    Args:
        token: JWT access token

    Returns:
        Current user

    Raises:
        UnauthorizedError: If token is invalid or user not found
    """
    credentials_exception = UnauthorizedError(
        message="Could not validate credentials",
        details={"headers": {"WWW-Authenticate": "Bearer"}},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception

    # TODO: Replace with actual database lookup
    # user = await user_repository.get_by_email(email)
    # if user is None:
    #     raise credentials_exception

    # For now, return a mock user (replace with database lookup)
    user = User(
        id=1,
        email=email,
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active user.

    Args:
        current_user: Current user from get_current_user

    Returns:
        Active user

    Raises:
        ForbiddenError: If user is not active
    """
    from app.core.exceptions import ForbiddenError

    if not current_user.is_active:
        raise ForbiddenError(message="Inactive user")
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get the current superuser.

    Args:
        current_user: Current active user

    Returns:
        Superuser

    Raises:
        ForbiddenError: If user is not a superuser
    """
    from app.core.exceptions import ForbiddenError

    if not current_user.is_superuser:
        raise ForbiddenError(message="Not enough permissions")
    return current_user
```

## Step 6: Create Authentication Endpoints

Create `app/api/v1/endpoints/auth.py`:

```python
"""Authentication endpoints."""

from datetime import timedelta

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User, UserCreate
from app.schemas.auth import Token

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Login endpoint to get access token.

    Args:
        form_data: OAuth2 password request form (username=email, password)

    Returns:
        Access token

    Raises:
        UnauthorizedError: If credentials are invalid
    """
    # TODO: Replace with actual database lookup
    # user = await user_repository.get_by_email(form_data.username)
    # if not user or not verify_password(form_data.password, user.hashed_password):
    #     raise UnauthorizedError(message="Incorrect email or password")

    # For now, use a mock check (replace with database)
    if form_data.username != "test@example.com" or form_data.password != "testpass":
        raise UnauthorizedError(message="Incorrect email or password")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    logger.info("user_logged_in", email=form_data.username)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate) -> User:
    """
    Register a new user.

    Args:
        user_data: User registration data

    Returns:
        Created user (without password)

    Raises:
        ValidationError: If user already exists
    """
    # TODO: Replace with actual database operations
    # Check if user exists
    # existing_user = await user_repository.get_by_email(user_data.email)
    # if existing_user:
    #     raise ValidationError(message="Email already registered")

    # Hash password
    hashed_password = get_password_hash(user_data.password)

    # Create user in database
    # user = await user_repository.create(user_data, hashed_password)

    # For now, return mock user
    user = User(
        id=1,
        email=user_data.email,
        full_name=user_data.full_name,
        is_active=user_data.is_active,
        is_superuser=user_data.is_superuser,
    )

    logger.info("user_registered", email=user_data.email)
    return user


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user information
    """
    return current_user
```

## Step 7: Update Router

Update `app/api/v1/router.py` to include auth routes:

```python
from app.api.v1.endpoints import auth, health, items

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
```

## Step 8: Protect Routes

Update any routes that need authentication. For example, in `app/api/v1/endpoints/items.py`:

```python
from app.api.dependencies import get_current_active_user
from app.models.user import User

@router.post("/", response_model=Item, status_code=201)
async def create_item(
    item: ItemCreate,
    current_user: User = Depends(get_current_active_user),
) -> Item:
    """Create a new item (requires authentication)."""
    # ... implementation ...
```

## Step 9: Add Database Support

When ready, add database models and repositories:

1. **Install SQLAlchemy**: `pip install sqlalchemy`

2. **Create database models** in `app/models/db/user.py`:
   - SQLAlchemy User model
   - Database session management

3. **Create user repository** in `app/repositories/user_repository.py`:
   - `get_by_email()`
   - `create()`
   - `get_by_id()`

4. **Update dependencies** to use database:
   - Replace mock user lookups with database queries
   - Add database session dependency

## Step 10: Testing Authentication

Create `tests/test_auth.py`:

```python
"""Tests for authentication endpoints."""

from fastapi.testclient import TestClient


def test_login_success(client: TestClient) -> None:
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpass"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient) -> None:
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_get_current_user(client: TestClient) -> None:
    """Test getting current user info."""
    # First login to get token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpass"},
    )
    token = login_response.json()["access_token"]

    # Use token to get user info
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data


def test_protected_route_without_token(client: TestClient) -> None:
    """Test accessing protected route without token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
```

## Summary

You've now added:
- ✅ Password hashing and verification
- ✅ JWT token creation and validation
- ✅ User models and schemas
- ✅ Authentication endpoints (login, register, me)
- ✅ Protected route dependencies
- ✅ Example protected routes

## Next Steps

1. **Add database**: Replace mock user lookups with actual database queries
2. **Add user management**: CRUD operations for users
3. **Add roles/permissions**: More granular access control
4. **Add token refresh**: Refresh token mechanism
5. **Add email verification**: Verify user emails
6. **Add password reset**: Password reset flow
7. **Add rate limiting**: Prevent brute force attacks
8. **Add 2FA**: Two-factor authentication

## Security Considerations

- Always use HTTPS in production
- Store secrets securely (use environment variables or secret management)
- Implement rate limiting on login endpoints
- Use strong password requirements
- Consider implementing account lockout after failed attempts
- Regularly rotate secrets
- Use secure session management
- Implement proper CORS policies
- Validate and sanitize all inputs
