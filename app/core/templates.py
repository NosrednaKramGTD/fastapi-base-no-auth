"""Template rendering utilities for Jinja2."""

from pathlib import Path
from typing import Any, Dict

from fastapi import Request
from fastapi.templating import Jinja2Templates

# Template directory path
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def render_template(
    request: Request,
    template_name: str,
    context: Dict[str, Any] | None = None,
    status_code: int = 200,
) -> Any:
    """
    Render a Jinja2 template with context.

    Args:
        request: FastAPI request object
        template_name: Name of the template file
        context: Dictionary of variables to pass to template
        status_code: HTTP status code for the response

    Returns:
        TemplateResponse: Rendered template response
    """
    if context is None:
        context = {}

    # Add common context variables
    context.setdefault("request", request)

    return templates.TemplateResponse(
        name=template_name,
        context=context,
        status_code=status_code,
    )


def is_htmx_request(request: Request) -> bool:
    """
    Check if the request is from HTMX.

    Args:
        request: FastAPI request object

    Returns:
        bool: True if request is from HTMX
    """
    return request.headers.get("HX-Request") == "true"


def get_htmx_trigger(request: Request) -> str | None:
    """
    Get the HTMX trigger name from request headers.

    Args:
        request: FastAPI request object

    Returns:
        str | None: Trigger name or None
    """
    return request.headers.get("HX-Trigger")
