# Loams Python examples

[Loams](https://loams.dev) is an open-source data engine that keeps your data in your own bucket and serves hybrid search (vector, BM25 and filters) and SQL over it. This repo holds example apps for the [Python SDK](https://github.com/ostrium-labs/loams/tree/main/sdks/python) (`loams` 0.1.0).

| Example | What it shows |
|---|---|
| [quickstart](quickstart) | connect, create a collection, upsert documents, hybrid search |
| [sql](sql) | SQL over the collection, including `rrf(vector_search(...), text_search(...))` |
| [fastapi-search](fastapi-search) | a FastAPI `/search` endpoint |

## Install

```sh
python -m venv .venv && . .venv/bin/activate
pip install loams==0.1.0 fastapi uvicorn
```

If `loams` is not on PyPI yet, install the SDK from the monorepo instead:

```sh
git clone https://github.com/ostrium-labs/loams && pip install ./loams/sdks/python
```

## Run against a local engine

Start an engine (`cargo run -p loams -- dev` from the [monorepo](https://github.com/ostrium-labs/loams), or the compose stack from [docs/release/preview.md](https://github.com/ostrium-labs/loams/blob/main/docs/release/preview.md)), then:

```sh
export LOAMS_ENDPOINT=http://127.0.0.1:8080   # default in these examples: http://127.0.0.1:18080
export LOAMS_API_KEY=...                       # only if auth is on
python quickstart/quickstart.py
python sql/sql.py
```

Examples read and write only the namespace `examples-python` (override with `LOAMS_NAMESPACE`).

## A note on the SDK surface

SDK 0.1.0 generates the `instance`, `live` and `system` modules; collections, search and SQL are not in it yet. The examples use the SDK for connecting and instance/feature discovery and call the engine's native HTTP JSON API ([`quickstart/native.py`](quickstart/native.py), about 20 lines) for the rest. When the SDK grows those modules the helper goes away.

Docs: <https://loams.dev/docs>. License: Apache-2.0.
