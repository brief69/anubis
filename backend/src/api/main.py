from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import files, gpt, workspace

app = FastAPI(
    title="Anubis IDE API",
    description="Anubis IDEのバックエンドAPI",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドの開発サーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(gpt.router, prefix="/api/gpt", tags=["gpt"])
app.include_router(workspace.router, prefix="/api/workspace", tags=["workspace"])

@app.get("/")
async def root():
    return {"message": "Anubis IDE API"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    ) 