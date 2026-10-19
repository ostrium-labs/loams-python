"""A FastAPI search endpoint over the quickstart collection.

    uvicorn app:app --port 8000
    curl 'localhost:8000/search?q=refund&tenant=a'
"""
import os

from fastapi import FastAPI, HTTPException, Query
from loams import Loams
from loams.instance.v1.instance_pb2 import GetInstanceRequest

from native import ENDPOINT, call

NAMESPACE = os.environ.get("LOAMS_NAMESPACE", "examples-python")
EMBED = {  # toy "embeddings" so the example needs no model
    "refund": [1.0, 0.0, 0.0], "shipping": [0.9, 0.1, 0.0], "window": [0.0, 0.0, 1.0],
}

app = FastAPI(title="Loams search")
client = Loams(ENDPOINT, api_key=os.environ.get("LOAMS_API_KEY") or None)


def embed(text: str) -> list[float]:
    vec = [0.0, 0.0, 0.0]
    for word in text.lower().split():
        for i, x in enumerate(EMBED.get(word, [0.0, 0.0, 0.0])):
            vec[i] += x
    return vec if any(vec) else [1.0, 1.0, 1.0]


@app.get("/health")
def health() -> dict:
    info = client.instance.get_instance(GetInstanceRequest())
    return {"instance": info.name, "version": info.server_version}


@app.get("/search")
def search(q: str = Query(min_length=1), tenant: str | None = None, limit: int = 5) -> dict:
    body = {
        "from": "collections.kb",
        "retrieve": [
            {"vector": {"field": "embedding", "query": embed(q), "k": 20}},
            {"text": {"field": "body", "query": q, "k": 20}},
        ],
        "fuse": {"method": "rrf", "k": 60},
        "limit": limit,
    }
    if tenant:
        body["filter"] = {"term": {"tenant": tenant}}
    try:
        out = call(f"/v1/namespaces/{NAMESPACE}/query", body)
    except RuntimeError as err:
        raise HTTPException(502, str(err)) from None
    return {"hits": [{"id": h["pk"], "score": h["score"], **h["source"]} for h in out["hits"]]}
