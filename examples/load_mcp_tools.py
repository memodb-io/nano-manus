import os
from rich import print
import asyncio
import dotenv

dotenv.load_dotenv()
from nano_manus.mcp_tool import MCPOfficial, MCPPool


terminal_mcp = MCPOfficial.from_smithery(
    "@wonderwhy-er/desktop-commander",
    suffix_args=[
        "--config",
        "{}",
    ],
)

search_mcp = MCPOfficial.from_docker(
    "mcp/brave-search",
    volume_mounts=[
        "-e",
        f"BRAVE_API_KEY={os.getenv('BRAVE_API_KEY')}",
    ],
)


thinking_mcp = MCPOfficial.from_npx(
    "@modelcontextprotocol/server-sequential-thinking", prefix_args=["-y"]
)

pool = MCPPool()
pool.add_mcp_client("terminal", terminal_mcp)
pool.add_mcp_client("search", search_mcp)
pool.add_mcp_client("thinking", thinking_mcp)


async def main():
    await pool.start()
    print(await pool.get_mcp_client("terminal").get_available_tools())
    print(await pool.get_mcp_client("search").get_available_tools())
    print(await pool.get_mcp_client("thinking").get_available_tools())

    await pool.stop()


if __name__ == "__main__":
    asyncio.run(main())
