import json
from ..types import BaseAsyncAgent
from ..env import CONSOLE, llm_complete, CONFIG
from ..mcp_client.local_session import MCPClient

PROMPT = """You are a helpful assistant capable of accessing external functions. 
 
# Tools
{tools}
 
# Notes  
- Ensure responses are based on the latest information available from function calls.
- Always highlight the potential of available tools to assist users comprehensively.
"""


class MCPAgent(BaseAsyncAgent):
    @classmethod
    def from_docker(
        cls,
        image_name,
        volume_mounts: list[str] = [],
        docker_args: list[str] = [],
        docker_env: dict[str, str] = None,
    ):
        mcp_client = MCPClient.from_official(
            image_name, volume_mounts, docker_args, docker_env
        )
        return cls(image_name, mcp_client)

    def __init__(self, name, mcp_client: MCPClient):
        self._name = name
        self._mcp_client = mcp_client
        self._connected = False

    @property
    def name(self):
        return self._name

    async def connect(self):
        await self._mcp_client.connect()
        self._connected = True

    async def disconnect(self):
        await self._mcp_client.disconnect()
        self._connected = False

    async def async_description(self) -> str:
        assert self._connected, "MCP client is not connected"
        tools = await self._mcp_client.get_available_tools()
        return "I have below tools:\n- " + "\n- ".join(
            [f"{tool.name}: {tool.description}" for tool in tools]
        )

    async def handle(self, instruction: str, global_ctx: dict = None) -> str:
        assert self._connected, "MCP client is not connected"
        tools = await self._mcp_client.openai_tools()
        tool_schemas = [t["schema"] for t in tools]

        messages = [
            {
                "role": "system",
                "content": PROMPT.format(tools=await self.async_description()),
            },
            {"role": "user", "content": instruction},
        ]
        while True:
            response = await llm_complete(
                model=CONFIG.prebuilt_general_model,
                messages=messages,
                tools=tool_schemas,
                temperature=0.1,
            )
            messages.append(response.choices[0].message)
            if response.choices[0].message.tool_calls is not None:
                tool_results = []
                for tool_call in response.choices[0].message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = tool_call.function.arguments
                    if isinstance(tool_args, str):
                        tool_args = json.loads(tool_args)
                    CONSOLE.log(f"Tool call: {tool_name} with args: {tool_args}")

                    actual_tool = self._mcp_client.call_tool(tool_name)
                    tool_result = await actual_tool(**tool_args)
                    CONSOLE.log(f"Tool result: {tool_result}")
                    tool_results.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": json.dumps(tool_result),
                        }
                    )
                messages.extend(tool_results)
                continue
            else:
                return response.choices[0].message.content


if __name__ == "__main__":
    import asyncio

    agent = MCPAgent.from_docker("mcp/sqlite")

    async def test():
        try:
            await agent.connect()
            print(
                await agent.handle(
                    "Create a new demo DB table and write some mock data in it."
                )
            )
        finally:
            await agent.disconnect()

    asyncio.run(test())
