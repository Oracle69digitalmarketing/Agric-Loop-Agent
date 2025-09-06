from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
import datetime

class FarmerInputBase(BaseModel):
    """
    Base model for any input received from a farmer.
    """
    farmer_id: str = Field(
        ...,
        description="Unique identifier for the farmer, e.g., WhatsApp number.",
        examples=["+14155552671"]
    )
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="The timestamp when the input was received."
    )

class TextInput(FarmerInputBase):
    """
    Schema for a text-based input from a farmer.
    """
    text: str = Field(
        ...,
        min_length=1,
        description="The text message content from the farmer.",
        examples=["My crops are looking yellow, what should I do?"]
    )

class ImageInput(FarmerInputBase):
    """
    Schema for an image-based input from a farmer.
    """
    image_url: HttpUrl = Field(
        ...,
        description="A valid URL pointing to the uploaded image of the crop or issue.",
        examples=["https://example.com/images/crop_disease.jpg"]
    )
    caption: Optional[str] = Field(
        None,
        description="An optional caption provided by the farmer for the image.",
        examples=["This is what the leaves look like up close."]
    )

class VoiceInput(FarmerInputBase):
    """
    Schema for a voice-based input from a farmer.
    """
    voice_url: HttpUrl = Field(
        ...,
        description="A valid URL pointing to the uploaded voice note file.",
        examples=["https://example.com/voice/farmer_query.wav"]
    )
    transcript: Optional[str] = Field(
        None,
        description="An optional transcript of the voice note, if available."
    )
