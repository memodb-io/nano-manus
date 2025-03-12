<div align="center">
  <h1>🐜 nano_manus</h1>
  <p><strong>Implementing some features of Manus with MCP</strong></p>
  <p>
    <a href="https://pypi.org/project/nano_manus/" > 
    	<img src="https://img.shields.io/badge/python->=3.11-blue">
    </a>
    <a href="https://pypi.org/project/nano_manus/">
      <img src="https://img.shields.io/pypi/v/nano_manus.svg">
    </a>
  </p>
</div>


<div align="center">
    <picture>
      <img alt="Shows the Memobase Workflow" src="./examples/imgs/arch.png" width="80%">
    </picture>
  <p>nano-manus</p>
</div>



## Features

- **Small**: `nano_manus` is about 1000 LOC.
- **Using MCP**: `nano_manus` supports [loading MCP](./examples/load_mcp_tools.py) from [docker](https://hub.docker.com/u/mcp), `npx` and [Smithery](https://smithery.ai/)
- **Plan-then-Execute**: `nano_manus` will gather your agents, make the plans and then assign the correct jobs to your agents



## User Cases

- `Find all .py file and explain them to me`
- `Give me the latest weather in SF in last 7 days and save it to csv`

> Welcome to give more user cases!



## QuickStart

#### Setup

- [Brave Search API key](https://brave.com/search/api/)
- [Jina API key](https://jina.ai/)
- OpenAI API key

Your `.env` should look like:

```
BRAVE_API_KEY=BSAxxxx
JINA_API_KEY=jina_xxxx
OPENAI_API_KEY=sk-proj-XXXXX
```

#### Run default `nano-manus`

```bash
uv sync
uv run examples/basic_planner.py
```



## Abilities

- [x] Search Web (`mcp/brave-search`, `jina-ai-mcp-server`)
- [x] Local files operations (`@wonderwhy-er/desktop-commander`)
- [x] Execute codes and commands in your computer (`@wonderwhy-er/desktop-commander`)
- [ ] (coming soon) Read `.pdf, .doc`
- [ ] (coming soon) browser use





## Known Issues

- `Unable to exit`: seem like some MCPs will cause the problems of unable to exit the program when all the tasks were done.
- `nano-manus` will operate files and run command **on the current dir of your local computer**, make sure you don't run it on some important folders.
