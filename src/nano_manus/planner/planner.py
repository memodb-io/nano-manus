import re
import json
from rich.markdown import Markdown
from ..env import CONFIG, llm_complete, LOG, CONSOLE
from ..worker.type import BaseWorker
from .prompts import PROMPT
from .parser import parse_step


class Planner:
    def __init__(self, max_steps: int = 10, max_tasks: int = 30):
        self.__workers: list[BaseWorker] = []
        self.__max_steps = max_steps
        self.__max_tasks = max_tasks

    @property
    def name(self) -> str:
        return "Planner"

    @property
    def description(self) -> str:
        return "Planner is a agent that plans the task into a list of steps."

    def add_workers(self, workers: list[BaseWorker]):
        self.__workers.extend(workers)

    async def handle(self, instruction: str, global_ctx: dict = {}) -> str:
        already_tasks = 0
        already_steps = 0
        LOG.info(
            f"Planning for {instruction}, using model: {CONFIG.prebuilt_plan_model}"
        )
        agent_maps = [
            {
                "agent_id": f"agent_{i}",
                "description": await worker.hint(),
            }
            for i, worker in enumerate(self.__workers)
        ]
        if not len(agent_maps):
            raise ValueError("No agents to plan")

        messages = (
            [
                {
                    "role": "system",
                    "content": PROMPT.format(
                        agent_descs=json.dumps(agent_maps, indent=2)
                    ),
                },
                {"role": "user", "content": instruction},
            ],
        )
        while already_tasks < self.__max_tasks and already_steps < self.__max_steps:
            response = await llm_complete(
                model=CONFIG.prebuilt_plan_model,
                messages=[
                    {
                        "role": "system",
                        "content": PROMPT.format(
                            agent_descs=json.dumps(agent_maps, indent=2)
                        ),
                    },
                    {"role": "user", "content": instruction},
                ],
            )
            response = response.choices[0].message.content
            goal, expressions = parse_step(response)
            CONSOLE.print("🤖: ", Markdown(goal))
            CONSOLE.print("🔍:", expressions)
            if not len(expressions):
                CONSOLE.log("🤖: No more steps to plan")
                break
            for e in expressions:
                agent_index = int(e["agent_id"].split("_")[-1])
                worker = self.__workers[agent_index]
                result = await worker.handle(e["task"], global_ctx)
                CONSOLE.print(f"🤖{worker.name}: ", result)

            exit()
            already_steps += 1
        return goal
