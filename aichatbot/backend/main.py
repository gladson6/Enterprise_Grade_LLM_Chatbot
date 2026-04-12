from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat

# Create the main FastAPI application instance
app = FastAPI(
    title="Company IT Chatbot API",
    description="API for the advanced RAG-based chatbot.",
    version="1.0.0"
)

# --- Middleware ---
# Configure CORS (Cross-Origin Resource Sharing) to allow the frontend
# to communicate with this backend.
# In a production environment, you should restrict the origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- API Routers ---
# Include the chat router. All routes defined in `app.api.chat`
# will be added to the application under the `/api/v1` prefix.
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Company IT Chatbot API. Visit /docs for documentation."}

