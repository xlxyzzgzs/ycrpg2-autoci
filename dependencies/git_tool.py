from fastapi import HTTPException
import subprocess
from ..config import REPO_LOCATION
from concurrent.futures import ProcessPoolExecutor
import asyncio


def pull_repo_sync(location: str = REPO_LOCATION):
    return subprocess.run(["git", "pull"], cwd=location, capture_output=True)


async def pull_repo(location: str = REPO_LOCATION):

    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=1) as executor:
        result = await loop.run_in_executor(executor, pull_repo_sync, location)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr.decode())
    return result.stdout.decode()
