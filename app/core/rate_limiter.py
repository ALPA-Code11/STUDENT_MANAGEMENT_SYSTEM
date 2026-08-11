from fastapi import Request, HTTPException, status

from app.core.redis_client import redis_client


def rate_limit(request: Request, limit: int = 5, window: int = 60):
    # 1. Client ka IP address
    client_ip = request.client.host

    # 2. Redis mein unique key
    key = f"rate_limit:{client_ip}"

    # 3. Request counter increase karo
    request_count = redis_client.incr(key)

    # 4. First request par 60 seconds ka expiry set karo
    if request_count == 1:
        redis_client.expire(key, window)

    # 5. Limit cross hui?
    if request_count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )

    return True