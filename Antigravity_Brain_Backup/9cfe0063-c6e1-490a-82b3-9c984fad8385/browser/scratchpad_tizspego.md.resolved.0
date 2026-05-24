# Task: Configure MCP Servers in Connect AI

## Goals
- [x] Understand what Connect AI is.
- [x] Find general instructions for adding MCP servers to Connect AI.
- [x] Find specific instructions for NotebookLM MCP server.
- [x] Find specific instructions for Stitch MCP server.

## Findings
- **Connect AI**: A VS Code/Cursor extension developed by wonseokjung. It's a local/offline AI coding agent with a "P-Reinforce" architecture. It automates knowledge management, file creation, and terminal execution. It integrates with Ollama, LM Studio, and Antigravity.
- **MCP Configuration**: The author recommends adding MCP servers to the `mcpServers` section of the JSON configuration (similar to Cursor or Claude Desktop).
- **NotebookLM MCP**: 
    - Repository: `wonseokjung/notebooklm-mcp`
    - Installation: Uses `uv` (Python). Command: `uvx notebooklm-mcp-server`.
    - Config: 
      ```json
      "notebooklm": {
        "command": "uv",
        "args": ["run", "notebooklm-mcp-server"]
      }
      ```
- **Stitch MCP**: 
    - Related Repo: `wonseokjung/stitch-skills` (forked from Google).
    - Service: Google's Stitch MCP server (stitch.withgoogle.com).
    - Installation: Follow Google's official Stitch MCP setup guide.

## Progress
- Completed research on all requested items.
- Found specific repositories and configuration details.