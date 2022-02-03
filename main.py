from fastapi import Depends, FastAPI, Header, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn
from verfy import verfy_token

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.post("/push_event", dependencies=[Depends(verfy_token)])
async def push_event(X_Github_Event: str = Header(None), request: Request = None):
    if X_Github_Event == "push":
        return {"message": "Push event received"}
    elif X_Github_Event == "ping":
        return {"message": "Ping event received"}
    else:
        raise HTTPException(
            status_code=403, detail="X-Github-Event not supported")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
