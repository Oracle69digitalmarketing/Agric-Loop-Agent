from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import SessionLocal, engine

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agri-Loop Agent API",
    description="The backend service for the Agri-Loop Agent, providing autonomous, data-driven support to smallholder farmers.",
    version="0.1.0",
)

# --- Dependency ---
def get_db():
    """
    Dependency that provides a database session for each request.
    This ensures that the session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API Endpoints ---

@app.get("/")
def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Agri-Loop Agent API"}


@app.post("/ingest/text", status_code=status.HTTP_201_CREATED, response_model=schemas.FarmerInput)
def ingest_text(data: schemas.TextInputCreate, db: Session = Depends(get_db)):
    """
    Endpoint to ingest a text message from a farmer and save it to the database.
    """
    db_input = models.FarmerInput(
        farmer_id=data.farmer_id,
        input_type='text',
        text_content=data.text
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input


@app.post("/ingest/image", status_code=status.HTTP_201_CREATED, response_model=schemas.FarmerInput)
def ingest_image(data: schemas.ImageInputCreate, db: Session = Depends(get_db)):
    """
    Endpoint to ingest an image submission from a farmer and save it to the database.
    """
    db_input = models.FarmerInput(
        farmer_id=data.farmer_id,
        input_type='image',
        media_url=str(data.image_url),
        caption=data.caption
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input


@app.post("/ingest/voice", status_code=status.HTTP_201_CREATED, response_model=schemas.FarmerInput)
def ingest_voice(data: schemas.VoiceInputCreate, db: Session = Depends(get_db)):
    """
    Endpoint to ingest a voice message from a farmer and save it to the database.
    """
    db_input = models.FarmerInput(
        farmer_id=data.farmer_id,
        input_type='voice',
        media_url=str(data.voice_url),
        transcript=data.transcript
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input


@app.get("/inputs", response_model=List[schemas.FarmerInput])
def get_all_inputs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all farmer inputs from the database with pagination.
    """
    inputs = db.query(models.FarmerInput).offset(skip).limit(limit).all()
    return inputs
