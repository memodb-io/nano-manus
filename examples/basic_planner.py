import os
import dotenv

dotenv.load_dotenv()
import argparse
from nano_manus.env import CONFIG, CONSOLE
from nano_manus.planner import Planner
from nano_manus.mcp_tool import TOOLS
from nano_manus.worker import SearchAgent, TerminalAgent
from nano_manus.worker.code_agent import CodeAgent

search_agent = SearchAgent()
terminal_agent = TerminalAgent()
code_agent = CodeAgent()

planner = Planner(workers=[search_agent, terminal_agent, code_agent])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="./tmp/agent_run")
    return parser.parse_args()


async def main():
    args = parse_args()
    CONFIG.allowed_local_dir = os.path.abspath(args.path)
    await TOOLS.start()
    # result = await planner.handle("Give me the latest weather in Tokyo today")
    await planner.outer_loop()
    await TOOLS.stop()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
