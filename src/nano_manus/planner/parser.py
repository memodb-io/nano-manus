import re

CODE_BLOCK_PATTERN = re.compile(r"<tasks>(.*?)</tasks>", re.DOTALL)
TASK_BLOCK_PATTERN = re.compile(r"<subtask>(.*?)</subtask>", re.DOTALL)
GOAL_BLOCK_PATTERN = re.compile(r"^(.*?)<tasks>", re.DOTALL)


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
        subtask_blocks = TASK_BLOCK_PATTERN.findall(subtasks)
        expressions = [parse_subtask_expression(st.strip()) for st in subtask_blocks]
        expressions = [e for e in expressions if e is not None]
    return goal, expressions


def parse_subtask_expression(subtask: str) -> dict:
    # Match pattern: result_name = subtask(agent_id, "task")
    subtask = subtask.strip()

    # Split by '=' to separate result name and the rest
    parts = subtask.split("=")
    result_name, expression = (
        parts[0].strip(),
        "=".join(parts[1:]).strip(),
    )

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


if __name__ == "__main__":
    print(
        parse_step(
            """
### Step 3: Write a Python script to load the CSV file.

Sub-goal: Use the Terminal Agent to create a Python file that loads and prints the content of the `sf_weather.csv` file.

<tasks>
<subtask>
result_31 = subtask(agent_1, "Create a Python file named 'load_sf_weather.py' with the following content:\n\n```\nimport csv\n\nwith open('sf_weather.csv', 'r') as file:\n    reader = csv.reader(file)\n    for row in reader:\n        print(', '.join(row))\n```\n")
</subtask>
</tasks>

Please let me know once this step is completed or if there are any issues.
"""
        )
    )
