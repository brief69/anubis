from fastapi import APIRouter, HTTPException
from typing import List
from pathlib import Path
from ..models.workspace import WorkspaceInfo, WorkspaceConfig
import json
import os

router = APIRouter()

@router.get("/info", response_model=WorkspaceInfo)
async def get_workspace_info():
    """ワークスペース情報の取得"""
    try:
        workspace_path = Path.cwd()
        config_path = workspace_path / ".anubis" / "config.json"
        
        config = {}
        if config_path.exists():
            with config_path.open() as f:
                config = json.load(f)
        
        return WorkspaceInfo(
            path=str(workspace_path),
            name=workspace_path.name,
            config=config
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config")
async def update_workspace_config(config: WorkspaceConfig):
    """ワークスペース設定の更新"""
    try:
        config_dir = Path.cwd() / ".anubis"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = config_dir / "config.json"
        with config_path.open("w") as f:
            json.dump(config.dict(), f, indent=2)
        
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/init")
async def initialize_workspace():
    """新しいワークスペースの初期化"""
    try:
        # 必要なディレクトリの作成
        dirs = [
            ".anubis",
            "src",
            "tests",
            "docs"
        ]
        
        for dir_name in dirs:
            path = Path.cwd() / dir_name
            path.mkdir(parents=True, exist_ok=True)
        
        # 基本設定の作成
        config = WorkspaceConfig(
            name=Path.cwd().name,
            version="0.1.0",
            description="",
            settings={}
        )
        
        config_path = Path.cwd() / ".anubis" / "config.json"
        with config_path.open("w") as f:
            json.dump(config.dict(), f, indent=2)
        
        return {"message": "Workspace initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 