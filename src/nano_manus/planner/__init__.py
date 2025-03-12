from .planner import Planner

__all__ = ["Planner"]


if __name__ == "__main__":
    import asyncio
    from ..worker.no_tool_agent import NoToolWorker

    search_agent = NoToolWorker(
        name="Search Agent", description="Search the web for information"
    )
    db_agent = NoToolWorker(name="DB Agent", description="Operate the database")

    wp = Planner()
    wp.add_workers([search_agent, db_agent])
    result = asyncio.run(
        wp.handle(
            "Search the web information for the last 30 days' weather, and save it to DB",
        )
    )
    print(result)
