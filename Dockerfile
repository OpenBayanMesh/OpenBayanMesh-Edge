FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN adduser --system --group appuser
USER appuser

COPY --chown=appuser:appuser . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
