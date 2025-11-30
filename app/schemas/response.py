"""Common response schemas."""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Standard message response schema."""

    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Operation completed successfully",
            }
        }
    }
