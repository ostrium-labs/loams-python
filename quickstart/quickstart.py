"""Connect, create a collection, upsert documents, run a hybrid search."""
import os

from loams import Loams
from loams.instance.v1.instance_pb2 import GetInstanceRequest

from native import ENDPOINT, call

NAMESPACE = os.environ.get("LOAMS_NAMESPACE", "examples-python")

# 1. Connect with the SDK and ask the instance what it is.
client = Loams(ENDPOINT, api_key=os.environ.get("LOAMS_API_KEY") or None)
info = client.instance.get_instance(GetInstanceRequest())
print(f"connected to {info.name} {info.server_version} ({ENDPOINT})")
print("serves:", ", ".join(client.system.served()))

# 2. A namespace and a collection: one text field, one keyword field, 3-d vectors.
try:
    call("/v1/namespaces", {"name": NAMESPACE})
except RuntimeError as err:
    if "already" not in str(err).lower() and "409" not in str(err):
        raise
try:
    call(f"/v1/namespaces/{NAMESPACE}/collections", {
        "name": "kb",
        "schema": {
            "fields": [
                {"name": "body", "source_path": "body", "kind": {"text": {"analyzer": "standard", "positions": True}}, "indexed": True, "fast": False},
                {"name": "tenant", "source_path": "tenant", "kind": "keyword", "indexed": True, "fast": True},
            ],
            "vectors": [{"name": "embedding", "dim": 3, "distance": "cosine"}],
            "sparse_vectors": [], "dynamic": "ignore", "max_fields": 1000,
        },
    })
except RuntimeError as err:
    if "already" not in str(err).lower() and "409" not in str(err):
        raise

# 3. Upsert documents (re-running replaces them by id).
call(f"/v1/namespaces/{NAMESPACE}/collections/kb/documents", {"ops": [
    {"upsert": {"id": 1, "source": {"body": "refund policy", "tenant": "a"}, "vectors": {"embedding": [1.0, 0.0, 0.0]}}},
    {"upsert": {"id": 2, "source": {"body": "shipping times", "tenant": "a"}, "vectors": {"embedding": [0.9, 0.1, 0.0]}}},
    {"upsert": {"id": 3, "source": {"body": "refund window", "tenant": "b"}, "vectors": {"embedding": [0.0, 0.0, 1.0]}}},
]})

# 4. Hybrid search: vector + BM25 text, filtered to tenant "a", fused with RRF.
result = call(f"/v1/namespaces/{NAMESPACE}/query", {
    "from": "collections.kb",
    "retrieve": [
        {"vector": {"field": "embedding", "query": [1.0, 0.0, 0.0], "k": 10}},
        {"text": {"field": "body", "query": "refund", "k": 10}},
    ],
    "filter": {"term": {"tenant": "a"}},
    "fuse": {"method": "rrf", "k": 60},
    "limit": 3,
})
for hit in result["hits"]:
    print(f'{hit["pk"]}  score={hit["score"]:.4f}  {hit["source"]["body"]}')
