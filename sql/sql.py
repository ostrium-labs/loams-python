"""Run parameterized read-only SQL through the loams.sql module."""
import os

from loams import Loams

NAMESPACE = os.environ.get("LOAMS_NAMESPACE", "examples-python")

with Loams.from_env(namespace=NAMESPACE) as loams:
    queries = [
        ("SELECT tenant, count(*) AS n FROM kb GROUP BY tenant ORDER BY tenant", []),
        ("SELECT n, body FROM kb WHERE tenant = $1 ORDER BY n", ["a"]),
        (
            "SELECT _id, body, _score FROM rrf("
            "vector_search('kb', [1.0, 0.0, 0.0], 'embedding', 10), "
            "text_search('kb', 'refund', 'body', 10)) LIMIT 3",
            [],
        ),
    ]
    for statement, params in queries:
        print("\n>", statement)
        for row in loams.sql.records(statement, params):
            print(row)
