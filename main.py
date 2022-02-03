from fastapi import Depends, FastAPI, Header, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Optional
from verfy import verfy_token

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.post("/push_event", dependencies=[Depends(verfy_token)])
async def push_event(X_Github_Event: str = Header(None), request: Request = None):
    print(X_Github_Event)
    print(request)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
