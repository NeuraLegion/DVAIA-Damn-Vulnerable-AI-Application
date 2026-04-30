# DVAIA

## How to Run the Application

### Prerequisites

Set your OpenAI API key in `.env` (copy from `.env.example`):

```bash
cp .env.example .env
# Edit .env and set: OPENAI_API_KEY=your-openai-api-key-here
```

### With Docker Compose

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
- `OPENAI_API_KEY` must be set in `.env` before starting
- the `/api/chat` endpoint calls the OpenAI API; ensure your key has sufficient quota
- clients, proxies, load balancers, and HTTP libraries should use adequate `response timeout` values

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
  --data-raw '{"prompt":"PROMPT DATA","model_id":"gpt-4o-mini","options":{"temperature":1.2,"top_p":0.95,"max_tokens":200}}'
```

Example with timing and an explicit long timeout:

```bash
time curl 'http://127.0.0.1:5000/api/chat' \
  -X POST \
  -H 'Content-Type: application/json' \
  --no-buffer \
  --max-time 120 \
  --data-raw '{
    "prompt": "PROMPT DATA",
    "model_id": "gpt-4o-mini",
    "options": {
      "temperature": 0.7,
      "top_p": 0.9,
      "max_tokens": 30
    }
  }'
```

Example valid JSON body:

```json
{
  "prompt": "Say short hi",
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 30
  }
}
```
