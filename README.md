# Loams Python examples

These examples target the released **Loams SDK 0.1.2**.

[Loams](https://loams.dev) is an open-source data engine that keeps your data in your own bucket and serves hybrid search (vector, BM25 and filters) and SQL over it. This repo holds example apps for the [Python SDK](https://github.com/ostrium-labs/loams/tree/main/sdks/python) (`loams` 0.1.2).

| Example | What it shows |
|---|---|
| [quickstart](quickstart) | connect, create a collection, upsert documents, hybrid search |
| [sql](sql) | SQL over the collection, including `rrf(vector_search(...), text_search(...))` |
| [fastapi-search](fastapi-search) | a FastAPI `/search` endpoint using the collection handle |
| [platform](platform) | opt-in, read-only auth/admin/Live admin module calls |

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
LOAMS_PLATFORM_EXAMPLE=1 python platform/platform.py   # authorized credential required
```

Examples read and write only the namespace `examples-python` (override with `LOAMS_NAMESPACE`).

## SDK module coverage

The quickstart and app examples use the published 0.1.2 SDK for namespace and collection setup, documents, hybrid/vector search, SQL records, streams, instance discovery, system feature detection and optional Graph. The generated `auth`, `admin.*` and `live.admin` modules are available through `loams.modules[...]` in Python 0.1.2; the opt-in platform example uses read-only calls and needs an authorized credential. House has no Python SDK module in 0.1.2. The existing TypeScript Live-tail example illustrates the `live` session and `tables` modules.

Docs: <https://loams.dev/docs>. License: Apache-2.0.
