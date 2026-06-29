from app.llm import call_llm, Stream_llm
from app.utils import load_chat_history, save_chat_history


SYSTEM_PROMPT = """
你是一个耐心、清晰的 AI 学习助手。
你的任务是帮助用户学习 Python、AI 应用开发和真实项目开发。
回答时尽量循序渐进，避免一次性给太多复杂内容。
"""

def build_messages(user_input:str, session_id = "default",max_rounds:int=5)->list:
    """
    构建聊天消息列表，包含系统提示和用户输入。
    :param user_input: 用户输入的文本
    :param session_id: 会话ID
    :param max_rounds: 最大对话轮数，默认5轮
    :return: 消息列表
    """
    messages = [
        {
            "role": "system",
            "content": "SYSEM_PROMPT"  # 系统提示，设定助手行为
        }
    ]

    history = load_chat_history(session_id)

    recent_history = history[-max_rounds:]  # 获取最近的 max_rounds 条聊天记录

    for record in recent_history:
        messages.append({
            "role": "user",
            "content": record["user"]
        })
        messages.append({
            "role": "assistant",
            "content": record["ai"]
        })

    messages.append({
        "role": "user",
        "content": user_input  # 用户输入作为对话的一部分
    })   


    return messages


def chat_with_ai(user_input: str, session_id: str = "default") -> str:

    messages = build_messages(user_input, session_id)

    reply = call_llm(messages)

    save_chat_history(user_input, reply, session_id)  # 保存聊天记录

    return reply


def stream_chat_with_ai(user_input: str, session_id: str = "default"):
    """
    流式处理一次用户对话。
    一边把模型回复 yield 给前端，一边收集完整回复，最后保存历史记录。
    """

    messages = build_messages(user_input, session_id=session_id)

    reply_parts = []

    for chunk in Stream_llm(messages):
        reply_parts.append(chunk)
        yield chunk

    full_reply = "".join(reply_parts)

    save_chat_history(user_input, full_reply, session_id=session_id)

