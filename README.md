# Loams Python examples

These examples target **Loams SDK 0.1.2**. Installation and CI require the matching
0.1.2 packages and release tags to be published.

[Loams](https://loams.dev) is an open-source data engine that keeps your data in your own bucket and serves hybrid search (vector, BM25 and filters) and SQL over it. This repo holds example apps for the [Python SDK](https://github.com/ostrium-labs/loams/tree/main/sdks/python) (`loams` 0.1.2).

| Example | What it shows |
|---|---|
| [quickstart](quickstart) | connect, create a collection, upsert documents, hybrid search |
| [sql](sql) | SQL over the collection, including `rrf(vector_search(...), text_search(...))` |
| [fastapi-search](fastapi-search) | a FastAPI `/search` endpoint |

## Install

```sh
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

For local SDK development, explicitly install a checkout of the matching release:

```sh
git clone --branch v0.1.2 --depth 1 https://github.com/ostrium-labs/loams
pip install ./loams/sdks/python
```

## Run against a local engine

Start an engine (`cargo run -p loams -- dev` from the [monorepo](https://github.com/ostrium-labs/loams), or the compose stack from [docs/release/preview.md](https://github.com/ostrium-labs/loams/blob/main/docs/release/preview.md)), then:

```sh
export LOAMS_ENDPOINT=http://127.0.0.1:8080   # default
export LOAMS_API_KEY=...                       # only if auth is on
python quickstart/quickstart.py
python sql/sql.py
```

Examples read and write only the namespace `examples-python` (override with `LOAMS_NAMESPACE`).

## A note on the SDK surface

The SDK provides namespaces, collections, documents, search, vector, graph, SQL and streams on both sync and async clients. These examples retain the native HTTP JSON helper ([`quickstart/native.py`](quickstart/native.py)) for their HTTP route examples. The [SDK notes example](https://github.com/ostrium-labs/loams/blob/v0.1.2/sdks/python/examples/notes/main.py) demonstrates builders, collection handles and SDK SQL.

Docs: <https://loams.dev/docs>. License: Apache-2.0.
