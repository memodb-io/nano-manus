import asyncio
from .type import BaseMCP
from typing import Dict, List


class MCPPool:
    def __init__(self):
        self.mcp_clients: Dict[str, BaseMCP] = {}

    def add_mcp_client(self, name: str, mcp_client: BaseMCP):
        self.mcp_clients[name] = mcp_client

    def get_mcp_client(self, name: str) -> BaseMCP:
        return self.mcp_clients[name]

    def get_all_mcp_clients(self) -> List[BaseMCP]:
        return list(self.mcp_clients.values())
