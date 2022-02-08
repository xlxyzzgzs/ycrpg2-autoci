from fastapi import APIRouter, Depends, Header, Request, HTTPException
from ..config import REPO_LOCATION, URL_PREFIX
from ..dependencies.generate_info import generate_file_info_json
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
        event = await request.json()
        if event["head_commit"] and (message := event["head_commit"]["message"]) and message.startswith("#publish"):
            return await punlish_new_version()
        else:
            return {"message": "nothing to do"}
    elif X_Github_Event == "ping":
        return {"message": "Pong"}
    else:
        raise HTTPException(
            status_code=403, detail="X-Github-Event not supported")


async def punlish_new_version():
    pull_result = await pull_repo()
    generate_result = await generate_file_info_json()
    return {"pull_result": pull_result, "generate_result": generate_result}
