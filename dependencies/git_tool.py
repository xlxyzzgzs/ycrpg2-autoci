from unittest import result
from fastapi import HTTPException
import subprocess
from ..config import REPO_LOCATION
from concurrent.futures import ProcessPoolExecutor
import asyncio
from .utils import async_wrapper


@async_wrapper
def pull_repo_async(location: str = REPO_LOCATION):
    return subprocess.run(["git", "pull"], cwd=location, capture_output=True)


async def pull_repo(location: str = REPO_LOCATION):
    result = await pull_repo_async(location)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr.decode())
    return result.stdout.decode()
