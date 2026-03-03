from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import dotenv, os, requests
from typing import Dict

dotenv.load_dotenv()

@tool
def get_live_weather(city:str) -> str:
    '''
    Return the live weather(实时天气) for the specified city via 高德地图天气API.
    Args:
        city: 城市名称(如"杭州"、"嘉兴",也可以具体到区县,如"上城区")或是城市编码adcode(如"330100"对应"杭州市")
    Returns:
        格式化的天气信息字符串，失败时返回友好提示
    '''
    api_key = os.getenv("AMAP_API_KEY")
    if not api_key:
        print(f"Cannot find GMAP_API_KEY") 

    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"

    params: Dict[str, str] = {
        "key": api_key,          # API Key
        "city": city,        # 城市名称或编号
        "extensions": "base",    # base=实时天气，all=预报天气
        "output": "json"         # 返回格式
    }
    try:
        response = requests.get(
            base_url,
            params=params,
            timeout=10          # 超时时间10秒
        )
        response.raise_for_status()  # 触发HTTP错误
        
        result = response.json()
        if result.get("status") != "1":
            return f"Error: 高德API返回错误 - {result.get('info', '未知错误')}"
        
        # 提取天气数据（取第一个城市的第一条记录）
        weather_data = result.get("lives", [])
        if not weather_data:
            return f"Error: 未查询到{city}的天气信息"
        
        live = weather_data[0]
        city = live.get("city", "未知")
        weather = live.get("weather", "未知")
        temperature = live.get("temperature", "未知")
        wind_dir = live.get("winddirection", "未知")
        wind_power = live.get("windpower", "未知")
        report_time = live.get("reporttime","未知")
        
        return (
            f"{city}实时天气：\n"
            f"天气：{weather}\n"
            f"温度：{temperature}℃\n"
            f"风向：{wind_dir}\n"
            f"风力：{wind_power}级\n"
            f"report_time: {report_time}"
        )
    
    except requests.exceptions.Timeout:
        return f"Error: 调用高德API超时({city})"
    except requests.exceptions.RequestException as e:
        return f"Error: 调用高德API失败 - {str(e)}"
    except Exception as e:
        return f"Error: 解析天气数据失败 - {str(e)}"
    
    
llm = ChatOpenAI(
    model = "qwen3.5-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.2,
)

graph = create_agent(
    model=llm,
    tools=[get_live_weather],
    system_prompt='''You are an helpful assistant.''',
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "user_1"}}
inputs = {
    "messages": [
        {"role": "user", "content": "上海的天气现在怎么样？"},     
        {"role": "user", "content": "杭州上城区的天气现在怎么样？"}, 
        {"role": "user", "content": "这两个地方都下雨吗？"},                
    ]
}
resonse = graph.invoke(
    inputs,
    config,
    stream_mode="updates",
)
# print(resonse)

final_answer = None
for update in resonse:
    if 'model' in update and len(update['model']['messages']) > 0:
        msg = update['model']['messages'][0]
        if hasattr(msg, 'content') and msg.content:
            final_answer = msg.content

if final_answer:
    print("智能体最终回答：")
    print(final_answer)
else:
    print("未获取到有效回答")