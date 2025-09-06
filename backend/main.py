from fastapi import FastAPI

app = FastAPI(
    title="Agri-Loop Agent API",
    description="The backend service for the Agri-Loop Agent, providing autonomous, data-driven support to smallholder farmers.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the Agri-Loop Agent API"}
