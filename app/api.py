from pathlib import Path

from fastapi import FastAPI,HTTPException

# FileResponse 用于返回文件给客户端
from fastapi.responses import FileResponse, StreamingResponse
# StaticFiles 用于挂载静态文件目录
from fastapi.staticfiles import StaticFiles

# Pydantic BaseModel 用于数据验证和模型定义
from pydantic import BaseModel

from app.chat import chat_with_ai, stream_chat_with_ai
from app.logger import logger

from app.utils import clear_chat_history
import time


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="AI助手API",
              description="基于DeepSeek V4的AI聊天助手API",
              version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    """
    请求体模型，用于验证和解析用户输入的JSON数据。
    """
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    """
    响应体模型，用于返回AI助手的回复。
    """
    reply: str

class ClearRequest(BaseModel):
    session_id: str = "default"

@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/clear")
def clear_history(request: ClearRequest):
    clear_chat_history(request.session_id)

    logger.info(f"已清空会话历史：session_id={request.session_id}")

    return {
        "message": "当前会话历史已清空"
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="message 不能为空")

    logger.info(f"收到用户请求：session_id={request.session_id}, message={user_message}")

    reply = chat_with_ai(user_message, session_id=request.session_id)

    return ChatResponse(reply=reply)

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="message 不能为空")

    logger.info(f"收到流式请求：session_id={request.session_id}, message={user_message}")

    return StreamingResponse(
        stream_chat_with_ai(user_message, session_id=request.session_id),
        media_type="text/plain; charset=utf-8"
    )



@app.get("/test/stream")
def test_stream():
    def generate():
        for i in range(1, 6):
            yield f"data: 第 {i} 段内容\n\n"
            time.sleep(1)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )