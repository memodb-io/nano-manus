from ..env import CONFIG
from ..mcp_tool import TOOLS
from .mcp_agent import BaseMCPAgent


class CodeAgent(BaseMCPAgent):
    def __init__(self):
        super().__init__(["terminal", "search_web", "read_webpage"])

    def overwrite_system(self):
        return f"""
You are a code agent. Your allowed path is {CONFIG.allowed_local_dir}, make sure your command is within this path.
You need to find programable solutions to solve the problems w
## Requirements
- You default coding language is `Python`
- You will use `uv` to manage dependencies, install packages and init a python project
- You will have website access, and you can use terminal to read/write and run your codes.
- Find revelant resources/bug-fixer or tutorials in StackOverflow or github before you start to 
- You need to read the output/error from the terminal to detect the bugs/errors
- You need to install the terminal command that is missing
- If you don't know how to use some commands, try search online and gain the information.
- Some default python package you may need:
    - pandas: load and analysis files
    - numpy: numerical computing
    - matplotlib: data visualization
- Remember to save your code with structures, using terminal write functions
- You can use code/scripts to do anything under {CONFIG.allowed_local_dir}, don't ask my opinion.
- You have capability to access external APIs or perform web scraping by write code, and run it in terminal
- Don't give up on the first try, always try to use python script to find a solution.

## System Infromation
- OS: {CONFIG.platform}
- Package Manager: {CONFIG.pkg_manager}
- Python package manager: `uv`
"""

    @property
    def name(self) -> str:
        return "Code Agent"

    async def hint(self) -> str:
        return f"""I'm Code Agent. 
I'm can use online search and code editor to write code and solve problems.
There are the following things I can do:
- Data analysis
- Convert files
- Run scripts from terminal
- Deploy web apps and services

## Note
- If you found out you're lacking of tools to deliver the results to user, you can state your requirements in details, I will use programs to solve the problems.
My allowed path is {CONFIG.allowed_local_dir}, make sure your command is within this path.
"""
