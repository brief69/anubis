from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FileInfo(BaseModel):
    """ファイル情報モデル"""
    name: str
    path: str
    is_dir: bool
    size: Optional[int] = None
    modified: int

    class Config:
        from_attributes = True

class DirectoryInfo(BaseModel):
    """ディレクトリ情報モデル"""
    path: str
    files: List[FileInfo]
    
    class Config:
        from_attributes = True 