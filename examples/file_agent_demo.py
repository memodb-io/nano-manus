import os
import asyncio
from nano_manus.env import CONSOLE
from nano_manus.worker.file_agent import FileAgent
from nano_manus.mcp_tool import TOOLS

file_agent = FileAgent()


async def ready():
    await TOOLS.start()


async def cleanup():
    await TOOLS.stop()


async def main():
    try:
        await ready()
        print(
            await file_agent.handle(
                "Write a hello_world.txt with content: 'nano_manus is here!'"
            )
        )
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
