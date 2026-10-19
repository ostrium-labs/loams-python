# fastapi-search

A FastAPI service with `GET /search?q=...&tenant=...` (hybrid vector + text, RRF) and `GET /health` (via the SDK). Vectors are a toy lookup so no model is needed. Run `../quickstart` first.

```sh
pip install fastapi uvicorn
cd fastapi-search && uvicorn app:app --port 8000
curl 'localhost:8000/search?q=refund&tenant=a'
```
