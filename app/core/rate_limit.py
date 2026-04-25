import time
from fastapi import Request, HTTPException

# simple in-memory store (upgrade to Redis later)
requests_log = {}

RATE_LIMIT = 10       # requests
WINDOW = 60          # seconds


def rate_limiter(request: Request):
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in requests_log:
        requests_log[client_ip] = []

    # remove old requests
    requests_log[client_ip] = [
        t for t in requests_log[client_ip]
        if current_time - t < WINDOW
    ]

    if len(requests_log[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    requests_log[client_ip].append(current_time)