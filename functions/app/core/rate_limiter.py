import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
        self.clients = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        timestamps = self.clients[client_id]

        # Remove expired entries
        self.clients[client_id] = [
            ts for ts in timestamps if now - ts < self.window
        ]

        if len(self.clients[client_id]) >= self.max_requests:
            return False

        self.clients[client_id].append(now)
        return True
