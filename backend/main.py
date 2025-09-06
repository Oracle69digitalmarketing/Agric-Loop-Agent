from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import SessionLocal, engine
from . import services

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agri-Loop Agent API",
    description="The backend service for the Agri-Loop Agent, providing autonomous, data-driven support to smallholder farmers.",
    version="0.1.0",
)

# --- API Router ---
# All API endpoints will be defined on this router and mounted under /api
router = APIRouter(prefix="/api")

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---

@router.get("/")
def read_root():
    return {"message": "Welcome to the Agri-Loop Agent API"}

@router.post("/ingest/text", status_code=status.HTTP_201_CREATED, response_model=schemas.FarmerInput)
def ingest_text(data: schemas.TextInputCreate, db: Session = Depends(get_db)):
    db_input = models.FarmerInput(
        farmer_id=data.farmer_id, input_type='text', text_content=data.text
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input

@router.post("/ingest/image", status_code=status.HTTP_201_CREATED, response_model=schemas.FarmerInput)
def ingest_image(data: schemas.ImageInputCreate, db: Session = Depends(get_db)):
    db_input = models.FarmerInput(
        farmer_id=data.farmer_id, input_type='image', media_url=str(data.image_url), caption=data.caption
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input

@router.post("/ingest/voice", status_code=status.HTTP_201_CREATED, response_model=schemas.FarmerInput)
def ingest_voice(data: schemas.VoiceInputCreate, db: Session = Depends(get_db)):
    db_input = models.FarmerInput(
        farmer_id=data.farmer_id, input_type='voice', media_url=str(data.voice_url), transcript=data.transcript
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return db_input

@router.get("/inputs", response_model=List[schemas.FarmerInput])
def get_all_inputs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inputs = db.query(models.FarmerInput).offset(skip).limit(limit).all()
    return inputs

@router.post("/diagnose/{input_id}", status_code=status.HTTP_200_OK)
def diagnose_input(input_id: int, db: Session = Depends(get_db)):
    db_input = db.query(models.FarmerInput).filter(models.FarmerInput.id == input_id).first()
    if not db_input:
        raise HTTPException(status_code=404, detail="Farmer input not found")

    if db_input.input_type != 'text' or not db_input.text_content:
        raise HTTPException(
            status_code=400, detail="Diagnosis is currently only supported for text inputs."
        )

    diagnosis = services.llm_service.get_diagnosis(db_input.text_content)
    action_result = services.action_service.send_whatsapp_message(
        farmer_id=db_input.farmer_id, message=diagnosis
    )
    return {
        "input_id": input_id,
        "diagnosis": diagnosis,
        "action_taken": action_result
    }

# Include the API router in the main app
app.include_router(router)

# --- Static Files Mount ---
# This must be the last thing in the file.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
