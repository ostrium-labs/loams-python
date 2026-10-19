"""Run SQL over the collection that ../quickstart created."""
import os

from native import call

NAMESPACE = os.environ.get("LOAMS_NAMESPACE", "examples-python")


def sql(query: str) -> None:
    out = call(f"/v1/namespaces/{NAMESPACE}/sql", {"query": query})
    names = [c["name"] for c in out["columns"]]
    print("  " + " | ".join(names))
    for row in out["rows"]:
        print("  " + " | ".join(str(v) for v in row))


print("plain SQL")
sql("SELECT _id, body, tenant FROM kb ORDER BY _id")

print("hybrid search in SQL: rrf(vector_search, text_search)")
sql(
    "SELECT _id, body, _score FROM rrf("
    "vector_search('kb', [1.0, 0.0, 0.0], 'embedding', 10), "
    "text_search('kb', 'refund', 'body', 10)) LIMIT 3"
)
