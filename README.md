# DVAIA

## How to Run the Application

## CI Secrets

For CI runs in GitHub Actions, configure repository secret `OPENAI_API_KEY`.

- Required secret: `OPENAI_API_KEY`
- Purpose: enables OpenAI-backed inference and embedding calls during CI

### 1) Configure environment

Create a `.env` file (or copy from `.env.example`) and set at least:

```bash
OPENAI_API_KEY=sk-...
# Optional for OpenAI-compatible providers:
# OPENAI_BASE_URL=https://api.openai.com/v1
# DEFAULT_MODEL=openai:gpt-4o-mini
# AGENTIC_MODEL=openai:gpt-4o-mini
# EMBEDDING_MODEL=text-embedding-3-small
```

### 2) Start with Docker Compose

```bash
docker compose up --build
```

Or with the helper script:

```bash
./run_docker.sh
```

Services:
- application at the host/port configured in your Docker Compose setup
- Qdrant at the host/port configured in your Docker Compose setup

Important:
- the `/api/chat` endpoint depends on your external OpenAI-compatible endpoint latency
- clients, proxies, load balancers, and HTTP libraries should use sufficiently large `response timeout` and `read timeout` values

## Example `/api/chat` Usage

Endpoint:

```text
POST /api/chat
```

Minimal example:

```bash
curl 'http://127.0.0.1:5000/api/chat' \
  -X POST \
  -H 'Content-Type: application/json' \
  --data-raw '{"prompt":"PROMPT DATA","model_id":"openai:gpt-4o-mini","options":{"temperature":0.7,"top_p":0.9,"max_tokens":200}}'
```

Example valid JSON body:

```json
{
  "prompt": "Say short hi",
  "model_id": "openai:gpt-4o-mini",
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 30
  }
}
```