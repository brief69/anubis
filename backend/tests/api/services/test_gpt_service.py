import pytest
from src.api.services.gpt_service import GPTService
from src.api.models.gpt import GenerationStatus
import asyncio

@pytest.fixture
def gpt_service():
    return GPTService()

@pytest.mark.asyncio
async def test_start_generation(gpt_service: GPTService):
    """生成タスクの開始テスト"""
    task_id = gpt_service.start_generation("Test prompt", "/test/workspace")
    assert task_id is not None
    assert isinstance(task_id, str)
    
    status = gpt_service.get_status(task_id)
    assert status.status == "processing"
    assert status.result is None
    assert status.error is None

@pytest.mark.asyncio
async def test_process_generation(gpt_service: GPTService):
    """生成タスクの実行テスト"""
    task_id = gpt_service.start_generation("Test prompt", "/test/workspace")
    await gpt_service.process_generation(task_id)
    
    status = gpt_service.get_status(task_id)
    assert status.status == "completed"
    assert status.result is not None
    assert "files" in status.result
    assert status.error is None

@pytest.mark.asyncio
async def test_stop_generation(gpt_service: GPTService):
    """生成タスクの停止テスト"""
    task_id = gpt_service.start_generation("Test prompt", "/test/workspace")
    
    # 非同期タスクを作成
    task = asyncio.create_task(gpt_service.process_generation(task_id))
    gpt_service._running_tasks[task_id] = task
    
    # タスクを停止
    gpt_service.stop_generation(task_id)
    
    status = gpt_service.get_status(task_id)
    assert status.status == "stopped"
    assert status.error == "Task stopped by user"

def test_get_status_not_found(gpt_service: GPTService):
    """存在しないタスクのステータス取得テスト"""
    with pytest.raises(ValueError):
        gpt_service.get_status("non_existent_task") 