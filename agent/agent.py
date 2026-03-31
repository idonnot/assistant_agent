from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from config.settings import (
    LLM_MODEL, LLM_API_KEY, LLM_BASE_URL,
    OLLAMA_MODEL, OLLAMA_BASE_URL
)

from .utils.tool_register import get_all_tools
from agent.prompts.prompt_loader import load_system_prompt


class MyAgent:

    def __init__(self, llm, graph):
        self.llm = llm
        self.graph = graph

    @classmethod
    async def create(cls):
        llm = ChatOpenAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            temperature=0.2,
        )

        # use Ollama：
        # llm = ChatOllama(
        #     model=OLLAMA_MODEL,
        #     base_url=OLLAMA_BASE_URL,
        #     temperature=0.2,
        #     num_ctx=4096,
        # )

        tools = await get_all_tools() 

        graph = create_agent(
            model=llm,
            tools=tools,
            system_prompt=load_system_prompt(),
            checkpointer=InMemorySaver(),
        )

        return cls(llm, graph)

    def run(self, messages, thread_id="default_user"):
        config = {"configurable": {"thread_id": thread_id}}

        response_stream = self.graph.invoke(
            {"messages": messages},
            config,
        )

        final_answer = None

        for update in response_stream:
            if "messages" in update:
                for msg in update["messages"]:
                    if getattr(msg, "content", None):
                        final_answer = msg.content

        return final_answer

    async def arun(self, messages, thread_id="default_user"):
        config = {"configurable": {"thread_id": thread_id}}

        response_stream = await self.graph.ainvoke(
            {"messages": messages},
            config,
        )

        final_answer = None

        for msg in response_stream.get("messages", []):
            if getattr(msg, "content", None):
                final_answer = msg.content

        return final_answer