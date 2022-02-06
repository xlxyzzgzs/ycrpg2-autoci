from fastapi import APIRouter, Depends, Header, Request, HTTPException
from ..config import REPO_LOCATION, URL_PREFIX
from ..dependencies.verfy import verfy_token
from ..dependencies.git_tool import pull_repo

repo_api = APIRouter(
    prefix=URL_PREFIX,
    dependencies=[Depends(verfy_token)],
    tags=["repo"],
    responses={404: {"description": "Not found"}},
)


@repo_api.post("/push_event")
async def push_event(X_Github_Event: str = Header(None), request: Request = None):
    if X_Github_Event == "push":
        return {"message": await pull_repo(REPO_LOCATION)}
    elif X_Github_Event == "ping":
        return {"message": "Pong"}
    else:
        raise HTTPException(
            status_code=403, detail="X-Github-Event not supported")
