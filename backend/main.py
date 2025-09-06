from fastapi import FastAPI, status
from typing import List, Union

from . import schemas

app = FastAPI(
    title="Agri-Loop Agent API",
    description="The backend service for the Agri-Loop Agent, providing autonomous, data-driven support to smallholder farmers.",
    version="0.1.0",
)

# In-memory database placeholder.
# In a real application, this would be a connection to TiDB.
db_placeholder: List[dict] = []


@app.get("/")
def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Agri-Loop Agent API"}


@app.post("/ingest/text", status_code=status.HTTP_201_CREATED)
def ingest_text(data: schemas.TextInput):
    """
    Endpoint to ingest a text message from a farmer.
    """
    db_placeholder.append(data.model_dump())
    return {"message": f"Text input from {data.farmer_id} received successfully."}


@app.post("/ingest/image", status_code=status.HTTP_201_CREATED)
def ingest_image(data: schemas.ImageInput):
    """
    Endpoint to ingest an image submission from a farmer.
    """
    db_placeholder.append(data.model_dump())
    return {"message": f"Image input from {data.farmer_id} received successfully."}


@app.post("/ingest/voice", status_code=status.HTTP_201_CREATED)
def ingest_voice(data: schemas.VoiceInput):
    """
    Endpoint to ingest a voice message from a farmer.
    """
    db_placeholder.append(data.model_dump())
    return {"message": f"Voice input from {data.farmer_id} received successfully."}


@app.get("/ingest/view", response_model=List[dict])
def view_ingested_data():
    """
    A simple endpoint to view the data currently held in the in-memory database.
    (For debugging purposes).
    """
    return db_placeholder


@app.post("/debug/clear-db", status_code=status.HTTP_200_OK, include_in_schema=False)
def clear_db():
    """
    Endpoint to clear the in-memory database.
    (For testing purposes only. Not included in the public API schema.)
    """
    db_placeholder.clear()
    return {"message": "In-memory database cleared."}
