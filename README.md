# Brazilian Law Research MCP Server

[🇧🇷 Leia em português](README.br.md)

A MCP (Model Context Protocol) server for agent-driven research on Brazilian law.

## Requirements

- git
- uv (recommended) or Python >= 3.11
- Google Chrome

## How to use

1. Clone the repository:
```bash
git clone https://github.com/pdmtt/brlaw_mcp_server.git
```

2. Setup your MCP client (e.g. Claude Desktop):
```json
{
  "mcpServers": {
    "brlaw_mcp_server": {
      "command": "uv",
      "args": [
        "--directory",
        "/<path>/brlaw_mcp_server",
        "run",
        "brlaw_mcp_server"
      ]
    }
  }
}
```

### Available Tools

- `pesquisar_precedentes_judiciais`: Research legal precedents that meet the specified criteria.

## Development

### Tooling

The project uses:
- Ruff for linting and formatting.
- BasedPyright for type checking.
- Pytest for testing.

### Language

Resources, tools and prompts related stuff must be written in Portuguese, because this project aims 
to be used by non-dev folks, such as lawyers and law students. 

Technical legal vocabulary is highly dependent on a country's legal tradition and translating it is 
no trivial task.

Development related stuff should stick to English as conventional, such as source code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.