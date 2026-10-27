"""Create a namespace and collection, then exercise the 0.1.2 app modules."""
import json
import os

from google.protobuf import json_format

from loams import AlreadyExistsError, Filter, Loams, Schema, rrf
from loams.collection.v1.collection_pb2 import CreateCollectionRequest, CreateNamespaceRequest
from loams.collection.v1.query_pb2 import SearchRequest
from loams.graph.v1.graph_pb2 import ExecuteRequest, ListGraphsRequest
from loams.instance.v1.instance_pb2 import GetInstanceRequest
from loams.stream.v1.stream_pb2 import CreateStreamRequest, ProduceRequest, Record

NAMESPACE = os.environ.get("LOAMS_NAMESPACE", "examples-python")

with Loams.from_env(namespace=NAMESPACE, session_consistency=True) as loams:
    info = loams.instance.get_instance(GetInstanceRequest())
    print(f"connected to {info.name} {info.server_version} (namespace {NAMESPACE})")
    print("served packages:", ", ".join(loams.system.served()))

    try:
        loams.namespaces.create(CreateNamespaceRequest(namespace=NAMESPACE))
    except AlreadyExistsError:
        pass

    schema = Schema().text("body").keyword("tenant").i64("n").vector("embedding", 3)
    try:
        loams.collections.create(
            json_format.ParseDict(
                {"name": "kb", "schema": schema.to_json()}, CreateCollectionRequest()
            )
        )
    except AlreadyExistsError:
        pass

    kb = loams.collection("kb")
    kb.upsert([
        {"id": 1, "source": {"body": "refund policy", "tenant": "a", "n": 1}, "vectors": {"embedding": [1, 0, 0]}},
        {"id": 2, "source": {"body": "shipping times", "tenant": "a", "n": 2}, "vectors": {"embedding": [0.9, 0.1, 0]}},
        {"id": 3, "source": {"body": "refund window", "tenant": "b", "n": 3}, "vectors": {"embedding": [0, 0, 1]}},
    ])

    hybrid = kb.search(
        kb.query()
        .text("refund", fields=["body"])
        .vector("embedding", [1, 0, 0], k=10)
        .fuse(rrf(60))
        .filter(Filter.eq("tenant", "a"))
        .limit(3)
    )
    for hit in hybrid.hits:
        print("hybrid", hit.pk, hit.score, hit.source)

    # Exercise the generated loams.vector module with the typed protobuf request.
    vector_request = json_format.ParseDict(
        {
            "namespace": NAMESPACE,
            "collection": "kb",
            "retrievers": [{"vector": {"field": "embedding", "query": [1, 0, 0], "k": 3}}],
            "filter": Filter.eq("tenant", "a"),
            "limit": 3,
        },
        SearchRequest(),
    )
    vector = loams.vector.search(vector_request)
    print("vector hits:", len(vector.hits))

    for row in loams.sql.records(
        "SELECT tenant, count(*) AS n FROM kb WHERE n >= $1 GROUP BY tenant ORDER BY tenant", [1]
    ):
        print("sql", row["tenant"], row["n"])

    loams.streams.create(CreateStreamRequest(name="kb-events", partitions=1))
    loams.streams.produce(
        ProduceRequest(
            stream="kb-events",
            records=[Record(value=json.dumps({"document": 1, "action": "indexed"}).encode())],
            producer_id="python-example",
            producer_seq=1,
        )
    )
    for event in loams.streams.subscribe("kb-events"):
        print("stream event offset:", event.offset)
        break

    # Graph is experimental and feature-gated; use it only if enabled and a
    # graph already exists in this namespace.
    if "loams.graph.v1" in loams.system.served():
        graphs = loams.graph.list(ListGraphsRequest(namespace=NAMESPACE, page_size=1))
        if graphs.graphs:
            result = loams.graph.query(
                ExecuteRequest(
                    namespace=NAMESPACE,
                    graph=graphs.graphs[0].name,
                    statement="RETURN 1 AS value",
                    language=1,
                    read_only=True,
                )
            )
            print("graph rows:", len(result.rows.rows) if result.rows else 0)
        else:
            print("graph is enabled; create a graph before running the optional GQL query")
    else:
        print("graph is experimental and not enabled in this engine build")
