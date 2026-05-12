#!/bin/bash
# DVAIA - Damn Vulnerable AI Application
# Docker Compose wrapper script for easy startup
# Starts OpenAI-backed app and Qdrant together

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if [ ! -f .env ]; then
    echo "Warning: .env file not found. Using defaults from docker-compose.yml"
    echo "Tip: Create .env file to customize PORT, DEFAULT_MODEL, etc."
else
    # Export .env so docker compose sees variables
    set -a
    source .env 2>/dev/null || true
    set +a
fi

echo "Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "Building and running DVAIA with OpenAI endpoint and Qdrant..."
echo "Make sure OPENAI_API_KEY is set in your .env file before startup"
echo ""
docker compose up --build
