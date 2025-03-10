from abc import ABC, abstractmethod


class BaseAsyncAgent(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Agent class must have a name")

    @abstractmethod
    async def connect(self):
        raise NotImplementedError("Agent class must have a connect method")

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError("Agent class must have a disconnect method")

    @abstractmethod
    async def async_description(self) -> str:
        raise NotImplementedError("Agent class must have a async_description method")

    @abstractmethod
    async def handle(self, instruction: str, global_ctx: dict = None) -> str:
        raise NotImplementedError("Agent class must have a async_handle method")


class BaseAgent(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Agent class must have a name")

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError("Agent class must have a description")

    @abstractmethod
    async def handle(self, instruction: str, global_ctx: dict = None) -> str:
        raise NotImplementedError("Agent class must have a handle method")


class BaseManager(BaseAgent):

    @abstractmethod
    def add_agents(self, agents: list[BaseAgent]):
        raise NotImplementedError("WorkingPlace class must have a add_agents method")
