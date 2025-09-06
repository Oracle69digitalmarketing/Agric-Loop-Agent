from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional
import datetime

# --- Schemas for Creating Data ---
# These schemas are used when receiving data from the API endpoints.

class FarmerInputCreateBase(BaseModel):
    """Base model for creating a new farmer input."""
    farmer_id: str = Field(..., description="Unique identifier for the farmer, e.g., WhatsApp number.")

class TextInputCreate(FarmerInputCreateBase):
    """Schema for creating a text input."""
    text: str = Field(..., min_length=1, description="The text message content from the farmer.")

class ImageInputCreate(FarmerInputCreateBase):
    """Schema for creating an image input."""
    image_url: HttpUrl = Field(..., description="A valid URL pointing to the uploaded image.")
    caption: Optional[str] = Field(None, description="An optional caption for the image.")

class VoiceInputCreate(FarmerInputCreateBase):
    """Schema for creating a voice input."""
    voice_url: HttpUrl = Field(..., description="A valid URL pointing to the uploaded voice note file.")
    transcript: Optional[str] = Field(None, description="An optional transcript of the voice note.")


# --- Schemas for Reading Data ---
# These schemas are used as response_models when returning data from the API.

class FarmerInput(BaseModel):
    """
    The main response model for a farmer input record read from the database.
    """
    id: int
    farmer_id: str
    timestamp: datetime.datetime
    input_type: str
    text_content: Optional[str] = None
    media_url: Optional[str] = None
    caption: Optional[str] = None
    transcript: Optional[str] = None

    # This tells Pydantic to read the data from ORM model attributes.
    model_config = ConfigDict(from_attributes=True)
