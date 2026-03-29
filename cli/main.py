import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.agent import WeatherAgent

def main():
    agent = WeatherAgent()

    print("Assistant Agent 已启动，输入 q 退出")

    while True:
        user_input = input(">>> ")

        if user_input.lower() == "q":
            break

        result = agent.run(user_input)
        print(result)


if __name__ == "__main__":
    main()