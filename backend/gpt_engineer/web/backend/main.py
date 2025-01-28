from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gpt_engineer.core.default.steps import setup_sys_prompt, setup_file_list
from gpt_engineer.core.default.steps import generate_code

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectRequest(BaseModel):
    prompt: str
    project_path: str
    openai_api_key: Optional[str] = None

@app.post("/api/generate")
async def generate_project(request: ProjectRequest):
    try:
        if request.openai_api_key:
            os.environ["OPENAI_API_KEY"] = request.openai_api_key
        
        # プロジェクトディレクトリの作成
        os.makedirs(request.project_path, exist_ok=True)
        
        # プロンプトファイルの作成
        with open(os.path.join(request.project_path, "prompt"), "w") as f:
            f.write(request.prompt)
        
        # コード生成の実行
        sys_prompt = setup_sys_prompt()
        files = setup_file_list(request.project_path)
        generated_code = generate_code(request.prompt, sys_prompt, files)
        
        return {"status": "success", "message": "Code generated successfully", "code": generated_code}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)