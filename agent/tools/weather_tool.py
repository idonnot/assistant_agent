from langchain.tools import tool
import requests
from config.settings import WEATHER_API_KEY, WEATHER_API_URL
from typing import Dict
from es_loader.searcher import get_searcher

def get_adcode_by_location(query:str) -> Dict[str, str]:
    '''
    Return the adcode for the specified location.
    Args:
        query: location name (包括省、市、区县的单独或组合名称，如"杭州市"、"西湖区"、"浙江省杭州市西湖区")
    Returns:
        adcode信息字典, 失败时返回友好提示
    '''
    searcher = get_searcher()
    adcode = searcher.get_adcode(query)
    if not adcode:
        return {"error": f"未找到位置 '{query}' 的adcode"}
    return {"adcode": adcode, "location": query}


def get_live_weather(city:str) -> dict:
    '''
    Return the live weather for the specified city via 高德地图天气API. 
    Args:
        city: 城市名称(e.g.杭州市,无法接收复杂的省、市、区县的组合名称，如"杭州市上城区")或城市编码adcode(e.g."330100"->"杭州市")
    Returns:
        格式化的天气信息字符串，失败时返回友好提示
    '''
    api_key = WEATHER_API_KEY
    if not api_key:
        print(f"Cannot find AMAP_API_KEY") 

    base_url = WEATHER_API_URL

    params: Dict[str, str] = {
        "key": api_key,          # API Key
        "city": city,            # adcode
        "extensions": "base",    # base=实时天气，all=预报天气
        "output": "json"         # 返回格式
    }
    try:
        response = requests.get(
            base_url,
            params=params,
            timeout=10         
        )
        response.raise_for_status() 
        
        result = response.json()
        if result.get("status") != "1":
            return f"Error: 高德API返回错误 - {result.get('info', '未知错误')}"
        
        weather_data = result.get("lives", [])
        if not weather_data:
            return f"Error: 未查询到{city}的天气信息"
        
        live = weather_data[0]
        city_live = live.get("city", "未知")
        weather = live.get("weather", "未知")
        temperature = live.get("temperature", "未知")
        wind_dir = live.get("winddirection", "未知")
        wind_power = live.get("windpower", "未知")
        report_time = live.get("reporttime","未知")
        
        return {
            "city": city_live,
            "weather": weather,
            "temperature": int(temperature),
            "wind_direction": wind_dir,
            "wind_power": wind_power,
            "report_time": report_time
        }
    
    except requests.exceptions.Timeout:
        return f"Error: 调用高德API超时({city})"
    except requests.exceptions.RequestException as e:
        return f"Error: 调用高德API失败 - {str(e)}"
    except Exception as e:
        return f"Error: 解析天气数据失败 - {str(e)}"
    
    