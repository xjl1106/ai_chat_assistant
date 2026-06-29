import json
import re
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("data/chat_history.json")

HISTORY_FILE = Path("data/chat_history.json")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_DIR = BASE_DIR / "data" / "sessions"


def safe_session_id(session_id: str) -> str:
    if not session_id:
        return "default"

    if not re.match(r"^[a-zA-Z0-9_-]+$", session_id):
        return "default"

    return session_id

def get_history_file(session_id: str) -> Path:
    """
    根据 session_id 获取对应的聊天历史文件路径。
    :param session_id: 会话ID
    :return: 聊天历史文件路径
    """
    SESSION_DIR.mkdir(parents=True, exist_ok=True)  # 确保目录存在

    session_id = safe_session_id(session_id)

    return SESSION_DIR / f"{session_id}.json"

def load_chat_history(session_id: str = "default") -> list:
    history_file = get_history_file(session_id)

    if not history_file.exists():
        return []

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    


def save_chat_history(user_input: str, ai_reply: str, session_id: str = "default"):
    """
    保存某个会话的一轮聊天记录
    """

    history_file = get_history_file(session_id)

    history = load_chat_history(session_id)  # 加载现有的聊天历史记录

    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_input,
        "ai": ai_reply
    })

    # 将聊天历史写回到 JSON 文件（覆盖写入）。
    # ensure_ascii=False 保持中文可读，indent=2 便于人工查看。
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)



def clear_chat_history(session_id: str = "default") -> bool:
    """
    清空某个会话的聊天历史。
    如果文件存在，就删除文件。
    如果文件不存在，也认为清空成功。
    """
    history_file = get_history_file(session_id)

    if history_file.exists():
        history_file.unlink()

    return True

