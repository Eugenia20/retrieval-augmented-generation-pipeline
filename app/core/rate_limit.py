import time
from fastapi import HTTPException, Request
from functools import wraps
import inspect

requests_log = {}

def rate_limiter(limit: int, window: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("http_request") or kwargs.get("request")

            if request and request.client:
                ip = request.client.host
            else:
                ip = "global"

            now = time.time()

            if ip not in requests_log:
                requests_log[ip] = []

            # clean old requests
            requests_log[ip] = [
                t for t in requests_log[ip]
                if now - t < window
            ]

            if len(requests_log[ip]) >= limit:
                raise HTTPException(status_code=429, detail="Too many requests")

            requests_log[ip].append(now)

            # 🔥 FIX HERE
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper
    return decorator