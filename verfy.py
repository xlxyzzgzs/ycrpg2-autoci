from fastapi import Header, Request, HTTPException
from typing import Optional
import hashlib
import hmac
import config


async def verfy_token(X_Hub_Signature_256: str = Header(None), request: Request = None):
    body = await request.body()
    if X_Hub_Signature_256.startswith('sha256='):
        X_Hub_Signature_256 = X_Hub_Signature_256[7:]
    result = hmac.compare_digest(X_Hub_Signature_256, hmac.new(
        config.SECRET_KEY.encode(), body, hashlib.sha256).hexdigest())
    if not result:
        raise HTTPException(
            status_code=403, detail="X-Hub-Signature is not valid")
    return True
