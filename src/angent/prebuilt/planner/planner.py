import re
import json
from ...types import BaseManager, BaseAgent
from ...env import CONFIG, llm_complete, LOG, CONSOLE
from .prompts import PROMPT, pack_plan_input, PROMPT_CONTINUE_OR_GOTO
from .parser import parse_steps


class Planner(BaseManager):
    def __init__(self, max_steps: int = 10, max_tasks: int = 30):
        self.__agents: list[BaseAgent] = []
        self.__max_steps = max_steps
        self.__max_tasks = max_tasks

    @property
    def name(self) -> str:
        return "Planner"

    @property
    def description(self) -> str:
        return "Planner is a agent that plans the task into a list of steps."

    def add_agents(self, agents: list[BaseAgent]):
        self.__agents.extend(agents)

    async def handle(self, instruction: str, global_ctx: dict = {}) -> str:
        already_tasks = 0
        already_steps = 0
        LOG.info(
            f"Planning for {instruction}, using model: {CONFIG.prebuilt_plan_model}"
        )
        agent_maps = [
            {"agent_id": f"agent_{i}", "description": f"{ag.name}; {ag.description}"}
            for i, ag in enumerate(self.__agents)
        ]
        if not len(agent_maps):
            raise ValueError("No agents to plan")

        response = await llm_complete(
            model=CONFIG.prebuilt_plan_model,
            messages=[
                {"role": "system", "content": PROMPT},
                {
                    "role": "user",
                    "content": pack_plan_input(
                        json.dumps(agent_maps, indent=2), instruction
                    ),
                },
            ],
        )
        response = response.choices[0].message.content
        steps = parse_steps(response)
        CONSOLE.print("Steps: ", steps)
        while already_tasks < self.__max_tasks and already_steps < self.__max_steps:
            pass
            already_steps += 1
        return steps
