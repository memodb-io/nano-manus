<div align="center">
  <h1>🐜 angent</h1>
  <p><strong>Educational Multi-Agent Scaffold( 🚧Still in Development🚧)</strong></p>
  <p>
    <a href="https://pypi.org/project/angent/" > 
    	<img src="https://img.shields.io/badge/python->=3.11-blue">
    </a>
    <a href="https://pypi.org/project/angent/">
      <img src="https://img.shields.io/pypi/v/angent.svg">
    </a>
  </p>
</div>




## Features

- **Small**: `angent` will be less than 1000 LOC.
- **MCP Agent in one line**: Check [examples](./examples)
- **Plan-then-Execute**: `angent` will gather your agents, make the plans and then assign the correct jobs to your agents



## QuickStart

#### Run a MCP agent

```bash
uv sync
uv run examples/file_agent_demo.py
```

This agent will write `Angent is here` to the file `./examples/hello_world.txt`

