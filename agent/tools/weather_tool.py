from langchain.tools import tool
import requests
from config.settings import WEATHER_API_KEY, WEATHER_API_URL
from typing import Dict
from es_loader.searcher import get_searcher

def get_adcode_by_location(location:str) -> Dict[str, str]:
    '''
    Return the adcode for the specified location.
    Args:location: 
        location name (can be a province, city, district individually or in combination, e.g., "Hangzhou", "Xihu District",
                "Xihu District, Hangzhou, Zhejiang")
    Returns:
        AReturns a structured dict with 'status', 'adcode', and optional 'error' or 'candidates'.
    '''
    searcher = get_searcher()
    result = searcher.get_adcode(location)
    return result
    


def get_live_weather(location:str) -> dict:
    '''
    Return the live weather for the specified city via the Amap Weather API.
    Args:
        location: Location name in Chinese (e.g., ""Hangzhou"";complex province-city-district combinations such as "Xihu District, Hangzhou" are not supported) or city adcode (e.g., "330100" → Hangzhou).
    Returns:
        Formatted weather information dictionary on success; user-friendly error message on failure.
    '''
    api_key = WEATHER_API_KEY
    if not api_key:
        print(f"Cannot find AMAP_API_KEY") 

    base_url = WEATHER_API_URL

    params: Dict[str, str] = {
        "key": api_key,          # API Key
        "city": location,            # adcode
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
            return f"Error: 未查询到{location}的天气信息"
        
        live = weather_data[0]
        city_live = live.get("city", "Unknow")
        weather = live.get("weather", "Unknow")
        temperature = live.get("temperature", "Unknow")
        wind_dir = live.get("winddirection", "Unknow")
        wind_power = live.get("windpower", "Unknow")
        report_time = live.get("reporttime","Unknow")
        
        return {
            "city": city_live,
            "weather": weather,
            "temperature": int(temperature),
            "wind_direction": wind_dir,
            "wind_power": wind_power,
            "report_time": report_time
        }
    
    except requests.exceptions.Timeout:
        return f"Error: 调用高德API超时({location})"
    except requests.exceptions.RequestException as e:
        return f"Error: 调用高德API失败 - {str(e)}"
    except Exception as e:
        return f"Error: 解析天气数据失败 - {str(e)}"
    
    