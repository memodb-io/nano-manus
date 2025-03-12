import json
from .type import BaseWorker
from ..mcp_tool import TOOLS
from ..env import CONFIG, CONSOLE, llm_complete

PROMPT = """{system}
 
# Tools
{tools}

# Additional Context
Below is the additional context you may need to understand the user's instruction.
{additional_context}

# Planning step by step 
Before you start to call functions, you should always plan step by step and explain your plan in a concise way.

# Notes  
- Always highlight the potential of available tools to assist users comprehensively.
- If you're unable to complete the task, state your reasons and encountered problems clearly.

## Recap
After callings are done and the task is completed, you should always summary why/what tools your called in a concise way after your response to the instruction.
For example:
```
// before is your response
## Recap
1. I used `search_web` to first search the latest weather in SF
2. Then I used `convert_to_csv` to convert the data into csv format
...
```
"""


class BaseMCPAgent(BaseWorker):
    def __init__(self, use_tools: list[str]):
        self.__mcps = [TOOLS.get_mcp_client(tool) for tool in use_tools]

    def overwrite_system(self):
        return "You are a helpful assistant capable of accessing external functions."

    async def handle(self, instruction: str, global_ctx: dict = {}) -> str:
        CONSOLE.print(f"🤖 {self.name} is solving:", instruction)
        additional_context = {
            r: c for r, c in global_ctx.get("results", {}).items() if r in instruction
        }
        if additional_context:
            CONSOLE.print(
                f"🤖 {self.name}: I will use previouse results", additional_context
            )
        additional_context_string = "\n".join(
            [f"- {k}: {v}" for k, v in additional_context.items()]
        )
        hints = [await m.hint() for m in self.__mcps]
        tool_schemas = []
        for m in self.__mcps:
            tool_schemas.extend(await m.tool_schemas())
        find_tools = {}
        for m in self.__mcps:
            for tool in await m.get_available_tools():
                find_tools[tool.name] = m.call_tool(tool.name)

        system_prompt = PROMPT.format(
            system=self.overwrite_system(),
            tools="\n".join(hints),
            additional_context=additional_context_string,
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
                    CONSOLE.log(f"🔧 {self.name} is using {tool_name}")

                    actual_tool = find_tools[tool_name]
                    tool_result = await actual_tool(**tool_args)
                    # CONSOLE.log(f"🔧 Tool result: {tool_result}")
                    tool_results.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": json.dumps(tool_result)[
                                : CONFIG.maximum_tool_result_length
                            ],
                        }
                    )
                messages.extend(tool_results)
                continue
            else:
                CONSOLE.print(
                    f"🤖 {self.name} is done:",
                    response.choices[0].message.content[
                        : CONFIG.maximum_tool_result_showing_length
                    ]
                    + "...",
                )
                return response.choices[0].message.content

    async def hint(self) -> str:
        raise NotImplementedError("hint method should be implemented")
