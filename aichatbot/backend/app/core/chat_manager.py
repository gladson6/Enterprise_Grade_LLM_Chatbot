from app.services.rag_service import RAGService
from app.services.llm_service import llm_service
from app.db.vector_store import VectorStoreManager
from app.models.schemas import ChatRequest, ChatResponse
from langchain_core.messages import HumanMessage, AIMessage

class ChatManager:
    """Manages the core chat flow, integrating RAG and LLM services."""
    
    def __init__(self):
        vector_store_manager = VectorStoreManager()
        self.rag_service = RAGService(vector_store_manager)
        self.llm_service = llm_service

    def process_chat(self, chat_request: ChatRequest) -> ChatResponse:
        user_message = chat_request.message
        
        # 1. Convert chat history to LangChain message format
        history_messages = []
        for msg in chat_request.history:
            if msg.role == 'user':
                history_messages.append(HumanMessage(content=msg.content))
            else:
                history_messages.append(AIMessage(content=msg.content))

        # 2. Retrieve relevant context
        context, sources = self.rag_service.get_relevant_context(user_message)

        # 3. Generate a response
        reply = self.llm_service.generate_response(
            question=user_message,
            context=context,
            history=history_messages
        )

        # 4. Construct and return the final response
        return ChatResponse(reply=reply, sources=sources)

chat_manager = ChatManager()
