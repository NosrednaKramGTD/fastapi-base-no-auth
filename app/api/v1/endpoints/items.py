"""Example items endpoint (replace with your domain logic)."""

from typing import List

import structlog
from fastapi import APIRouter, HTTPException

from app.core.exceptions import NotFoundError
from app.models.item import Item, ItemCreate, ItemUpdate
from app.schemas.response import MessageResponse

logger = structlog.get_logger(__name__)
router = APIRouter()

# In-memory storage for example (replace with database)
_items_db: dict[int, Item] = {}
_next_id = 1


@router.get("/", response_model=List[Item])
async def list_items() -> List[Item]:
    """
    List all items.

    Returns:
        List of items
    """
    logger.info("listing_items", count=len(_items_db))
    return list(_items_db.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    """
    Get a specific item by ID.

    Args:
        item_id: Item identifier

    Returns:
        Item details

    Raises:
        NotFoundError: If item is not found
    """
    if item_id not in _items_db:
        raise NotFoundError(message=f"Item {item_id} not found")

    logger.info("retrieving_item", item_id=item_id)
    return _items_db[item_id]


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate) -> Item:
    """
    Create a new item.

    Args:
        item: Item creation data

    Returns:
        Created item
    """
    global _next_id

    new_item = Item(id=_next_id, **item.model_dump())
    _items_db[_next_id] = new_item
    _next_id += 1

    logger.info("item_created", item_id=new_item.id)
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate) -> Item:
    """
    Update an existing item.

    Args:
        item_id: Item identifier
        item_update: Item update data

    Returns:
        Updated item

    Raises:
        NotFoundError: If item is not found
    """
    if item_id not in _items_db:
        raise NotFoundError(message=f"Item {item_id} not found")

    existing_item = _items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    updated_item = existing_item.model_copy(update=update_data)
    _items_db[item_id] = updated_item

    logger.info("item_updated", item_id=item_id)
    return updated_item


@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_item(item_id: int) -> MessageResponse:
    """
    Delete an item.

    Args:
        item_id: Item identifier

    Returns:
        Success message

    Raises:
        NotFoundError: If item is not found
    """
    if item_id not in _items_db:
        raise NotFoundError(message=f"Item {item_id} not found")

    del _items_db[item_id]
    logger.info("item_deleted", item_id=item_id)

    return MessageResponse(message=f"Item {item_id} deleted successfully")
