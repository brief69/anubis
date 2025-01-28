from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
from ..models.files import FileInfo, DirectoryInfo
import os
import shutil

router = APIRouter()

@router.get("/list/{path:path}", response_model=List[FileInfo])
async def list_files(path: str):
    """指定されたパスのファイル一覧を取得"""
    try:
        full_path = Path(path).resolve()
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Path not found")
        
        files = []
        for item in full_path.iterdir():
            files.append(FileInfo(
                name=item.name,
                path=str(item.relative_to(Path.cwd())),
                is_dir=item.is_dir(),
                size=item.stat().st_size if item.is_file() else None,
                modified=item.stat().st_mtime
            ))
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/read/{path:path}")
async def read_file(path: str):
    """ファイルの内容を読み取り"""
    try:
        full_path = Path(path).resolve()
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        if not full_path.is_file():
            raise HTTPException(status_code=400, detail="Path is not a file")
        
        return FileResponse(full_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/write/{path:path}")
async def write_file(path: str, file: UploadFile = File(...)):
    """ファイルの書き込み"""
    try:
        full_path = Path(path).resolve()
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with full_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"message": "File written successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{path:path}")
async def delete_file(path: str):
    """ファイルまたはディレクトリの削除"""
    try:
        full_path = Path(path).resolve()
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Path not found")
        
        if full_path.is_file():
            full_path.unlink()
        else:
            shutil.rmtree(full_path)
        
        return {"message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create/directory/{path:path}")
async def create_directory(path: str):
    """ディレクトリの作成"""
    try:
        full_path = Path(path).resolve()
        full_path.mkdir(parents=True, exist_ok=True)
        return {"message": "Directory created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 