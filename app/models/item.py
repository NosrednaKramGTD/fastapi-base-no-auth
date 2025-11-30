"""Item domain model (example - replace with your domain models)."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base item model with common fields."""

    name: str = Field(..., description="Item name", min_length=1, max_length=100)
    description: Optional[str] = Field(
        None, description="Item description", max_length=500
    )
    price: float = Field(..., description="Item price", gt=0)


class ItemCreate(ItemBase):
    """Model for creating a new item."""

    pass


class ItemUpdate(BaseModel):
    """Model for updating an item (all fields optional)."""

    name: Optional[str] = Field(
        None, description="Item name", min_length=1, max_length=100
    )
    description: Optional[str] = Field(
        None, description="Item description", max_length=500
    )
    price: Optional[float] = Field(None, description="Item price", gt=0)


class Item(ItemBase):
    """Complete item model with ID and timestamps."""

    id: int = Field(..., description="Item identifier")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Example Item",
                "description": "This is an example item",
                "price": 19.99,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
            }
        }
    }
