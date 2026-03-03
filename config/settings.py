import dotenv, os 
dotenv.load_dotenv()

# Dashscope Configuration
LLM_MODEL = "qwen3.5-plus"
LLM_API_KEY = os.getenv("DASHSCOPE_API_KEY")
LLM_BASE_URL = os.getenv("DASHSCOPE_BASE_URL")

# ES Configuration
ES_HOST = "localhost"
ES_PORT = 9202
ES_SCHEME = "http"
ES_INDEX = "city_adcode"

# Folder Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ADCODE_EXCEL_PATH = os.path.join(DATA_DIR, "AMap_adcode_citycode.xlsx")

# GMAP API Configuration
WEATHER_API_KEY = os.getenv("AMAP_API_KEY") 
WEATHER_API_URL = os.getenv("AMAP_WEATHER_URL")