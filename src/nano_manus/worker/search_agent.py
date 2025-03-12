from ..env import CONFIG
from ..mcp_tool import TOOLS
from .mcp_agent import BaseMCPAgent


class SearchAgent(BaseMCPAgent):
    def __init__(self):
        super().__init__(["search_web", "read_webpage"])

    def overwrite_system(self):
        return """
You're a search agent. You're able to search the web and read webpages.
You need to search the web based on the user's instruction.
Pick the most informative and relevant results from the search and read their full content using read_webpage tool.
"""

    @property
    def name(self) -> str:
        return "Search Web Agent"

    async def hint(self) -> str:
        return f"""I'm Search Web Agent. 
Tell me what I need to search, and I will search the online, realtime results for you.
"""
