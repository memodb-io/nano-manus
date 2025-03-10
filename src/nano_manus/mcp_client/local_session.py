from functools import wraps
from mcp import ClientSession, StdioServerParameters, Tool
from typing import List, Dict, Callable, Awaitable
from mcp.client.stdio import stdio_client
from datetime import datetime
from ..env import CONSOLE


class MCPClient:
    """
    A client class for interacting with the MCP (Model Control Protocol) server.
    This class manages the connection and communication with the SQLite database through MCP.
    """

    @classmethod
    def from_official(
        cls,
        image_name: str,
        volume_mounts: List[str] = [],
        docker_args: List[str] = [],
        docker_env: Dict[str, str] = None,
    ):
        server_params = StdioServerParameters(
            command="docker",
            args=[
                "run",
                "--rm",  # Remove container after exit
                "-i",  # Interactive mode
                *volume_mounts,
                image_name,  # Use SQLite MCP image
                *docker_args,
            ],
            env=docker_env,
        )
        CONSOLE.log(f"Init MCP: {image_name} with above params:", server_params)
        return cls(server_params)

    def __init__(self, server_params: StdioServerParameters):
        """Initialize the MCP client with server parameters"""
        self.server_params = server_params
        self.session = None
        self._client = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def connect(self):
        """Establishes connection to MCP server"""
        self._client = stdio_client(self.server_params)
        self.read, self.write = await self._client.__aenter__()
        session = ClientSession(self.read, self.write)
        self.session = await session.__aenter__()

        await self.session.initialize()

    async def disconnect(self):
        """Disconnects from MCP server"""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self._client:
            await self._client.__aexit__(None, None, None)

    async def get_available_tools(self) -> List[Tool]:
        """
        Retrieve a list of available tools from the MCP server.
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        tools = await self.session.list_tools()
        return tools.tools

    def call_tool(self, tool_name: str) -> Callable[..., Awaitable[str]]:
        """
        Create a callable function for a specific tool.
        This allows us to execute database operations through the MCP server.

        Args:
            tool_name: The name of the tool to create a callable for

        Returns:
            A callable async function that executes the specified tool
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        async def callable(*args, **kwargs):
            response = await self.session.call_tool(tool_name, arguments=kwargs)
            return response.content[0].text

        return callable

    async def openai_tools(self) -> list[dict]:
        openai_tools = []
        tools = await self.get_available_tools()
        for tool in tools:
            openai_tools.append(
                {
                    "name": tool.name,
                    "schema": {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema,
                        },
                    },
                }
            )
        return openai_tools


if __name__ == "__main__":
    import asyncio

    async def test():
        mcp_client = MCPClient.from_official(
            "mcp/sqlite", ["--db-path", "/mcp/test.db"]
        )
        async with mcp_client:
            CONSOLE.print(await mcp_client.openai_tools())

    asyncio.run(test())
