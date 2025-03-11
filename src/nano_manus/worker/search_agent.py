from ..env import CONFIG
from ..mcp_tool import TOOLS
from .mcp_agent import BaseMCPAgent


class SearchAgent(BaseMCPAgent):
    def __init__(self):
        super().__init__(["search_web"])

    @property
    def name(self) -> str:
        return "Search Web Agent"

    async def hint(self) -> str:
        return f"""I'm Search Web Agent. 
Tell me what I need to search, and I will search the online, realtime results for you.
"""
