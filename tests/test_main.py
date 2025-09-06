from fastapi.testclient import TestClient
import pytest
from backend.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Fixture to clear the database before each test is run.
    `autouse=True` ensures it's used for every test function.
    """
    client.post("/debug/clear-db")
    yield
    client.post("/debug/clear-db")

def test_read_root():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Agri-Loop Agent API"}

def test_ingest_text_success():
    """
    Test successful ingestion of a text message.
    """
    test_payload = {"farmer_id": "+15551234567", "text": "My corn is looking sick."}
    response = client.post("/ingest/text", json=test_payload)
    assert response.status_code == 201
    assert response.json() == {"message": f"Text input from {test_payload['farmer_id']} received successfully."}

    # Verify data was stored
    stored_data = client.get("/ingest/view").json()
    assert len(stored_data) == 1
    assert stored_data[0]["farmer_id"] == test_payload["farmer_id"]
    assert stored_data[0]["text"] == test_payload["text"]

def test_ingest_image_success():
    """
    Test successful ingestion of an image submission.
    """
    test_payload = {
        "farmer_id": "+15551234568",
        "image_url": "https://example.com/image.jpg",
        "caption": "Close up of the leaves"
    }
    response = client.post("/ingest/image", json=test_payload)
    assert response.status_code == 201
    assert response.json() == {"message": f"Image input from {test_payload['farmer_id']} received successfully."}

    # Verify data was stored
    stored_data = client.get("/ingest/view").json()
    assert len(stored_data) == 1
    assert stored_data[0]["farmer_id"] == test_payload["farmer_id"]
    assert stored_data[0]["image_url"] == test_payload["image_url"]
    assert stored_data[0]["caption"] == test_payload["caption"]

def test_ingest_voice_success():
    """
    Test successful ingestion of a voice message.
    """
    test_payload = {
        "farmer_id": "+15551234569",
        "voice_url": "https://example.com/voice.mp3"
    }
    response = client.post("/ingest/voice", json=test_payload)
    assert response.status_code == 201
    assert response.json() == {"message": f"Voice input from {test_payload['farmer_id']} received successfully."}

    # Verify data was stored
    stored_data = client.get("/ingest/view").json()
    assert len(stored_data) == 1
    assert stored_data[0]["farmer_id"] == test_payload["farmer_id"]
    assert stored_data[0]["voice_url"] == test_payload["voice_url"]

def test_ingest_text_invalid_payload():
    """
    Test ingestion of a text message with an invalid payload.
    """
    # Missing 'text' field
    test_payload = {"farmer_id": "+15551234567"}
    response = client.post("/ingest/text", json=test_payload)
    assert response.status_code == 422  # Unprocessable Entity
