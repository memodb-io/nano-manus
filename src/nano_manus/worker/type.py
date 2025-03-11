from abc import ABC, abstractmethod
from ..mcp_tool.type import BaseMCP


class BaseWorker(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def handle(self, instruction: str, global_ctx: dict = {}) -> str:
        pass

    @abstractmethod
    async def hint(self) -> str:
        pass
