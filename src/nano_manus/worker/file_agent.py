from ..env import CONFIG
from ..mcp_tool import TOOLS
from .mcp_agent import BaseMCPAgent


class FileAgent(BaseMCPAgent):
    def __init__(self):
        super().__init__(["local_file"])

    def overwrite_system(self):
        return f"""
You are a file agent, that can only operate files under `{CONFIG.use_dir}` path.


## Notes
- You need to translate the file path to relative path of `{CONFIG.use_dir}` when talking to user.
- Use absolute path when you need to operate files and calling tools.
"""

    @property
    def name(self) -> str:
        return "File Agent"

    async def hint(self) -> str:
        return f"""I'm File Agent.
I can handle file operations under `{CONFIG.use_dir}` path
Make sure you give me the clear file operations, make sure you give me the absolute file/dir path.
"""
