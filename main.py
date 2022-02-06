from fastapi import FastAPI
from .routers.repo_event import repo_api
app = FastAPI()

app.include_router(repo_api)
