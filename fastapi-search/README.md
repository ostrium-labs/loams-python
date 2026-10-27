# fastapi-search

A FastAPI service with `GET /search?q=...&tenant=...` using the published SDK's collection handle, search builder and hybrid text/vector query. Vectors are a toy lookup so no embedding model is needed. Run quickstart first.

```sh
pip install fastapi uvicorn
cd fastapi-search && uvicorn app:app --port 8000
curl 'localhost:8000/search?q=refund&tenant=a'
```
