import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json
from src.api.models.workspace import WorkspaceConfig

def test_get_workspace_info(client: TestClient, temp_workspace: Path):
    """ワークスペース情報取得のテスト"""
    response = client.get("/api/workspace/info")
    assert response.status_code == 200
    
    data = response.json()
    assert "path" in data
    assert "name" in data
    assert "config" in data

def test_update_workspace_config(client: TestClient, temp_workspace: Path):
    """ワークスペース設定更新のテスト"""
    config = {
        "name": "test-workspace",
        "version": "0.1.0",
        "description": "Test workspace",
        "settings": {
            "theme": "dark"
        }
    }
    
    response = client.post("/api/workspace/config", json=config)
    assert response.status_code == 200
    
    config_path = temp_workspace / ".anubis" / "config.json"
    assert config_path.exists()
    
    saved_config = json.loads(config_path.read_text())
    assert saved_config["name"] == "test-workspace"
    assert saved_config["version"] == "0.1.0"
    assert saved_config["description"] == "Test workspace"
    assert saved_config["settings"]["theme"] == "dark"

def test_initialize_workspace(client: TestClient, temp_workspace: Path):
    """ワークスペース初期化のテスト"""
    response = client.post("/api/workspace/init")
    assert response.status_code == 200
    
    # 必要なディレクトリが作成されているか確認
    assert (temp_workspace / ".anubis").exists()
    assert (temp_workspace / "src").exists()
    assert (temp_workspace / "tests").exists()
    assert (temp_workspace / "docs").exists()
    
    # 設定ファイルが作成されているか確認
    config_path = temp_workspace / ".anubis" / "config.json"
    assert config_path.exists()
    
    config = json.loads(config_path.read_text())
    assert config["name"] == temp_workspace.name
    assert config["version"] == "0.1.0" 