from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
from ..models.gpt import CodeGenerationRequest, CodeGenerationResponse
from ..services.gpt_service import GPTService

router = APIRouter()
gpt_service = GPTService()

@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest, background_tasks: BackgroundTasks):
    """コード生成リクエストの処理"""
    try:
        task_id = gpt_service.start_generation(request.prompt, request.workspace_path)
        background_tasks.add_task(gpt_service.process_generation, task_id)
        return CodeGenerationResponse(task_id=task_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}", response_model=CodeGenerationResponse)
async def get_generation_status(task_id: str):
    """生成タスクのステータス確認"""
    try:
        status = gpt_service.get_status(task_id)
        return CodeGenerationResponse(
            task_id=task_id,
            status=status.status,
            result=status.result,
            error=status.error
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop/{task_id}")
async def stop_generation(task_id: str):
    """生成タスクの停止"""
    try:
        gpt_service.stop_generation(task_id)
        return {"message": "Generation stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 