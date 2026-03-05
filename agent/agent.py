from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from config.settings import LLM_MODEL, LLM_API_KEY, LLM_BASE_URL, OLLAMA_MODEL, OLLAMA_BASE_URL
from agent.skills.weather_skill import get_real_time_weather
import pprint
from agent.prompts.prompt_loader import load_system_prompt


class WeatherAgent:
    def __init__(self):
        # self.llm = ChatOpenAI(
        #     model = LLM_MODEL,
        #     api_key = LLM_API_KEY,
        #     base_url = LLM_BASE_URL,
        #     temperature = 0.2,
        # )

        self.llm = ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.2,
        )

        self.graph = create_agent(
            model=self.llm,
            tools=[get_real_time_weather],
            system_prompt=load_system_prompt(),
            checkpointer=InMemorySaver(),
        )


    def run(self, messages, thread_id="default_user"):
        """
        Args:
        messages: [
            {"role": "user", "content": "..."}
        ]
        """

        config = {"configurable": {"thread_id": thread_id}}

        response_stream = self.graph.invoke(
            {"messages": messages},
            config,
            stream_mode="updates",
        )

        final_answer = None

        for update in response_stream:
            # pprint.pprint(update)

            if "model" in update and len(update["model"]["messages"]) > 0:
                msg = update["model"]["messages"][0]
                if hasattr(msg, "content") and msg.content:
                    final_answer = msg.content

        return final_answer

