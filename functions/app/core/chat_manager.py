from app.services.rag_service import RAGService
from app.services.llm_service import llm_service
from app.db.vector_store import VectorStoreManager
from app.models.schemas import ChatRequest, ChatResponse
from langchain_core.messages import HumanMessage, AIMessage
from fastapi.concurrency import run_in_threadpool
import asyncio
import time
import uuid
from app.core.vector_store_singleton import vector_store




RAG_TIMEOUT = 2.0   # seconds
LLM_TIMEOUT = 8.0   # seconds


class ChatManager:
    """Manages the core chat flow, integrating RAG and LLM services."""

    def __init__(self):
        
        self.rag_service = RAGService(vector_store)
        self.llm_service = llm_service
       

    async def process_chat(self, chat_request: ChatRequest) -> ChatResponse:
        request_id = uuid.uuid4().hex[:8]
        print(f"🧩 process_chat START [{request_id}]")

        user_message = chat_request.message

        # 1. Convert history
        history_messages = []
        for msg in chat_request.history:
            if msg.role == "user":
                history_messages.append(HumanMessage(content=msg.content))
            else:
                history_messages.append(AIMessage(content=msg.content))

        # 2. RAG with timeout
        try:
            rag_start = time.perf_counter()
            context, sources = await asyncio.wait_for(
                run_in_threadpool(
                    self.rag_service.get_relevant_context,
                    user_message
                ),
                timeout=RAG_TIMEOUT
            )
            print(f"⏱ RAG time: {time.perf_counter() - rag_start:.2f}s")
        except asyncio.TimeoutError:
            print("⚠️ RAG timeout — proceeding without context")
            context = ""
            sources = []

        # 3. LLM with timeout
        try:
            llm_start = time.perf_counter()
            reply = await asyncio.wait_for(
                run_in_threadpool(
                    self.llm_service.generate_response,
                    question=user_message,
                    context=context,
                    history=history_messages
                ),
                timeout=LLM_TIMEOUT
            )
            print(f"⏱ LLM time: {time.perf_counter() - llm_start:.2f}s")
        except asyncio.TimeoutError:
            print("❌ LLM timeout")
            reply = "The assistant is currently busy. Please try again in a moment."

        print(f"🧩 process_chat END [{request_id}]")
        return ChatResponse(reply=reply, sources=sources)
    


    

chat_manager = ChatManager()
