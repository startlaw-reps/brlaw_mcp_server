# Containerize MCP Server with Network Support

## Overview

Transform the stdio-based MCP server into a network-accessible service running in Docker, suitable for OpenAI agent integration.

## Key Changes

### 1. Add Network Transport to MCP Server

**File:** `src/brlaw_mcp_server/presentation/mcp.py`

- Add TCP server support alongside existing stdio transport
- Modify `serve()` function to accept transport mode (stdio/tcp)
- Add CLI arguments for host/port configuration (default: 0.0.0.0:8000)
- Keep stdio as default for backward compatibility

### 2. Create Dockerfile

**File:** `Dockerfile` (new)

- Base image: `python:3.12-slim` for minimal footprint
- Install system dependencies: Chrome/Chromium browser dependencies
- Install uv package manager
- Copy project files and install with `uv sync`
- Install Patchright browser binaries via `uv run patchright install chromium`
- Expose port 8000
- Set environment variables for headless operation
- Use non-root user for security
- Entry point: `serve --tcp`

### 3. Docker Configuration Files

**Files:** `.dockerignore` (new), `docker-compose.yml` (new, optional)

- `.dockerignore`: Exclude `__pycache__`, `.git`, `tests/`, `*.pyc`, virtual environments
- `docker-compose.yml`: Optional helper for easy container management with environment variables

### 4. Update CLI Entry Point

**File:** `pyproject.toml`

- Ensure `serve` script supports CLI arguments for transport selection

### 5. Documentation

**Files:** `README.md`, potentially `README.br.md`

- Add Docker deployment section with build/run instructions
- Document TCP connection details for OpenAI agents
- Include example MCP client configuration for network mode
- Add troubleshooting section

## Technical Details

### Network Protocol

The MCP protocol works over stdio by default, but the `mcp` library supports network transports. We'll implement a TCP server using `asyncio` that wraps the MCP server's stdin/stdout operations.

### Browser in Docker

Patchright (Playwright fork) requires system dependencies for Chromium. The Dockerfile will install necessary packages like `libnss3`, `libatk1.0-0`, `libx11-xcb1`, etc.

### Security Considerations

- Run as non-root user inside container
- No authentication by default (suitable for internal agent communication)
- Could add optional authentication layer if needed later

### Volume Mounts

- Mount `mcp.log` location for persistent logging outside container
