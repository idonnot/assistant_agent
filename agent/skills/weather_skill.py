
from agent.services.weather_tool import get_adcode_by_location, get_live_weather
from langchain.tools import tool
from ..schemas.tool_schema import ToolResponse


@tool("real_time_weather")
def get_real_time_weather(location: str) -> str:
    '''
    Use this tool when the user asks about the real-time weather.
    '''

    try:
        # Step 1: Get adcode
        adcode_result = get_adcode_by_location(location)

        # Step 2
        status = adcode_result.get("status")

        if status == "ambiguous":
            return ToolResponse(
                status="error",
                message="Location is ambiguous, please clarify",
                data=adcode_result
            ).model_dump_json()

        elif status == "not_found":
            return ToolResponse(
                status="error",
                message="Location not found",
                data=adcode_result
            ).model_dump_json()

        elif status != "ok":
            return ToolResponse(
                status="error",
                message=f"Unexpected error: {adcode_result}",
                data=None
            ).model_dump_json()

        # Step 3
        adcode = adcode_result["adcode"]
        weather_result = get_live_weather(adcode)

        if isinstance(weather_result, str):
            return ToolResponse(
                status="error",
                message=weather_result,
                data=None
            ).model_dump_model_dump_json()

        # Step 4
        return ToolResponse(
            status="success",
            message=None,
            data=weather_result
        ).model_dump_json()

    except Exception as e:
        return ToolResponse(
            status="error",
            message=str(e),
            data=None
        ).model_dump_json()