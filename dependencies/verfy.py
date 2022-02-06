from fastapi import Header, Request, HTTPException
import hashlib
import hmac
from ..config import SECRET_KEY


async def verfy_token(X_Hub_Signature_256: str = Header(None), request: Request = None):
    body = await request.body()
    if X_Hub_Signature_256 is None:
        raise HTTPException(
            status_code=403, detail="X-Hub-Signature-256 not found")
    if X_Hub_Signature_256.startswith('sha256='):
        X_Hub_Signature_256 = X_Hub_Signature_256[7:]

    result = False
    try:
        result = hmac.compare_digest(X_Hub_Signature_256, hmac.new(
            SECRET_KEY.encode(), body, hashlib.sha256).hexdigest())
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

    if not result:
        raise HTTPException(
            status_code=403, detail="X-Hub-Signature is not valid")
    return True
