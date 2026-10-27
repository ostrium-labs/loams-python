"""FastAPI search endpoint backed by the published Loams app modules.

    uvicorn app:app --port 8000
    curl 'localhost:8000/search?q=refund&tenant=a'
"""
import os

from fastapi import FastAPI, HTTPException, Query
from google.protobuf import json_format
from loams import Filter, Loams, rrf
from loams.instance.v1.instance_pb2 import GetInstanceRequest

NAMESPACE = os.environ.get("LOAMS_NAMESPACE", "examples-python")
EMBED = {
    "refund": [1.0, 0.0, 0.0],
    "shipping": [0.9, 0.1, 0.0],
    "window": [0.0, 0.0, 1.0],
}

app = FastAPI(title="Loams search")
client = Loams.from_env(namespace=NAMESPACE)
kb = client.collection("kb")


def embed(text: str) -> list[float]:
    vector = [0.0, 0.0, 0.0]
    for word in text.lower().split():
        for index, value in enumerate(EMBED.get(word, [0.0, 0.0, 0.0])):
            vector[index] += value
    return vector if any(vector) else [1.0, 1.0, 1.0]


@app.get("/health")
def health() -> dict:
    info = client.instance.get_instance(GetInstanceRequest())
    return {"instance": info.name, "version": info.server_version}


@app.get("/search")
def search(q: str = Query(min_length=1), tenant: str | None = None, limit: int = 5) -> dict:
    builder = (
        kb.query()
        .text(q, fields=["body"])
        .vector("embedding", embed(q), k=20)
        .fuse(rrf(60))
        .limit(max(1, min(limit, 50)))
    )
    if tenant:
        builder = builder.filter(Filter.eq("tenant", tenant))
    try:
        result = kb.search(builder)
    except Exception as err:
        raise HTTPException(502, str(err)) from None
    return {
        "hits": [
            {
                "id": json_format.MessageToDict(hit.pk),
                "score": hit.score,
                **json_format.MessageToDict(hit.source),
            }
            for hit in result.hits
        ]
    }
