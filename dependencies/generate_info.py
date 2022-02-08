import os
import json
import os.path
import hashlib
from .utils import async_wrapper
from fastapi import HTTPException
from ..config import REPO_LOCATION

skip_names = ["__pycache__", "__init__.py",
              "__init__.pyc", "__init__.pyo", "__init__.pyw", "__init__.pyd"]


def generate_file_info_json_sync():
    file_info = generate_info_dir("")
    if not os.path.exists(REPO_LOCATION):
        raise HTTPException(status_code=500, detail="repo not found")

    if os.path.exists(os.path.join(REPO_LOCATION, "file_info.json")):
        os.remove(os.path.join(REPO_LOCATION, "file_info.json"))

    with open(os.path.join(REPO_LOCATION, "file_info.json"), "w", encoding="UTF-8") as f:
        json.dump(file_info, f, ensure_ascii=False)
    return file_info["sha_512"]


def generate_info_dir(file_name):
    t_root_path = os.path.join(REPO_LOCATION, file_name)
    info = {}
    info["is_file"] = False
    info["is_dir"] = True
    info["files"] = {}
    info["dirs"] = {}
    info["sha_512"] = ""

    if not os.path.exists(t_root_path) or not os.path.isdir(t_root_path):
        raise HTTPException(
            status_code=404, detail=f"repo path {t_root_path} not found or not a dir")
    for name in os.listdir(t_root_path):
        if name.startswith(".") or name in skip_names:
            continue
        t_path = os.path.join(t_root_path, name)
        if os.path.isdir(t_path):
            info["dirs"][name] = generate_info_dir(
                os.path.join(file_name, name))
        else:
            info["files"][name] = generate_info_file(
                os.path.join(file_name, name))

    info["sha_512"] = hashlib.sha512(json.dumps(info).encode()).hexdigest()
    return info


def generate_info_file(file_name):
    t_file_path = os.path.join(REPO_LOCATION, file_name)
    if not os.path.exists(t_file_path) or not os.path.isfile(t_file_path):
        raise HTTPException(
            status_code=404, detail=f"repo path {t_file_path} not found or not a file")
    info = {}
    info["is_file"] = True
    info["is_dir"] = False
    with open(t_file_path, "rb") as f:
        info["sha_512"] = hashlib.sha512(f.read()).hexdigest()
    return info


async def generate_file_info_json():
    return await async_wrapper(generate_file_info_json_sync)()
