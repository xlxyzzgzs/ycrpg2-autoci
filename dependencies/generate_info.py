import os
import json
import os.path
import hashlib
from .utils import async_wrapper
from fastapi import HTTPException
from ..config import REPO_LOCATION


@async_wrapper
def generate_file_info_json():
    file_info = generate_info_dir("")
    with open(os.path.join(REPO_LOCATION, "file_info.json"), "w", encoding="UTF-8") as f:
        json.dump(file_info, f, ensure_ascii=False)
    return file_info["sha_512"]


def generate_info_dir(file_name):
    t_root_path = os.path.join(REPO_LOCATION, file_name)
    info = {}
    info["is_file"] = False
    info["is_dir"] = True
    info["files"] = []
    info["dirs"] = []
    info["sha_512"] = ""

    if not os.path.exists(t_root_path) or not os.path.isdir(t_root_path):
        raise HTTPException(
            status_code=404, detail=f"repo path {t_root_path} not found or not a dir")
    for name in os.listdir(t_root_path):
        t_path = os.path.join(t_root_path, name)
        if os.path.isdir(t_path):
            info["dirs"].insert(0, generate_info_dir(
                os.path.join(file_name, name)))
        else:
            info["dirs"].insert(0, generate_info_file(
                os.path.join(file_name, name)))

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
