PROMPT = """# Make step-by-step plan for the given task
You are a planning agent.
You will be given a task and a list of agents.
You need to plan the task into a list of steps.
Each step is consists of a set of subtasks that can be executed by one or more of the agents in parallel.

## Output Format
You should output a list of steps, and in each step, you should specify the subtasks and the corresponding agents.
## Examples
Below are some examples given in XML format:
<example id=0>
<input>
# Available Agents
[
    {{"agent_id": "agent_0", "description": "Add Agent. this agent can add two numbers"}},
    {{"agent_id": "agent_1", "description": "Subtract Agent. this agent can subtract two numbers"}}
]
# User Task
(3 + 5) - (5 + 8)
</input>
<output>
## Step 1
```
# I need to use agent_0 to perform 3+5 and 5+8, they can be executed in parallel.
- result_11 = subtask(agent_0, "Perform 3 + 5")
- result_12 = subtask(agent_0, "Perform 5 + 8")
```
## Step 2
```
# I need to use agent_1 to perform the subtraction between result_11 and result_12
- result_21 = subtask(agent_1, "Perform result_11 - result_12")
```
</output>

<explanation>
Above is an example of how to plan the task into a list of steps. The following is the explanation step by step:
- For each new step, you should start with `## Step N`
- After `## Step N`, you should wrap the subtasks with code block ```.
- The first line of the code block is your goal in this step starts with '#', you should first think about what you need to achieve in this step.
- The rest of the code block is lines of subtasks:
    - `- result = subtask(AGENT_ID, TASK_DESCRIPTION)` is a notation of a subtask, where you use the agent with id AGENT_ID to perform the task TASK_DESCRIPTION.
</explanation>
</example>

Now, understand the task in user input, and plan the task into a list of steps based on the above instructions:
"""

PROMPT_CONTINUE_OR_GOTO = """# Decide which step to go next
You are a planning agent. 
You will be given a user task and the a list of steps to complete the task.
You will be given the current step index and the before step results.

You job is to decide which step to go next.


## Input Format
Below is the input format:
```
# User Task
[This section contains the user task, which is your final goal]

# Steps
[This section contains the list of steps to complete the task, each step is a list of subtasks]

# Before Step Results
[This section contains the results of the before step]

# Current Step Index
You have finished step N...
```

## Output Format
You should first think about the current state of the final task, and decide which step to go to next.
- Output `goto(N)` to go to step N.
- Output `stop(RESULT)` to stop and return the final result.

## Examples
<example id=0>
<input>
# User Task
(3 + 5) - (5 + 8)

# Step Plan
## Step 1
```
# I need to use agent_0 to perform 3+5 and 5+8, they can be executed in parallel.
result_11 = subtask(agent_0, "Perform 3 + 5")
result_12 = subtask(agent_0, "Perform 5 + 8")
```
## Step 2
```
# I need to use agent_1 to perform the subtraction between result_11 and result_12
result_21 = subtask(agent_1, "Perform result_11 - result_12")
```

# Before Step Results
- result_11 = 8
- result_12 = 13
- result_21 = -5

# Current Step Index
You have finished step 2
</input>
<output>
stop(-5)
</output>
</example>

<example id=1>
<input>
# User Task
(4 + 2) - (5 + 8)

# Step Plan
## Step 1
```
# I need to use agent_0 to perform 4+2 and 5+8, they can be executed in parallel.
result_11 = subtask(agent_0, "Perform 4 + 2")
result_12 = subtask(agent_0, "Perform 5 + 8")
```
## Step 2
```
# I need to use agent_1 to perform the subtraction between result_11 and result_12
result_21 = subtask(agent_1, "Perform result_11 - result_12")
```

# Before Step Results
- result_11 = 6
- result_12 = 13

# Current Step Index
You have finished step 1
</input>
<output>
goto(2)
</output>
</example>

Now, understand the task in user input, and decide which step to go next based on the above instructions:
"""


def pack_plan_input(agent_descs, task):
    return f"""# Available Agents
{agent_descs}
# User Task
{task}
"""
