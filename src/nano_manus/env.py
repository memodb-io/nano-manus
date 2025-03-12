import os
import logging
import dotenv
from rich.console import Console
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from dataclasses import dataclass

dotenv.load_dotenv()
LOG = logging.getLogger("nano_manus")
CONSOLE = Console()
async_openai_client = None


def setup_openai_async_client(client: AsyncOpenAI):
    global async_openai_client
    async_openai_client = client


def get_async_openai_client() -> AsyncOpenAI:
    global async_openai_client
    if async_openai_client is None:
        async_openai_client = AsyncOpenAI()
    return async_openai_client


async def llm_complete(model: str, messages: list[dict], **kwargs) -> ChatCompletion:
    client = get_async_openai_client()
    response = await client.chat.completions.create(
        model=model, messages=messages, **kwargs
    )
    return response


@dataclass
class Config:
    prebuilt_general_model: str = "gpt-4o"
    prebuilt_plan_model: str = "gpt-4o"

    use_dir: str = "/home"
    allowed_local_dir: str = None

    maximum_tool_result_length: int = 10000
    maximum_tool_result_showing_length: int = 200

    def __post_init__(self):
        if self.allowed_local_dir is None:
            self.allowed_local_dir = os.getcwd()
        CONSOLE.print(f"Allowed local dir: {self.allowed_local_dir}")


CONFIG = Config()

LOGO = """                                      
 __   __     ______     __   __     ______                
/\ "-.\ \   /\  __ \   /\ "-.\ \   /\  __ \               
\ \ \-.  \  \ \  __ \  \ \ \-.  \  \ \ \/\ \              
 \ \_\\"\_\  \ \_\ \_\  \ \_\\"\_\  \ \_____\             
  \/_/ \/_/   \/_/\/_/   \/_/ \/_/   \/_____/             
                                                          
 __    __     ______     __   __     __  __     ______    
/\ "-./  \   /\  __ \   /\ "-.\ \   /\ \/\ \   /\  ___\   
\ \ \-./\ \  \ \  __ \  \ \ \-.  \  \ \ \_\ \  \ \___  \  
 \ \_\ \ \_\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \/\_____\ 
  \/_/  \/_/   \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/                                                                                                     
"""
