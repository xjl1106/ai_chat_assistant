import logging
from pathlib import Path

# 日志目录（相对于项目根）
LOG_DIR = Path("logs")
# 如果不存在则创建目录
LOG_DIR.mkdir(exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / "app.log"

# 配置根日志，输出到文件和控制台，使用 UTF-8 编码写文件
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 模块级 logger，其他模块可 from app.logger import logger 使用
logger = logging.getLogger(__name__)