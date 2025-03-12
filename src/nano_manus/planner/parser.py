import re
from ..env import CONSOLE

CODE_BLOCK_PATTERN = re.compile(r"```tasks(.*?)```", re.DOTALL)
GOAL_BLOCK_PATTERN = re.compile(r"^(.*?)```tasks", re.DOTALL)


def parse_step(step: str) -> dict:
    code_blocks = CODE_BLOCK_PATTERN.findall(step)
    goal_blocks = GOAL_BLOCK_PATTERN.findall(step)
    if not len(goal_blocks):
        # CONSOLE.log("!Missing goal in this step")
        goal = ""
    else:
        goal = goal_blocks[0].strip()
    if not len(code_blocks):
        # CONSOLE.log("!Missing subtasks in this step")
        return goal, []
    else:
        subtasks = code_blocks[0].strip()
        subtasks = [l.strip() for l in subtasks.split("\n") if l.startswith("- ")]
        expressions = [parse_subtask_expression(st[2:]) for st in subtasks]
        expressions = [e for e in expressions if e is not None]
    return goal, expressions


def parse_subtask_expression(subtask: str) -> dict:
    # Match pattern: result_name = subtask(agent_id, "task")
    subtask = subtask.strip()

    # Split by '=' to separate result name and the rest
    result_name, expression = [x.strip() for x in subtask.split("=")]

    # Extract agent_id and param from subtask(agent_id, "param")
    # Remove 'subtask(' from start and ')' from end
    if not expression.startswith("subtask(") or not expression.endswith(")"):
        return None
    inner_content = expression[8:-1]

    # Split by comma, but only first occurrence to handle possible commas in the task string
    agent_id, param = [x.strip() for x in inner_content.split(",", 1)]

    # Remove quotes from param
    param = param.strip("\"'")

    return {"result_name": result_name, "agent_id": agent_id, "param": param}
