import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json

def test_list_files(client: TestClient, temp_workspace: Path, test_file: Path, test_directory: Path):
    """ファイル一覧取得のテスト"""
    response = client.get(f"/api/files/list/{temp_workspace}")
    assert response.status_code == 200
    
    files = response.json()
    assert len(files) == 2
    
    file_names = [f["name"] for f in files]
    assert "test.txt" in file_names
    assert "test_dir" in file_names

def test_read_file(client: TestClient, test_file: Path):
    """ファイル読み取りのテスト"""
    response = client.get(f"/api/files/read/{test_file}")
    assert response.status_code == 200
    assert response.content.decode() == "Test content"

def test_write_file(client: TestClient, temp_workspace: Path):
    """ファイル書き込みのテスト"""
    test_content = "New test content"
    new_file = temp_workspace / "new_file.txt"
    
    response = client.post(
        f"/api/files/write/{new_file}",
        files={"file": ("new_file.txt", test_content)}
    )
    assert response.status_code == 200
    assert new_file.read_text() == test_content

def test_create_directory(client: TestClient, temp_workspace: Path):
    """ディレクトリ作成のテスト"""
    new_dir = temp_workspace / "new_dir"
    response = client.post(f"/api/files/create/directory/{new_dir}")
    assert response.status_code == 200
    assert new_dir.exists()
    assert new_dir.is_dir()

def test_delete_file(client: TestClient, test_file: Path):
    """ファイル削除のテスト"""
    assert test_file.exists()
    response = client.delete(f"/api/files/delete/{test_file}")
    assert response.status_code == 200
    assert not test_file.exists()

def test_delete_directory(client: TestClient, test_directory: Path):
    """ディレクトリ削除のテスト"""
    assert test_directory.exists()
    response = client.delete(f"/api/files/delete/{test_directory}")
    assert response.status_code == 200
    assert not test_directory.exists()

def test_file_not_found(client: TestClient, temp_workspace: Path):
    """存在しないファイルへのアクセスのテスト"""
    non_existent = temp_workspace / "non_existent.txt"
    response = client.get(f"/api/files/read/{non_existent}")
    assert response.status_code == 404 