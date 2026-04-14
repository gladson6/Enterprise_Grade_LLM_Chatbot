from fastapi import Request, HTTPException
from app.core.rate_limiter import RateLimiter

rate_limiter = RateLimiter(max_requests=5, window_seconds=60)

async def rate_limit(request: Request):
    client_ip = request.client.host

    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait and try again."
        )
