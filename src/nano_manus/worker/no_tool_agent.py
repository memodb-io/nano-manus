from .type import BaseWorker
from ..env import CONFIG, llm_complete


class NoToolWorker(BaseWorker):
    def __init__(self, name: str, description: str):
        self.__name = name
        self.__description = description
        self.prompt = f"You're a {self.__name}, {self.__description}"

    @property
    def name(self) -> str:
        return self.__name

    async def hint(self) -> str:
        return f"I'm a {self.__name}, {self.__description}"

    async def handle(self, instruction: str, global_ctx: dict) -> str:
        response = await llm_complete(
            model=CONFIG.prebuilt_general_model,
            messages=[
                {
                    "role": "system",
                    "content": self.prompt,
                },
                {"role": "user", "content": instruction},
            ],
        )
        return response.choices[0].message.content
