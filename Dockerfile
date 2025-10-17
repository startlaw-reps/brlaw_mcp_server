# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Chrome/Chromium
RUN apt-get update && apt-get install -y \
    # Chrome dependencies
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libgdk-pixbuf-2.0-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    # Additional dependencies for web scraping
    wget \
    curl \
    ca-certificates \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Create a non-root user
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install Python dependencies
RUN uv sync --frozen

# Install Patchright browser binaries
RUN uv run patchright install chromium

# Create directory for logs and cache
RUN mkdir -p /app/logs /home/mcpuser/.cache && chown -R mcpuser:mcpuser /app /home/mcpuser

# Switch to non-root user
USER mcpuser

# Expose port 8000 for TCP mode
EXPOSE 8000

# Set the entry point to run the server in TCP mode
ENTRYPOINT ["uv", "run", "serve", "--tcp", "--host", "0.0.0.0", "--port", "8000"]
