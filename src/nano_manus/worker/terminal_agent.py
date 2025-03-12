from ..env import CONFIG
from ..mcp_tool import TOOLS
from .mcp_agent import BaseMCPAgent


class TerminalAgent(BaseMCPAgent):
    def __init__(self):
        super().__init__(["terminal"])

    def overwrite_system(self):
        return f"""
You are a terminal agent. Your allowed path is {CONFIG.allowed_local_dir}, make sure your command is within this path.
## Notes
- When encounterng error like `directory does not exist`, you need to first look at the files and dirs in parent directory to see if the path is wrongly typed.
- When writing file, make sure the file path is within {CONFIG.allowed_local_dir} path and you can only create new file and dir under {CONFIG.allowed_local_dir}.
- When using `search_files`, you don't need to use wildcard like `*.py`, just use `.py` is enough.
- If you need to run some code, you can save it to file first and then try to run it.
- If you encounter error from terminal, try to fix it by running further commands.
"""

    @property
    def name(self) -> str:
        return "Terminal Agent"

    async def hint(self) -> str:
        return f"""I'm Terminal Agent. 
I can help you to:
- search local files, write/read text file(.txt/.md) content
- execute terminal commands, read terminal output
My allowed path is {CONFIG.allowed_local_dir}, make sure your command is within this path.
"""
