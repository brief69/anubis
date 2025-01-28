from pydantic import BaseModel
from typing import Dict, Any, Optional

class WorkspaceConfig(BaseModel):
    """ワークスペース設定モデル"""
    name: str
    version: str
    description: Optional[str] = ""
    settings: Dict[str, Any] = {}

class WorkspaceInfo(BaseModel):
    """ワークスペース情報モデル"""
    path: str
    name: str
    config: Dict[str, Any] 