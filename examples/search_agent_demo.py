from rich import print
import asyncio
import dotenv

dotenv.load_dotenv()

from nano_manus.worker.search_agent import SearchAgent
from nano_manus.mcp_tool import TOOLS


# search_agent = SearchAgent()


# async def ready():
#     await TOOLS.start()


# async def cleanup():
#     await TOOLS.stop()


async def main():
    # for mcp_client in TOOLS.get_all_mcp_clients():
    #     await mcp_client.connect()

    async with TOOLS.get_mcp_client("local_file") as local_file:
        print(await local_file.get_available_tools())

    # for mcp_client in TOOLS.get_all_mcp_clients():
    #     await mcp_client.disconnect()
    # await TOOLS.get_mcp_client("terminal").disconnect()
    # await TOOLS.stop()
    # await TOOLS.get_mcp_client("search_web").disconnect()
    # await TOOLS.get_mcp_client("local_file").disconnect()
    # try:
    #     await ready()
    #     print(await search_agent.handle("Tell me the last 7 days' weather in Beijing"))
    # finally:
    #     await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
