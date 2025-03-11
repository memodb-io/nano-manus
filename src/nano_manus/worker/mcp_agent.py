import json
from .type import BaseWorker
from ..mcp_tool import TOOLS
from ..env import CONFIG, CONSOLE, llm_complete

PROMPT = """{system}
 
# Tools
{tools}
 
# Notes  
- Ensure responses are based on the latest information available from function calls.
- Always highlight the potential of available tools to assist users comprehensively.
"""


class BaseMCPAgent(BaseWorker):
    def __init__(self, use_tools: list[str]):
        self.__mcps = [TOOLS.get_mcp_client(tool) for tool in use_tools]

    def overwrite_system(self):
        return "You are a helpful assistant capable of accessing external functions."

    async def handle(self, instruction: str, global_ctx: dict = {}) -> str:
        hints = [await m.hint() for m in self.__mcps]
        tool_schemas = []
        for m in self.__mcps:
            tool_schemas.extend(await m.tool_schemas())
        find_tools = {}
        for m in self.__mcps:
            for tool in await m.get_available_tools():
                find_tools[tool.name] = m.call_tool(tool.name)

        system_prompt = PROMPT.format(
            system=self.overwrite_system(), tools="\n".join(hints)
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
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

                    actual_tool = find_tools[tool_name]
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

    async def hint(self) -> str:
        raise NotImplementedError("hint method should be implemented")
