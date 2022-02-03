from fastapi import Depends, FastAPI, Header, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn
from verfy import verfy_token
from git_tool import pull_repo
from config import REPO_LOCATION
app = FastAPI()

app.mount("/static", StaticFiles(directory=REPO_LOCATION, html=True), name="static")


@app.post("/push_event", dependencies=[Depends(verfy_token)])
async def push_event(X_Github_Event: str = Header(None), request: Request = None):
    if X_Github_Event == "push":
        return {"message": await pull_repo()}
    elif X_Github_Event == "ping":
        return {"message": "Pong"}
    else:
        raise HTTPException(
            status_code=403, detail="X-Github-Event not supported")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
