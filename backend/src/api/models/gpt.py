from pydantic import BaseModel
from typing import Optional, Dict, Any

class CodeGenerationRequest(BaseModel):
    """コード生成リクエストモデル"""
    prompt: str
    workspace_path: str
    options: Optional[Dict[str, Any]] = None

class CodeGenerationResponse(BaseModel):
    """コード生成レスポンスモデル"""
    task_id: str
    status: str  # "processing", "completed", "failed"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class GenerationStatus(BaseModel):
    """生成タスクのステータスモデル"""
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None 