from app.logger import logger

from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError
from app.config import DEEPSEEK_API_KEY,DEEPSEEK_BASE_URL,MODEL_NAME




def call_llm(messages: list) -> str:
    """
    调用DeepSeek V4 API模型生成回复
    :param user_input: 用户输入的文本
    :return: LLM模型生成的回复文本
    """
    
    if not DEEPSEEK_API_KEY:
        return "API Key未配置，请在.env文件中设置DEEPSEEK_API_KEY。"
    

    # 初始化 OpenAI 客户端
    # - DEEPSEEK_API_KEY: 用于认证的 API Key
    # - DEEPSEEK_BASE_URL: 自定义或代理的基础 URL，用于替换默认的 OpenAI API 地址
    # - MODEL_NAME: 配置中可能指定的模型名（当前在此文件未直接使用，但保留以便未来扩展）
    client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    # 注意：OpenAI Python 客户端的构造函数可能不直接接受 model 参数。
    # 模型通常在调用接口（如 client.chat.completions.create(...)）时指定。
    )
    
    # 构建 chat completion 请求
    # - model: 指定使用的模型名称（从配置中读取）
    # - messages: 按顺序传入 system/user/assistant 角色的消息以构成对话上下文
    # - stream: False 表示一次性返回完整响应；若为 True 则为流式响应
    try:
        logger.info("开始调用大模型API")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=False
        )

        logger.info("大模型API调用成功")

        return response.choices[0].message.content  # 返回第一个候选响应的消息内容（通常只有一个候选）
    
    except RateLimitError as e:
        logger.error(f"请求频率限制或额度问题：{e}")
        return "请求过于频繁，或者当前请稍后再试。"
    
    except APIConnectionError as e:
        logger.error(f"网络连接失败：{e}")
        return "网络连接失败，请检查网络或 DeepSeek 服务是否可用。"

    except APIStatusError as e:
        logger.error(f"API 状态错误：状态码 {e.status_code}，错误信息：{e}")
        return f"API 请求失败，状态码：{e.status_code}，请检查模型名、API Key 或账户余额。"

    except Exception as e:
        logger.exception(f"未知错误：{e}")
        return "程序出现未知错误，请查看日志文件。"
    

def Stream_llm(messages: list):
    """
    调用DeepSeek V4 API模型生成回复（流式返回）
    :param user_input: 用户输入的文本
    :return: LLM模型生成的回复文本
    """
    
    if not DEEPSEEK_API_KEY:
        logger.error("API Key未配置，请在.env文件中设置DEEPSEEK_API_KEY。")
        yield "API Key未配置，请在.env文件中设置DEEPSEEK_API_KEY。"
        return
    
    # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
    )

    try:
        logger.info("开始调用大模型API（流式）")

        # 使用流式响应模式
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            # 每个 chunk 代表一个流式返回的片段
            if not chunk.choices:
                continue

            # 取出当前片段中的增量内容
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)

            # 只有当片段中包含文本增量时，才返回给调用方
            if content:
                yield content  # 实时返回生成的内容
                
        logger.info("大模型API流式调用完成")

    except RateLimitError as e:
        logger.error(f"请求频率限制或额度问题：{e}")
        return "请求过于频繁，或者当前请稍后再试。"
    
    except APIConnectionError as e:
        logger.error(f"网络连接失败：{e}")
        return "网络连接失败，请检查网络或 DeepSeek 服务是否可用。"

    except APIStatusError as e:
        logger.error(f"API 状态错误：状态码 {e.status_code}，错误信息：{e}")
        return f"API 请求失败，状态码：{e.status_code}，请检查模型名、API Key 或账户余额。"

    except Exception as e:
        logger.exception(f"未知错误：{e}")
        return "程序出现未知错误，请查看日志文件。"
    


    

