# Assistant Agent 🌤

一个基于LLM的智能个人代理，集成Elasticsearch地理位置检索和高德地图天气API，支持自然语言查询天气信息;RAG集成凡人修仙传的内容，支持查询凡人修仙传相关内容。

## 项目概述

Weather Agent是一个多模块协作系统，当用户查询天气时：
1. LLM理解用户查询意图
2. 调用城市位置检索工具获取adcode
3. 调用天气API查询实时天气信息
4. 返回格式化的天气结果

## 架构

```
┌─────────────────┐
│  main.py        │ ← 用户交互入口
└────────┬────────┘
         │
    ┌────▼────────┐
    │ MyAgent│ (LLM agent)
    └────┬────────┘
         │
    ┌────┴──────────────┬──────────────────┐
    │                   │                  │
┌───▼──────┐  ┌────────▼────────┐  ┌─────▼─────┐
│ LLM      │  │ Tool 1:         │  │ Tool 2:   │
│(Qwen)    │  │ get_adcode_by   │  │ get_live  │
│          │  │ _location       │  │ _weather  │
└──────────┘  └────────┬────────┘  └─────┬─────┘
                       │                  │
         ┌─────────────▼─────┐      ┌──────▼──────┐
         │ Elasticsearch     │      │ AMAP API    │
         │ (城市adcode查询)  │      │ (天气信息)  │
         └───────────────────┘      └─────────────┘
```

## 核心功能

### 1. **智能位置检索** (`es_loader/`)

- **位置搜索** (`searcher.py`)：
  - 支持多种查询方式（精确、模糊、前缀）
  - 优先级：adcode精确匹配 > 全名匹配 > 名称匹配 > 前缀匹配
  - 按行政级别过滤（province/city/district）
  - 可获取行政区划层级关系

- **数据加载** (`adcode_data_loader.py`)：
  - 从Excel读取中国行政区划数据
  - 自动识别三级行政区划（省/市/区）
  - 构建完整的层级关系图
  - 批量导入Elasticsearch

- **ES工具** (`es_utils.py`)：
  - Elasticsearch连接管理
  - 索引创建与删除
  - 中文分词器(IK)集成

### 2. **智能Agent系统** (`agent/`)

- **MyAgent** (`agent.py`)：
  - 基于LLM的对话代理
  - 集成两个专用工具
  - 支持对话历史记录
  - 流式响应处理

- **工具函数** (`agent/tools/weather_tool.py`)：
  - `get_adcode_by_location()`：地点→adcode转换
  - `get_live_weather()`：实时天气查询

### 3. **配置管理** (`config/`)

- Elasticsearch连接配置
- AMAP API密钥管理
- Dashscope LLM配置
- 数据文件路径管理

## 安装

### 前置要求

- Python 3.9+
- Elasticsearch 8.6+ (需要支持IK分词器)
- Docker (可选，用于快速启动Elasticsearch)

### 步骤

#### 1. 克隆项目并安装依赖

```bash
git clone <repo_url>
cd weather_agent
pip install -r requirements.txt
```

#### 2. 获取API密钥

创建`.env`文件，添加以下配置：

```bash
# Dashscope API (阿里云通义千问)
DASHSCOPE_API_KEY=your_dashscope_key
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# AMAP API (高德地图天气)
AMAP_API_KEY=your_amap_key

# 可选：Elasticsearch配置
# ES_HOST=localhost
# ES_PORT=9202
```

申请地址：
- [Dashscope Control Panel](https://dashscope.console.aliyun.com/)
- [AMAP Developer Platform](https://lbs.amap.com/)

#### 3. 启动Elasticsearch

**选项A：使用Docker**

```bash
cd docker
docker-compose up -d
```

**选项B：本地安装**

需要手动安装Elasticsearch 8.6+和IK分词器插件

#### 4. 加载地理位置数据

将城市数据文件 `data/AMap_adcode_citycode.xlsx` 放在指定位置，然后运行：

```bash
python -c "from es_loader.adcode_data_loader import load_excel_to_es; load_excel_to_es()"
```

## 使用

### 命令行交互模式

```bash
python main.py
```

示例查询：

```
>>> 杭州最近天气怎么样？
>>> 帮我查一下北京的实时温度
>>> 西湖区现在的天气如何？
>>> q (退出)
```

### 作为库使用

```python
from agent.agent import MyAgent

agent = MyAgent()

# 单次查询
message = "杭州天气"
result = agent.run(message)
print(result)

# 多轮对话（使用相同thread_id保存上下文）
result = agent.run(message, thread_id="user_123")
```

## 配置说明

### Elasticsearch配置

```python
# config/settings.py
ES_HOST = "localhost"           # ES服务器地址
ES_PORT = 9202                  # ES服务器端口
ES_SCHEME = "http"             # 连接协议
ES_INDEX = "city_adcode"       # 索引名称
```

### LLM配置

```python
# agent/agent.py
model = "qwen3.5-plus"          # 使用的LLM模型
temperature = 0.2               # 回复随机性（0-1）
```

## 项目结构

```
weather_agent/
├── main.py                          # 主程序入口
├── config/
│   ├── __init__.py
│   └── settings.py                 # 全局配置
├── agent/
│   ├── __init__.py
│   ├── agent.py                    # MyAgent主类
│   ├── simple_weather_agent.py     # 简化版本
│   └── tools/
│       ├── __init__.py
│       └── weather_tool.py         # 工具函数定义
├── es_loader/
│   ├── __init__.py
│   ├── es_utils.py                # ES连接管理
│   ├── adcode_data_loader.py      # 数据导入
│   └── searcher.py                # 位置搜索
├── data/
│   └── AMap_adcode_citycode.xlsx  # 城市adcode数据
├── docker/
│   ├── docker-compose.yml         # Docker配置
│   ├── data/                      # ES数据持久化目录
│   └── logs/                      # ES日志
├── tests/
│   ├── test_adcode.py
│   ├── test_es_client.py
│   └── test_*                      # 其他测试
├── README.md
└── requirements.txt
```

## 依赖说明

### 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| elasticsearch | 8.6.2 | Elasticsearch Python客户端 |
| langchain-openai | - | LLM集成框架 |
| langgraph | - | Agent工作流引擎 |
| langchain | - | 工具框架 |
| pandas | - | 数据处理 |
| requests | - | HTTP请求 |
| python-dotenv | - | 环境变量管理 |

## 常见问题

### Q: 如何更换LLM模型？
A: 修改 `agent/agent.py` 中的 `model` 参数，支持Qwen、GPT等主流模型

### Q: Elasticsearch无法连接？
A: 检查ES服务是否运行，默认端口9202，可在 `config/settings.py` 修改

### Q: 地理位置查询不准确？
A: 确保数据集最新，可重新运行 `load_excel_to_es()` 更新索引

### Q: 支持哪些地区的天气查询？
A: 支持中国大陆所有省市区县级行政区划

## 未来计划

- [ ] 支持多日天气预报
- [ ] 集成空气质量数据
- [ ] 支持极端天气预警
- [ ] Web界面
- [ ] 数据缓存优化

## 许可证

MIT