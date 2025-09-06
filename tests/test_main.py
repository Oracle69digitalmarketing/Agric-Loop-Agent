from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from backend.main import app, get_db
from backend.database import Base
from backend import models

# --- Test Database Setup ---

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override to use the in-memory database during tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the dependency override to the FastAPI app
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """
    Pytest fixture to create a fresh, empty database for each test function.
    `autouse=True` ensures this runs before every test.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

# --- Tests ---

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Agri-Loop Agent API"}

def test_ingest_text():
    """Test successful ingestion of a text message."""
    test_payload = {"farmer_id": "+15551234567", "text": "My corn is looking sick."}
    response = client.post("/ingest/text", json=test_payload)
    assert response.status_code == 201

    data = response.json()
    assert data["farmer_id"] == test_payload["farmer_id"]
    assert data["text_content"] == test_payload["text"]
    assert data["input_type"] == "text"
    assert "id" in data
    assert "timestamp" in data

    # Verify it was saved by querying the /inputs endpoint
    response = client.get("/inputs")
    assert response.status_code == 200
    all_inputs = response.json()
    assert len(all_inputs) == 1
    assert all_inputs[0]["farmer_id"] == test_payload["farmer_id"]

def test_ingest_image():
    """Test successful ingestion of an image submission."""
    test_payload = {
        "farmer_id": "+15551234568",
        "image_url": "http://example.com/image.jpg",
        "caption": "Close up of the leaves"
    }
    response = client.post("/ingest/image", json=test_payload)
    assert response.status_code == 201

    data = response.json()
    assert data["farmer_id"] == test_payload["farmer_id"]
    assert data["media_url"] == test_payload["image_url"]
    assert data["caption"] == test_payload["caption"]
    assert data["input_type"] == "image"

    response = client.get("/inputs")
    assert len(response.json()) == 1

def test_ingest_voice():
    """Test successful ingestion of a voice message."""
    test_payload = {
        "farmer_id": "+15551234569",
        "voice_url": "http://example.com/voice.mp3",
        "transcript": "The leaves are turning brown."
    }
    response = client.post("/ingest/voice", json=test_payload)
    assert response.status_code == 201

    data = response.json()
    assert data["farmer_id"] == test_payload["farmer_id"]
    assert data["media_url"] == test_payload["voice_url"]
    assert data["transcript"] == test_payload["transcript"]
    assert data["input_type"] == "voice"

    response = client.get("/inputs")
    assert len(response.json()) == 1

def test_get_all_inputs_pagination():
    """Test pagination of the /inputs endpoint."""
    # Ingest 3 records
    client.post("/ingest/text", json={"farmer_id": "1", "text": "a"})
    client.post("/ingest/text", json={"farmer_id": "2", "text": "b"})
    client.post("/ingest/text", json={"farmer_id": "3", "text": "c"})

    # Test limit
    response = client.get("/inputs?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Test skip
    response = client.get("/inputs?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["farmer_id"] == "3"

def test_ingest_text_invalid_payload():
    """Test validation for invalid payload."""
    response = client.post("/ingest/text", json={"farmer_id": "+1"}) # Missing 'text'
    assert response.status_code == 422
