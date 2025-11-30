# HTMX Templating Guide

This guide explains how to use HTMX templating in your FastAPI application.

## Overview

HTMX allows you to build dynamic web applications with minimal JavaScript by using HTML attributes to make AJAX requests, trigger CSS transitions, and update parts of the page directly from HTML responses.

## Features

- ✅ **Jinja2 Templates**: Full Jinja2 templating support
- ✅ **HTMX Integration**: HTMX library included via CDN
- ✅ **Partial Templates**: Reusable template fragments for HTMX responses
- ✅ **Error Handling**: HTMX-aware error responses
- ✅ **Form Handling**: Easy form submission with HTMX

## Project Structure

```
templates/
├── base.html              # Base template with HTMX
├── index.html             # Main index page
└── htmx/
    └── partials/         # HTMX partial templates
        ├── item_list.html
        └── item_detail.html
```

## Basic Usage

### 1. Creating Templates

Templates are stored in the `templates/` directory. The base template includes HTMX:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/htmx.org@2.0.3"></script>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### 2. Rendering Templates

Use the `render_template` utility function:

```python
from fastapi import Request
from app.core.templates import render_template

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return render_template(
        request=request,
        template_name="index.html",
        context={"project_name": "My App"},
    )
```

### 3. HTMX Attributes

Use HTMX attributes to make dynamic requests:

```html
<!-- Simple GET request -->
<button
    hx-get="/api/v1/htmx/example/swap"
    hx-target="#result"
    hx-swap="innerHTML">
    Load Content
</button>
<div id="result"></div>
```

### 4. Form Submission

Submit forms without page reload:

```html
<form
    hx-post="/api/v1/htmx/example/form"
    hx-target="#form-result"
    hx-swap="innerHTML">
    <input type="text" name="name" required>
    <button type="submit">Submit</button>
</form>
<div id="form-result"></div>
```

### 5. Partial Templates

Create reusable partial templates for HTMX responses:

```html
<!-- templates/htmx/partials/item_list.html -->
<div class="space-y-2">
    {% for item in items %}
    <div class="border rounded p-3">
        <h4>{{ item.name }}</h4>
        <p>${{ item.price }}</p>
    </div>
    {% endfor %}
</div>
```

Return partials from HTMX endpoints:

```python
@router.get("/items", response_class=HTMLResponse)
async def list_items(request: Request):
    items = get_all_items()
    return render_template(
        request=request,
        template_name="htmx/partials/item_list.html",
        context={"items": items},
    )
```

## Common Patterns

### Content Swap

Replace content in a target element:

```html
<button
    hx-get="/api/v1/htmx/data"
    hx-target="#content"
    hx-swap="innerHTML">
    Load Data
</button>
<div id="content">Initial content</div>
```

### Form Submission with Reset

Submit form and reset it after success:

```html
<form
    hx-post="/api/v1/htmx/create"
    hx-target="#list"
    hx-swap="innerHTML"
    hx-on::after-request="this.reset()">
    <!-- form fields -->
</form>
```

### Delete with Confirmation

Delete item with confirmation dialog:

```html
<button
    hx-delete="/api/v1/htmx/items/{{ item.id }}"
    hx-target="closest div"
    hx-swap="outerHTML"
    hx-confirm="Are you sure?">
    Delete
</button>
```

### Loading Indicators

Show loading state during requests:

```html
<button
    hx-get="/api/v1/htmx/data"
    hx-target="#result"
    hx-indicator="#spinner">
    Load
</button>
<div id="spinner" class="htmx-indicator">Loading...</div>
<div id="result"></div>
```

### Polling

Auto-refresh content periodically:

```html
<div
    hx-get="/api/v1/htmx/status"
    hx-trigger="every 5s"
    hx-swap="innerHTML">
    Status will update every 5 seconds
</div>
```

### Trigger Events

Trigger custom events:

```html
<button
    hx-post="/api/v1/htmx/action"
    hx-trigger="click"
    hx-on::after-request="alert('Done!')">
    Action
</button>
```

## Detecting HTMX Requests

Check if a request is from HTMX:

```python
from app.core.templates import is_htmx_request

@router.get("/endpoint")
async def my_endpoint(request: Request):
    if is_htmx_request(request):
        # Return HTML partial
        return render_template(...)
    else:
        # Return full page or redirect
        return RedirectResponse(url="/")
```

## Error Handling

The error handler automatically returns HTML for HTMX requests:

```python
# In your endpoint
raise NotFoundError(message="Item not found")

# HTMX requests get HTML error response
# API requests get JSON error response
```

## Best Practices

### 1. Use Partial Templates

Keep HTMX responses as small HTML fragments:

```python
# Good: Return partial template
return render_template(
    request=request,
    template_name="htmx/partials/item.html",
    context={"item": item},
)

# Avoid: Returning full page HTML in HTMX responses
```

### 2. Separate HTMX and API Endpoints

Keep HTMX endpoints separate from JSON API endpoints:

```python
# HTMX endpoint
@router.get("/htmx/items", response_class=HTMLResponse)
async def htmx_list_items(request: Request):
    ...

# API endpoint
@router.get("/api/v1/items")
async def api_list_items():
    ...
```

### 3. Use Semantic HTML

Use appropriate HTML elements:

```html
<!-- Good -->
<button hx-get="/endpoint">Action</button>
<a hx-get="/endpoint">Link</a>

<!-- Avoid -->
<div onclick="..." hx-get="/endpoint">Click me</div>
```

### 4. Handle Loading States

Provide visual feedback during requests:

```html
<button
    hx-get="/endpoint"
    hx-indicator="#spinner">
    Load
</button>
<div id="spinner" class="htmx-indicator">
    <span>Loading...</span>
</div>
```

### 5. Validate on Server

Always validate on the server, even with HTMX:

```python
@router.post("/htmx/create")
async def create_item(
    request: Request,
    name: str = Form(...),
    price: float = Form(..., gt=0),
):
    # Server-side validation
    if not name or len(name) < 3:
        raise ValidationError(message="Name too short")
    ...
```

## HTMX Headers

Access HTMX-specific headers:

```python
from app.core.templates import is_htmx_request, get_htmx_trigger

@router.get("/endpoint")
async def endpoint(request: Request):
    if is_htmx_request(request):
        trigger = get_htmx_trigger(request)
        # Handle HTMX-specific logic
```

Available HTMX headers:
- `HX-Request`: Always "true" for HTMX requests
- `HX-Trigger`: Name of the element that triggered the request
- `HX-Trigger-Name`: Name attribute of the triggering element
- `HX-Target`: ID of the target element
- `HX-Current-URL`: Current URL of the browser

## Examples

See the example endpoints in `app/api/v1/endpoints/htmx.py` for complete working examples:

- Content swapping
- Form submission
- Dynamic lists
- Item CRUD operations
- Error handling

## Resources

- [HTMX Documentation](https://htmx.org/docs/)
- [HTMX Examples](https://htmx.org/examples/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
