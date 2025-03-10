import logging
from rich.console import Console
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from dataclasses import dataclass

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
    prebuilt_general_model: str = "gpt-4o-mini"
    prebuilt_plan_model: str = "gpt-4o"


CONFIG = Config()
