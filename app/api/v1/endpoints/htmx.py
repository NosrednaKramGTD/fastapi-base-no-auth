"""HTMX templating endpoints."""

import structlog
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.core.exceptions import NotFoundError
from app.core.templates import is_htmx_request, render_template
from app.models.item import Item

logger = structlog.get_logger(__name__)
router = APIRouter()

# In-memory storage for example (replace with database)
_items_db: dict[int, Item] = {}
_next_id = 1


@router.get("/", response_class=HTMLResponse)
async def htmx_index(request: Request) -> HTMLResponse:
    """
    HTMX index page.

    Args:
        request: FastAPI request object

    Returns:
        HTMLResponse: Rendered index page
    """
    from app.core.config import settings

    return render_template(
        request=request,
        template_name="index.html",
        context={"project_name": settings.PROJECT_NAME},
    )


@router.get("/example/swap", response_class=HTMLResponse)
async def htmx_example_swap(request: Request) -> HTMLResponse:
    """
    Example HTMX endpoint that swaps content.

    Args:
        request: FastAPI request object

    Returns:
        HTMLResponse: Rendered partial template
    """
    if not is_htmx_request(request):
        # If not HTMX request, return full page or redirect
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/htmx/")

    return HTMLResponse(
        content="""
        <div class="p-4 bg-green-100 border border-green-400 rounded">
            <p class="text-green-800">
                ✅ Content loaded via HTMX! This content was swapped without a full page reload.
            </p>
            <p class="text-sm text-green-600 mt-2">
                Current time: <span id="time"></span>
            </p>
            <script>
                document.getElementById('time').textContent = new Date().toLocaleTimeString();
            </script>
        </div>
        """
    )


@router.post("/example/form", response_class=HTMLResponse)
async def htmx_example_form(
    request: Request, name: str = Form(...)
) -> HTMLResponse:
    """
    Example HTMX form submission endpoint.

    Args:
        request: FastAPI request object
        name: Form field value

    Returns:
        HTMLResponse: Rendered response
    """
    if not is_htmx_request(request):
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/htmx/")

    logger.info("form_submitted", name=name)

    return HTMLResponse(
        content=f"""
        <div class="p-4 bg-blue-100 border border-blue-400 rounded">
            <p class="text-blue-800">
                ✅ Form submitted successfully! Hello, <strong>{name}</strong>!
            </p>
        </div>
        """
    )


@router.get("/items", response_class=HTMLResponse)
async def htmx_list_items(request: Request) -> HTMLResponse:
    """
    List items as HTMX partial.

    Args:
        request: FastAPI request object

    Returns:
        HTMLResponse: Rendered item list partial
    """
    items = list(_items_db.values())
    logger.info("listing_items_htmx", count=len(items))

    return render_template(
        request=request,
        template_name="htmx/partials/item_list.html",
        context={"items": items},
    )


@router.get("/items/{item_id}", response_class=HTMLResponse)
async def htmx_get_item(request: Request, item_id: int) -> HTMLResponse:
    """
    Get item detail as HTMX partial.

    Args:
        request: FastAPI request object
        item_id: Item identifier

    Returns:
        HTMLResponse: Rendered item detail partial

    Raises:
        NotFoundError: If item is not found
    """
    if item_id not in _items_db:
        raise NotFoundError(message=f"Item {item_id} not found")

    item = _items_db[item_id]
    logger.info("retrieving_item_htmx", item_id=item_id)

    return render_template(
        request=request,
        template_name="htmx/partials/item_detail.html",
        context={"item": item},
    )


@router.post("/items", response_class=HTMLResponse)
async def htmx_create_item(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
) -> HTMLResponse:
    """
    Create item via HTMX form.

    Args:
        request: FastAPI request object
        name: Item name
        description: Item description
        price: Item price

    Returns:
        HTMLResponse: Rendered item list partial (refreshed)
    """
    global _next_id

    if not is_htmx_request(request):
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/htmx/")

    new_item = Item(
        id=_next_id,
        name=name,
        description=description if description else None,
        price=price,
    )
    _items_db[_next_id] = new_item
    _next_id += 1

    logger.info("item_created_htmx", item_id=new_item.id)

    # Return updated list
    items = list(_items_db.values())
    return render_template(
        request=request,
        template_name="htmx/partials/item_list.html",
        context={"items": items},
    )


@router.delete("/items/{item_id}", response_class=HTMLResponse)
async def htmx_delete_item(request: Request, item_id: int) -> HTMLResponse:
    """
    Delete item via HTMX.

    Args:
        request: FastAPI request object
        item_id: Item identifier

    Returns:
        HTMLResponse: Empty response (item removed from DOM)

    Raises:
        NotFoundError: If item is not found
    """
    if not is_htmx_request(request):
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/htmx/")

    if item_id not in _items_db:
        raise NotFoundError(message=f"Item {item_id} not found")

    del _items_db[item_id]
    logger.info("item_deleted_htmx", item_id=item_id)

    # Return empty content (HTMX will remove the element)
    return HTMLResponse(content="")


@router.get("/items/form", response_class=HTMLResponse)
async def htmx_item_form(request: Request) -> HTMLResponse:
    """
    Get item creation form as HTMX partial.

    Args:
        request: FastAPI request object

    Returns:
        HTMLResponse: Rendered form partial
    """
    return HTMLResponse(
        content="""
        <div class="border rounded p-4 bg-white">
            <h3 class="text-lg font-semibold mb-4">Create New Item</h3>
            <form
                hx-post="/htmx/items"
                hx-target="#items-list"
                hx-swap="innerHTML"
                hx-on::after-request="this.reset()">
                <div class="mb-4">
                    <label for="item-name" class="block text-sm font-medium mb-2">Name:</label>
                    <input
                        type="text"
                        id="item-name"
                        name="name"
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md">
                </div>
                <div class="mb-4">
                    <label for="item-description" class="block text-sm font-medium mb-2">Description:</label>
                    <textarea
                        id="item-description"
                        name="description"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md"></textarea>
                </div>
                <div class="mb-4">
                    <label for="item-price" class="block text-sm font-medium mb-2">Price:</label>
                    <input
                        type="number"
                        id="item-price"
                        name="price"
                        step="0.01"
                        min="0"
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md">
                </div>
                <button
                    type="submit"
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                    Create Item
                </button>
            </form>
        </div>
        """
    )
