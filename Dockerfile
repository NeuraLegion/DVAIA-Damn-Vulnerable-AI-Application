# DVAIA - Damn Vulnerable AI Application
# Intentionally vulnerable LLM web application for security testing education (OpenAI API)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install Python dependencies (no system deps for Gemini-only; add later for local models)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fonts for payload image generation; tesseract-ocr for Document Injection image uploads
RUN apt-get update && apt-get install -y --no-install-recommends fonts-dejavu-core tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Non-root user for better security
RUN useradd -m agentuser && chown -R agentuser:agentuser /app
USER agentuser

EXPOSE 5000

# Run with Gunicorn production WSGI server
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "api.server:app"]
