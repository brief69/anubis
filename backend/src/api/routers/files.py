from fastapi import APIRouter, HTTPException
from typing import List
import os
from ..models.files import FileInfo

router = APIRouter()

@router.get("/list/{path:path}", response_model=List[FileInfo])
async def list_files(path: str):
    try:
        abs_path = os.path.abspath(path)
        items = []
        for item in os.listdir(abs_path):
            item_path = os.path.join(abs_path, item)
            stat = os.stat(item_path)
            items.append(
                FileInfo(
                    name=item,
                    path=os.path.relpath(item_path),
                    is_dir=os.path.isdir(item_path),
                    size=stat.st_size if not os.path.isdir(item_path) else None,
                    modified=int(stat.st_mtime)
                )
            )
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/read/{path:path}")
async def read_file(path: str):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/write/{path:path}")
async def write_file(path: str, content: str):
    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create/directory/{path:path}")
async def create_directory(path: str):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{path:path}")
async def delete_path(path: str):
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 