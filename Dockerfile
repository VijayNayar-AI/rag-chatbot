FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY certs/zscaler-root.crt /usr/local/share/ca-certificates/zscaler-root.crt

RUN update-ca-certificates

COPY . .

RUN pip install uv

RUN uv sync --system-certs --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]