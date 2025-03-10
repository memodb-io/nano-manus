import os
import asyncio
from nano_manus.env import CONSOLE
from nano_manus.prebuilt.mcp import MCPAgent
from nano_manus.prebuilt.planner import Planner

local_dir = os.path.dirname(os.path.abspath(__file__))
dir_name = os.path.basename(local_dir)

CONSOLE.print(f"Local dir: {local_dir}, Dir name: {dir_name}")

file_agent = MCPAgent.from_docker(
    "mcp/filesystem",
    volume_mounts=["--mount", f"type=bind,src={local_dir},dst=/projects/{dir_name}"],
    docker_args=["/projects"],
)


async def ready():
    await file_agent.connect()


async def cleanup():
    await file_agent.disconnect()


async def main():
    try:
        await ready()
        print(
            await file_agent.handle(
                "Go to /projects/examples, and write a hello_world.txt with content: 'nano_manus is here!'"
            )
        )
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
