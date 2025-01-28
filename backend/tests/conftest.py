import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import shutil
import tempfile
from typing import Generator
from src.api.main import app

@pytest.fixture
def client() -> TestClient:
    """テストクライアントを提供するフィクスチャ"""
    return TestClient(app)

@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """一時的なワークスペースディレクトリを提供するフィクスチャ"""
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace_path = Path(temp_dir)
        yield workspace_path

@pytest.fixture
def test_file(temp_workspace: Path) -> Generator[Path, None, None]:
    """テスト用のファイルを提供するフィクスチャ"""
    file_path = temp_workspace / "test.txt"
    file_path.write_text("Test content")
    yield file_path
    if file_path.exists():
        file_path.unlink()

@pytest.fixture
def test_directory(temp_workspace: Path) -> Generator[Path, None, None]:
    """テスト用のディレクトリを提供するフィクスチャ"""
    dir_path = temp_workspace / "test_dir"
    dir_path.mkdir()
    yield dir_path
    if dir_path.exists():
        shutil.rmtree(dir_path) 