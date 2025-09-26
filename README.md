# Chatbot Backend

Backend para el chatbot basado en FastAPI y LangChain, con soporte para múltiples proveedores de LLM y memoria configurable.

## Requisitos

- Python 3.11+
- Poetry 1.7+

## Configuración

```bash
poetry install
cp .env.example .env
```

Edita `.env` para definir proveedor de LLM (`stub`, `local`, `openai`, `anthropic`), URL de base de datos y nivel de logs.

## Ejecución

```bash
poetry run uvicorn app.main:app --reload
```

El servicio queda expuesto en `http://localhost:8000`. Endpoint principal: `POST /api/v1/chat`. También hay `GET /health` para chequeos rápidos.

## Pruebas

```bash
poetry run pytest
```

## Docker (opcional)

```bash
docker build -t chatbot-backend -f docker/Dockerfile .
docker run -p 8000:8000 chatbot-backend
```