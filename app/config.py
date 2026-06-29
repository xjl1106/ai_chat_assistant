# 导入所需模块
import os
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()

# 从环境变量获取 DeepSeek API 密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DeepSeek API 基础 URL，带有默认值
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL","https://api.deepseek.com")
# 模型名称，带有默认值
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-v4-flash")