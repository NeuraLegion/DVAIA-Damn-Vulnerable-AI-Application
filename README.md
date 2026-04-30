# DVAIA

## How to Run the Application

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
- Ollama at the host/port configured in your Docker Compose setup
- Qdrant at the host/port configured in your Docker Compose setup

Important:
- on first startup, Ollama downloads models, so startup can take several minutes
- the `/api/chat` endpoint can respond very slowly because the request is processed by a local LLM
- clients, proxies, load balancers, and HTTP libraries should use large `response timeout` and `read timeout` values
- for `curl`, using `--max-time 600` or higher is reasonable

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
  --data-raw '{"prompt":"PROMPT DATA","model_id":"ollama:llama3.2","options":{"temperature":1.2,"top_k":200,"top_p":0.95,"max_tokens":200,"repeat_penalty":1}}'
```

Example with timing and an explicit long timeout:

```bash
time curl 'http://127.0.0.1:5000/api/chat' \
  -X POST \
  -H 'Content-Type: application/json' \
  --no-buffer \
  --max-time 600 \
  --data-raw '{
    "prompt": "PROMPT DATA",
    "model_id": "ollama:llama3.2",
    "options": {
      "temperature": 0.7,
      "top_k": 40,
      "top_p": 0.9,
      "max_tokens": 30,
      "repeat_penalty": 1
    }
  }'
```

Example valid JSON body:

```json
{
  "prompt": "Say short hi,
  "options": {
    "temperature": 0.7,
    "top_k": 40,
    "top_p": 0.9,
    "max_tokens": 30,
    "repeat_penalty": 1
  }
}
```

Timeout note:
- if the request goes through `nginx`, `traefik`, `cloudflare tunnel`, `requests`, `axios`, or `fetch` behind a proxy, increase timeouts in advance
- if the timeout is too small, the client may terminate the connection before the model finishes generation
- if you need a faster response, reduce `max_tokens` and use a lighter model