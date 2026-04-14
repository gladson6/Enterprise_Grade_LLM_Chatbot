import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_functions import https_fn
print("PYTHON EXECUTABLE:", sys.executable)

# importing time for calculating the cold start duration.
import time
START_TIME = time.time()
print("🔥 Cold start — process booting")

# Make the app folder importable
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

# --- FastAPI app ---
app = FastAPI(
    title="Company IT Chatbot API",
    description="API for the advanced RAG-based chatbot.",
    version="1.0.0",
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
from app.api import chat  # your chat router
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

# --- Root endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Company IT Chatbot API. Visit /docs for docs."}

# --- Firebase HTTPS function wrapper ---
# This is all Firebase needs. DO NOT use Mangum or uvicorn here.
@https_fn.on_request()
def fastapi_app(req: https_fn.Request):
    """
    Handles HTTP requests from Firebase and forwards them to FastAPI.
    Works with 2nd Gen Python Functions (no Cloud Run port needed).
    """
    from starlette.requests import Request
    from starlette.responses import Response
    from starlette.types import Receive, Scope, Send

    # Convert Firebase request to Starlette ASGI request
    scope: Scope = {
        "type": "http",
        "method": req.method,
        "headers": [(k.encode(), v.encode()) for k, v in req.headers.items()],
        "path": req.path,
        "query_string": req.query_string.encode(),
        "server": ("", 80),
        "client": ("", 0),
    }

    async def receive() -> dict:
        return {"type": "http.request", "body": req.get_data() or b"", "more_body": False}

    response_obj: Response = None

    async def send(message: dict):
        nonlocal response_obj
        if message["type"] == "http.response.start":
            response_obj = Response(status_code=message["status"])
        elif message["type"] == "http.response.body":
            response_obj.body = message.get("body", b"")

    import asyncio
    loop = asyncio.new_event_loop()
    loop.run_until_complete(app(scope, receive, send))
    return https_fn.Response(
        content=response_obj.body,
        status=response_obj.status_code,
        headers=dict(response_obj.headers),
    )
