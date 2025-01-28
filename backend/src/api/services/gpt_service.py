import uuid
from typing import Dict, Optional
from ..models.gpt import GenerationStatus
from gpt_engineer.core import run_gpt_engineer
import asyncio
import logging

class GPTService:
    def __init__(self):
        self._tasks: Dict[str, GenerationStatus] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self.logger = logging.getLogger(__name__)

    def start_generation(self, prompt: str, workspace_path: str) -> str:
        """コード生成タスクの開始"""
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = GenerationStatus(status="processing")
        return task_id

    async def process_generation(self, task_id: str):
        """コード生成の実行"""
        try:
            status = self._tasks[task_id]
            if status.status != "processing":
                return

            # GPT Engineerの実行
            result = await self._run_gpt_engineer(task_id)
            
            self._tasks[task_id] = GenerationStatus(
                status="completed",
                result=result
            )
        except Exception as e:
            self.logger.error(f"Error in generation task {task_id}: {str(e)}")
            self._tasks[task_id] = GenerationStatus(
                status="failed",
                error=str(e)
            )

    def get_status(self, task_id: str) -> GenerationStatus:
        """タスクのステータス取得"""
        if task_id not in self._tasks:
            raise ValueError(f"Task {task_id} not found")
        return self._tasks[task_id]

    def stop_generation(self, task_id: str):
        """タスクの停止"""
        if task_id in self._running_tasks:
            task = self._running_tasks[task_id]
            task.cancel()
            self._tasks[task_id] = GenerationStatus(
                status="stopped",
                error="Task stopped by user"
            )

    async def _run_gpt_engineer(self, task_id: str) -> Dict:
        """GPT Engineerの実行ロジック"""
        # TODO: 実際のGPT Engineer統合を実装
        return {
            "files": [
                {"path": "example.py", "content": "print('Hello, World!')"}
            ],
            "message": "Code generated successfully"
        } 