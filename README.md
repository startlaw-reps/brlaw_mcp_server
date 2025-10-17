# Brazilian Law Research MCP Server

[🇧🇷 Leia em português](README.br.md)

A MCP (Model Context Protocol) server for agent-driven research on Brazilian law using official
sources.

<a href="https://glama.ai/mcp/servers/@pdmtt/brlaw_mcp_server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@pdmtt/brlaw_mcp_server/badge" alt="Brazilian Law Research Server MCP server" />
</a>

## Foreword

This server empowers models with scraping capacities, thus making research easier to anyone
legitimately interested in Brazilian legal matters.

This facility comes with a price: the risk of overloading the official sources' servers if misused.
Please be sure to keep the load on the sources to a reasonable amount.

## Requirements

- git
- uv (recommended) or Python >= 3.12
- Google Chrome

## How to use

### Option 1: Docker Deployment (Recommended for Production)

1. Clone the repository:

```bash
git clone https://github.com/pdmtt/brlaw_mcp_server.git
cd brlaw_mcp_server
```

2. Build and run with Docker Compose:

```bash
docker-compose up --build
```

Or build and run manually:

```bash
# Build the Docker image
docker build -t brlaw-mcp-server .

# Run the container
docker run -p 8000:8000 -v $(pwd)/logs:/app/logs brlaw-mcp-server
```

3. The MCP server will be available on `localhost:8000` for TCP connections.

### Option 2: Local Development

1. Clone the repository:

```bash
git clone https://github.com/pdmtt/brlaw_mcp_server.git
```

2. Install the dependencies

```bash
uv run patchright install
```

3. Setup your MCP client (e.g. Claude Desktop):

```json
{
  "mcpServers": {
    "brlaw_mcp_server": {
      "command": "uv",
      "args": ["--directory", "/<path>/brlaw_mcp_server", "run", "serve"]
    }
  }
}
```

### Network Mode (TCP)

For agent-based integrations, you can run the server in TCP mode:

```bash
# Local development
uv run serve --tcp --host 0.0.0.0 --port 8000

# Docker
docker run -p 8000:8000 brlaw-mcp-server
```

The server will accept MCP protocol connections on the specified host and port.

### Available Tools

- `StjLegalPrecedentsRequest`: Research legal precedents made by the National High Court of Brazil
  (STJ) that meet the specified criteria.
- `TstLegalPrecedentsRequest`: Research legal precedents made by the National High Labor Court of
  Brazil (TST) that meet the specified criteria.
- `StfLegalPrecedentsRequest`: Research legal precedents made by the Supreme Court (STF) that meet
  the specified criteria.

## Troubleshooting

### Docker Issues

**Container fails to start with browser errors:**

- Ensure you're using the latest Docker image: `docker pull brlaw-mcp-server`
- Check that all Chrome dependencies are installed in the container
- Verify the container has sufficient memory (recommended: 2GB+)

**Connection refused on port 8000:**

- Ensure the port is not already in use: `lsof -i :8000`
- Check Docker port mapping: `docker ps` should show `0.0.0.0:8000->8000/tcp`
- Verify firewall settings allow connections to port 8000

**Permission errors with logs:**

- Create logs directory with proper permissions: `mkdir -p logs && chmod 755 logs`
- Ensure Docker has write access to the mounted volume

### Network Mode Issues

**MCP client cannot connect:**

- Verify the server is running in TCP mode: `uv run serve --tcp --help`
- Check network connectivity: `telnet localhost 8000`
- Ensure the MCP client is configured for TCP transport, not stdio

**Browser automation fails:**

- Check that Patchright browser binaries are installed: `uv run patchright install chromium`
- Verify system dependencies for Chrome are available
- Check logs for specific browser error messages

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
