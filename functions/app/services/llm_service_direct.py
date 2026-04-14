import httpx
from app.config import settings


class DirectLLMService:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL.rstrip("/")
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.LLM_MODEL_NAME

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.YOUR_SITE_URL,
            "X-Title": settings.YOUR_APP_NAME,
        }

    async def generate_response(self, question: str, context: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Kai, the KAITOZ AI assistant. "
                        "Be clear, concise, and professional. "
                        "If you don’t know, say so."
                    ),
                },
                {
                    "role": "user",
                    "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}",
                },
            ],
            "temperature": 0.1,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
            )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]
