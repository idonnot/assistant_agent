import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.prompts.prompt_loader import load_system_prompt

if __name__ == "__main__":
    system_prompt = load_system_prompt()
    print(system_prompt)