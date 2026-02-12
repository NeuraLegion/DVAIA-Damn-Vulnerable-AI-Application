#!/bin/bash
# Run red-team-agent API in a contained Docker setup (Gemini now; local models in container next).
# Always run from the directory containing this script so volume ".:/app" mounts the correct project.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

if [ ! -f .env ]; then
    echo "Tip: Copy .env.example to .env and set GEMINI_API_KEY (and optionally DEFAULT_MODEL, PORT, REDTEAM_API_URL)."
else
    # Export .env so docker compose sees DEFAULT_MODEL etc. (e.g. when using sudo)
    set -a
    source .env 2>/dev/null || true
    set +a
fi

echo "Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "Building and running red-team-agent in Docker..."
docker compose up --build
