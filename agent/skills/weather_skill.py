
from agent.tools.weather_tool import get_adcode_by_location, get_live_weather
from langchain.tools import tool

@tool("real_time_weather")
def get_real_time_weather(location: str) -> dict:
    '''
    Retrieve real-time (current) weather data for a specified location.

    This tool MUST be used only for real-time weather queries.
    It MUST NOT be used for weather forecast or future weather inquiries.

    The tool returns structured weather data.
    When generating the final answer, you MUST:
        - Clearly describe the current weather condition
        - Include the current temperature
        - Provide appropriate clothing advice

    Args:
        location: Name of the location (e.g., "Hangzhou", "Xihu District",
                "Xihu District, Hangzhou, Zhejiang")

    Returns:
        A formatted weather information dictionary.
        If the query fails, return a clear and user-friendly error message.
    '''
    # Step 1: Get adcode for the location
    adcode_result = get_adcode_by_location(location)
    
    # Step 2: Handle different status codes
    if adcode_result['status'] == 'ambiguous':
        # Location is ambiguous, ask for clarification
        return {"error": adcode_result['error']}
    elif adcode_result['status'] == 'not_found':
        # Location not found
        return {"error": adcode_result['error']}
    elif adcode_result['status'] != 'ok':
        # Unexpected status
        return {"error": f"未知错误：{adcode_result}"}
    
    # Step 3: Get weather data using the adcode
    adcode = adcode_result['adcode']
    weather_result = get_live_weather(adcode)
    
    return weather_result