#!/bin/bash
# DVAIA - Damn Vulnerable AI Application
# Docker Compose wrapper script for easy startup
# Starts Qdrant and Flask app (uses OpenAI API for inference)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if [ ! -f .env ]; then
    echo "Warning: .env file not found. Using defaults from docker-compose.yml"
    echo "Tip: Create .env from .env.example and set OPENAI_API_KEY."
else
    # Export .env so docker compose sees variables
    set -a
    source .env 2>/dev/null || true
    set +a
fi

echo "Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "Building and running DVAIA with Qdrant..."
echo ""
docker compose up --build
