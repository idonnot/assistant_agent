import dotenv, os 
dotenv.load_dotenv()

# Dashscope Configuration
LLM_MODEL = "qwen3.5-plus"
LLM_API_KEY = os.getenv("DASHSCOPE_API_KEY")
LLM_BASE_URL = os.getenv("DASHSCOPE_BASE_URL")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

# ES Configuration
ES_HOST = "localhost"
ES_PORT = 9202
ES_SCHEME = "http"
ES_INDEX = "city_adcode"

# Folder Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ADCODE_EXCEL_PATH = os.path.join(DATA_DIR, "AMap_adcode_citycode.xlsx")

PROMPT_DIR = os.path.join(BASE_DIR, "agent", "prompts")

# Fanren Config
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
DOC_CHUNKS_DIR = os.path.join(DATA_DIR, "doc_chunks")
FANREN_NOVEL_DIR = os.path.join(DATA_DIR, "fanren_novel")
FANREN_DOC_CHUNKS_PATH = os.path.join(DOC_CHUNKS_DIR, "fanren_chunks.pkl")
FANREN_CHARACTER_MAP_PATH = os.path.join(DATA_DIR, "fanren_character_map.json")

# GMAP API Configuration
WEATHER_API_KEY = os.getenv("AMAP_API_KEY") 
WEATHER_API_URL = os.getenv("AMAP_WEATHER_URL")


# RAG Configuration
MODEL_DIR = os.path.join(BASE_DIR, "rag", "model")
RERANK_MODEL = os.path.join(MODEL_DIR, "bge-reranker-base")
VECTOR_DB_MODEL = os.path.join(MODEL_DIR, "bge-small-zh-v1.5")

# GitHub MCP Cinfigutation
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_MCP_ENABLED = os.getenv("GITHUB_MCP_ENABLED", "true").lower() == "true"

MCP_CONFIG_PATH = os.path.join(BASE_DIR, "config", "mcp_config.json")