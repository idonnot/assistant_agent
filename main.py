from agent.agent import WeatherAgent

def main():
    agent = WeatherAgent()

    print("🌤 Weather Agent 已启动，输入 q 退出")

    while True:
        user_input = input(">>> ")

        if user_input.lower() == "q":
            break

        result = agent.run(user_input)
        print(result)


if __name__ == "__main__":
    main()