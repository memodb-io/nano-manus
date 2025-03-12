import re
import json
from rich.markdown import Markdown
from ..env import CONFIG, llm_complete, LOG, CONSOLE, LOGO
from ..worker.type import BaseWorker
from .prompts import PROMPT
from .parser import parse_step


class Planner:
    def __init__(
        self, max_steps: int = 30, max_tasks: int = 60, workers: list[BaseWorker] = []
    ):

        self.__workers: list[BaseWorker] = workers
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

    def exit_or_not(self, up: str):
        up = up.strip()
        if up == "quit" or not up:
            CONSOLE.print("[green]This session is ended.[/green]")
            return True
        return False

    async def outer_loop(self):
        CONSOLE.print(LOGO)
        agent_hints = "# Available Agents\n"
        for w in self.__workers:
            agent_hints += f"## {w.name}\n"
            agent_hints += f"{await w.hint()}\n"
        CONSOLE.print(Markdown(agent_hints + "---"))

        while True:
            user_input = CONSOLE.input(
                "🤖: [green bold]How are you! Would you like to ask me to do anything?[/green bold](ctrl+c to quit)\n👉: "
            )
            if self.exit_or_not(user_input):
                break
            else:
                await self.handle(user_input)

    async def handle(self, instruction: str) -> str:
        global_ctx = {"results": {}}
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
        messages = [
            {
                "role": "system",
                "content": PROMPT.format(agent_descs=json.dumps(agent_maps, indent=2)),
            },
            {"role": "user", "content": instruction},
        ]

        while True:
            if already_tasks >= self.__max_tasks or already_steps >= self.__max_steps:
                CONSOLE.print(
                    "[red]Nano-Manus stop to work because the maximum step is reached.[/red]"
                )
                break

            stream_response = await llm_complete(
                model=CONFIG.prebuilt_plan_model, messages=messages, stream=True
            )
            # response = response.choices[0].message.content
            response = ""
            CONSOLE.rule("nano-manus response")
            async for chunk in stream_response:
                if chunk.choices[0].delta.content is None:
                    break
                print(chunk.choices[0].delta.content, end="", flush=True)
                response += chunk.choices[0].delta.content
            print()
            messages.append({"role": "assistant", "content": response})
            goal, expressions = parse_step(response)
            if not len(expressions):
                CONSOLE.log("🤖: No more steps to plan")
                user_input = CONSOLE.input(
                    "🤖: [green bold]Do you have further commands?[/green bold] (type `quit` to leave)\n👉: "
                )
                if self.exit_or_not(user_input):
                    break
                else:
                    messages.append(
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    )
                    continue
            current_results = {}
            for e in expressions:
                agent_index = int(e["agent_id"].split("_")[-1])
                result_id = e["result_name"]
                worker = self.__workers[agent_index]
                CONSOLE.rule(f"{worker.name} is working")

                result = await worker.handle(e["param"], global_ctx)
                global_ctx["results"][result_id] = result
                current_results[result_id] = result
                already_tasks += 1

            user_feedback = "\n".join(
                [f"- {r}: {rr}" for r, rr in current_results.items()]
            )
            messages.append(
                {
                    "role": "user",
                    "content": f"Here are the results from the previous steps:\n{user_feedback}",
                }
            )
            already_steps += 1
        return goal
