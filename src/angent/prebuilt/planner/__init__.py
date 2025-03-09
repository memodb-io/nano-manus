from .planner import Planner

__all__ = ["Planner"]


if __name__ == "__main__":
    import asyncio
    from ..general import GeneralAgent

    add_agent = GeneralAgent(name="Add Agent", description="Add two numbers")
    sub_agent = GeneralAgent(name="Subtract Agent", description="Subtract two numbers")

    wp = Planner()
    wp.add_agents([add_agent, sub_agent])
    result = asyncio.run(wp.handle("(10 - 2) + (3 - 8)", {}))
