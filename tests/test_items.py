"""Tests for items endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_create_item(client: TestClient) -> None:
    """Test creating a new item."""
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
    }
    response = client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["id"] is not None


def test_get_item(client: TestClient) -> None:
    """Test retrieving an item."""
    # First create an item
    item_data = {"name": "Test Item", "price": 10.99}
    create_response = client.post("/api/v1/items/", json=item_data)
    item_id = create_response.json()["id"]

    # Then retrieve it
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == item_data["name"]


def test_get_nonexistent_item(client: TestClient) -> None:
    """Test retrieving a non-existent item."""
    response = client.get("/api/v1/items/99999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


def test_list_items(client: TestClient) -> None:
    """Test listing all items."""
    # Create a few items
    for i in range(3):
        client.post("/api/v1/items/", json={"name": f"Item {i}", "price": 10.0 + i})

    # List all items
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_update_item(client: TestClient) -> None:
    """Test updating an item."""
    # Create an item
    item_data = {"name": "Original Name", "price": 10.99}
    create_response = client.post("/api/v1/items/", json=item_data)
    item_id = create_response.json()["id"]

    # Update it
    update_data = {"name": "Updated Name", "price": 20.99}
    response = client.put(f"/api/v1/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]


def test_delete_item(client: TestClient) -> None:
    """Test deleting an item."""
    # Create an item
    item_data = {"name": "To Delete", "price": 10.99}
    create_response = client.post("/api/v1/items/", json=item_data)
    item_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404
