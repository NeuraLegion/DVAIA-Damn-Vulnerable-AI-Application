#!/bin/bash
# DVAIA - Damn Vulnerable AI Application
# Docker Compose wrapper script for easy startup
# Starts Ollama, Qdrant, and Flask app together

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

echo "Building and running DVAIA with Ollama and Qdrant..."
echo "First startup will download llama3.2 and nomic-embed-text models (2-3 minutes)"
echo ""
docker compose up --build
