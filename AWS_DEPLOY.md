# AWS EC2 Deployment Guide

This guide covers deploying DVAIA to AWS EC2 with an OpenAI-compatible inference endpoint.

Security warning: this is intentionally vulnerable software for testing and education. Deploy only in isolated environments.

## Prerequisites

- AWS account with EC2 access
- SSH key pair
- Docker and Docker Compose support on instance
- OpenAI API key (or API key for your OpenAI-compatible provider)

## 1. Launch EC2 Instance

Recommended baseline:

- Instance type: `t3.small` or larger
- OS: Ubuntu 22.04 LTS
- Storage: 16 GB+

Note: compute requirements are lower than local-model deployments because inference is remote.

## 2. Configure Security Group

Typical inbound rules:

- SSH TCP 22 from your IP
- App TCP 5000 from your IP (or restricted CIDR)
- Optional Qdrant TCP 6333 from your IP (debugging only)

## 3. Install Docker

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
sudo usermod -aG docker "$USER"
sudo apt install docker-compose-plugin -y
```

Reconnect your SSH session, then verify:

```bash
docker --version
docker compose version
```

## 4. Deploy DVAIA

```bash
git clone https://github.com/your-username/DVAIA.git
cd DVAIA
cp .env.example .env
```

Edit `.env` and set at least:

```bash
OPENAI_API_KEY=sk-...
# Optional:
# OPENAI_BASE_URL=https://api.openai.com/v1
# DEFAULT_MODEL=openai:gpt-4o-mini
# AGENTIC_MODEL=openai:gpt-4o-mini
# EMBEDDING_MODEL=text-embedding-3-small
# PORT=5000
```

Start services:

```bash
docker compose up -d --build
```

Check status:

```bash
docker compose ps
docker compose logs -f dvaia
```

## 5. Verify

Health check:

```bash
curl http://127.0.0.1:5000/api/health
```

Chat check:

```bash
curl 'http://127.0.0.1:5000/api/chat' \
  -X POST \
  -H 'Content-Type: application/json' \
  --data-raw '{"prompt":"Say hi","model_id":"openai:gpt-4o-mini"}'
```

## Troubleshooting

### Missing API key

Symptom: chat endpoints return an error about `OPENAI_API_KEY`.

Fix:

- Ensure `.env` includes `OPENAI_API_KEY`
- Restart app container: `docker compose restart dvaia`

### Endpoint/auth errors

Symptom: 401/403/404/429 from model provider.

Fix:

- Validate API key
- Validate `OPENAI_BASE_URL` for your provider
- Check selected model exists for your account

### Qdrant unavailable

Symptom: RAG-related features fail.

Fix:

```bash
docker compose logs qdrant
docker compose restart qdrant
```

## Maintenance

- Update images regularly: `docker compose pull && docker compose up -d`
- Rotate API keys periodically
- Restrict network exposure to trusted IP ranges only
