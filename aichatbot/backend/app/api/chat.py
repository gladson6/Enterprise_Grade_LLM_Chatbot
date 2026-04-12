from fastapi import APIRouter, HTTPException, Body, BackgroundTasks
from app.models.schemas import ChatRequest, ChatResponse, Lead
from app.core.chat_manager import chat_manager
from app.services.email_service import email_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(request: ChatRequest = Body(...)):
    """Handles incoming chat messages and returns the bot's RAG-based reply."""
    try:
        response = chat_manager.process_chat(request)
        return response
    except Exception as e:
        print(f"An error occurred during chat processing: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@router.post("/lead")
async def capture_lead(lead: Lead, background_tasks: BackgroundTasks):
    """
    Captures lead information, prints it, and sends an email notification
    in the background if email is configured.
    """
    print(f"Received new lead: {lead.model_dump_json(indent=2)}")
    
    # Send email in the background to avoid blocking the API response
    if email_service.is_configured:
        background_tasks.add_task(email_service.send_lead_notification, lead)
    
    return {"message": "Thank you! We have received your information and will be in touch shortly."}
