# AI Chat Assistant

这是一个基于 Python、FastAPI 和 DeepSeek API 实现的 Web AI 对话助手项目。项目支持网页聊天、多轮上下文、流式输出、会话隔离、聊天记录保存、清空当前会话以及日志记录。

## 项目功能

* 支持网页端 AI 对话
* 支持 DeepSeek API 调用
* 支持流式输出，AI 回复可以逐步显示
* 支持多轮对话上下文
* 支持基于 session_id 的会话隔离
* 支持每个会话单独保存聊天记录
* 支持清空当前会话历史
* 支持日志记录和异常处理
* 同时保留命令行入口和 Web API 入口

## 技术栈

* Python
* FastAPI
* Uvicorn
* OpenAI Python SDK
* DeepSeek API
* HTML
* CSS
* JavaScript
* python-dotenv

## 项目结构

```text
ai_chat_assistant/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── chat.py
│   ├── config.py
│   ├── llm.py
│   ├── logger.py
│   └── utils.py
├── static/
│   └── index.html
├── data/
│   └── sessions/
├── logs/
│   └── app.log
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

## 环境准备

建议使用虚拟环境运行项目。

```bash
python -m venv venv
```

Windows 激活虚拟环境：

```bash
venv\Scripts\activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

## 环境变量配置

在项目根目录新建 `.env` 文件，并填写以下内容：

```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-v4-flash
```

注意：`.env` 文件中包含 API Key，不要上传到 GitHub。

## 启动项目

在项目根目录运行：

```bash
uvicorn app.api:app --reload
```

启动成功后，浏览器访问：

```text
http://127.0.0.1:8000/
```

即可打开网页聊天界面。

## API 接口说明

### 首页

```http
GET /
```

返回前端聊天页面。

### 普通聊天接口

```http
POST /chat
```

请求示例：

```json
{
  "message": "你好，请介绍一下 Python",
  "session_id": "example-session-id"
}
```

响应示例：

```json
{
  "reply": "Python 是一种高级编程语言..."
}
```

### 流式聊天接口

```http
POST /chat/stream
```

请求示例：

```json
{
  "message": "请解释什么是 Python 虚拟环境",
  "session_id": "example-session-id"
}
```

该接口会以流式方式返回模型生成内容，前端可以边接收边显示。

### 清空当前会话接口

```http
POST /clear
```

请求示例：

```json
{
  "session_id": "example-session-id"
}
```

响应示例：

```json
{
  "message": "当前会话历史已清空"
}
```

## 核心实现思路

项目采用分层结构设计：

* `api.py` 负责 FastAPI 接口定义
* `chat.py` 负责对话流程、多轮上下文和流式对话处理
* `llm.py` 负责调用 DeepSeek API
* `utils.py` 负责聊天记录读取、保存和清空
* `config.py` 负责读取环境变量
* `logger.py` 负责日志记录
* `index.html` 负责前端页面展示和请求发送

用户在网页中输入问题后，前端通过 `fetch` 请求 FastAPI 接口。后端根据 `session_id` 读取当前会话的历史记录，构造 messages 后调用 DeepSeek API。模型返回结果后，后端将回复返回给前端，并把本轮对话保存到当前 session 对应的历史文件中。

## 注意事项

* 不要上传 `.env` 文件
* 不要把 API Key 写死在代码中
* 不要上传 `venv/` 或 `.venv/`
* 不要上传用户聊天记录
* 开发环境可以使用 `--reload`，正式部署时不建议使用

## 后续可扩展方向

* 接入数据库保存聊天记录
* 支持用户登录
* 支持历史会话列表
* 支持新建会话和切换会话
* 支持上传文档并进行 RAG 知识库问答
* 使用 LangChain 或 LangGraph 重构对话流程
* 部署到云服务器
