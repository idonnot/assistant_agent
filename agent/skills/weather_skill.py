
from agent.tools.weather_tool import get_adcode_by_location, get_live_weather
from langchain.tools import tool

@tool
def get_weather_by_location(location: str) -> dict:
    '''
    查询指定位置实时天气，必须用于实时天气问题，而非天气预报。
    Args:
        location: 位置名称（如"杭州市"、"西湖区"、"浙江省杭州市西湖区"）或是adcode（如"330100"->"杭州市"）
    Returns:
        格式化的天气信息字符串，失败时返回友好提示
    '''
    adcode_result = get_adcode_by_location(location)
    if "error" in adcode_result:
        return adcode_result["error"]
    
    adcode = adcode_result["adcode"]
    weather_result = get_live_weather(adcode)
    
    return weather_result