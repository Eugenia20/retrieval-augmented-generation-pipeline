import time
from fastapi import HTTPException
from functools import wraps

# simple in-memory store
requests_log = {}


def rate_limiter(limit: int, window: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # identify user by IP (basic)
            request = kwargs.get("request")

            if request:
                ip = request.client.host
            else:
                ip = "global"

            now = time.time()

            if ip not in requests_log:
                requests_log[ip] = []

            # remove old requests
            requests_log[ip] = [
                t for t in requests_log[ip]
                if now - t < window
            ]

            if len(requests_log[ip]) >= limit:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests"
                )

            requests_log[ip].append(now)

            return func(*args, **kwargs)

        return wrapper
    return decorator