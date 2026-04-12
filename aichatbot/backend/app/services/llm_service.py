from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings # Assuming your settings are managed here

class LLMService:
    """
    Service to interact with a model via OpenRouter API, using the latest LangChain package.
    """
    def __init__(self):
        # Instantiate the model using ChatOpenAI, configured for OpenRouter
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL_NAME, # e.g., "anthropic/claude-3-haiku"
            temperature=0.1,
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base=settings.OPENROUTER_BASE_URL, # Should be "https://openrouter.ai/api/v1"
            default_headers={
                "HTTP-Referer": settings.YOUR_SITE_URL, # Optional, but recommended by OpenRouter
                "X-Title": settings.YOUR_APP_NAME,      # Optional, but recommended by OpenRouter
            }
        )

        system_prompt = (
            "You are Kai, the KAITOZ AI assistant. "
            "Your style is: clear, concise, and professional. "
            "Rules:\n"
            "- If the user greets (hi, hello, hey, etc.), reply ONLY with: 'Hello! I’m the KAITOZ AI assistant. How can I help you today?'\n"
            "- If the user asks about your name, identity, or who you are, reply ONLY with: 'My name is Kai, and I am the KAITOZ AI assistant.'\n"
            "- For any question about services, features, or offerings, ALWAYS reply in bullet points.\n"
            "- Never use phrases like 'Based on the context,' 'According to the documents,' or similar.\n"
            "- Keep answers short (1–2 sentences max) unless listing items.\n"
            "- If the context does not contain the answer, reply ONLY with: 'I'm sorry, I don't have that information. Would you like to connect with our team?'\n"
        )


        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder", "{history}"),
            ("human", "CONTEXT:\n{context}\n\nQUESTION:\n{question}")
        ])

        # The chain definition remains the same
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def generate_response(self, question: str, context: str, history: list) -> str:
        """Generates a response from the LLM."""
        print(f"Generating response from OpenRouter using model: {settings.LLM_MODEL_NAME}...")
        
        try:
            response = self.chain.invoke({
                "question": question,
                "context": context,
                "history": history
            })
            return response
        except Exception as e:
            print(f"Error communicating with OpenRouter API: {e}")
            # Updated error message for clarity
            return "I'm sorry, but I'm having trouble connecting to the OpenRouter API. Please check your API key and configuration."

# Singleton instance
llm_service = LLMService()