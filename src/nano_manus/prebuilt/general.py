from ..types import BaseAgent
from ..env import CONFIG, llm_complete

PROMPT = """
You are {name}
{description}

Now, complete the task based on the above instructions.
"""


class GeneralAgent(BaseAgent):
    def __init__(self, name: str, description: str):
        self.__name = name
        self.__description = description

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    async def handle(self, instruction: str, global_ctx: dict) -> str:
        response = await llm_complete(
            model=CONFIG.prebuilt_general_model,
            messages=[
                {
                    "role": "system",
                    "content": PROMPT.format(
                        name=self.name, description=self.description
                    ),
                },
                {"role": "user", "content": instruction},
            ],
        )
        return response.choices[0].message.content
