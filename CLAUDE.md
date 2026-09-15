# Development notes

This repository contains FELN RAG and the FELN Studio SPA. See `README.md` for setup and usage.

## Data and privacy

- Keep only NorthSea examples, catalogs, screenshots, and measurements.
- Default data lives in `feln_rag/data/NorthSea`; do not introduce personal filesystem paths.
- Bundled layer connection URIs are removed. OKF source references use relative NorthSea names.
- Never commit credentials, local configuration, generated request payloads, or embedding caches.
- Dependencies use relative sibling paths. The generated lockfile is ignored because sibling
  metadata can contain personal repository URLs.
- Check Git history as well as working files before publishing; deleting a file does not erase
  its contents or author metadata from prior commits.

## Commands

```bash
uv sync
uv run --no-sync pytest -q
uv run --no-sync pyright feln_rag
uv run --no-sync python -m feln_rag.web
uv run --no-sync python -m feln_rag.eval retrieval --encoders local:all-MiniLM-L6-v2
uv run --no-sync python -m feln_rag.eval e2e --encoders none --holdout 10 --limit 3
```

Use `--no-sync` for the installed environment. E2E spends provider tokens; always pass a small
`--limit` when iterating. The CLI loads `.env`; library callers manage their environment.

## Implementation

- `index.py`: lowercased, normalized embeddings; NumPy top-k search; corpus/encoder cache
  fingerprints; current metadata on cache hits; recovery from unreadable vector caches.
  Model loading and local inference share a lock to prevent native device crashes.
- `rag.py`: prompt rendering, worked-example message pairs, embedding and vectorless retrieval,
  and FELN generation. The query is always the final message. Requests have a 120-second timeout.
- `eval.py`: deterministic holdout splits, batched retrieval evaluation, concurrent generation,
  and explicit error rows. Zero shots skips retriever setup.
- `web.py`: loopback-only HTTP server, strict request validation, generic provider errors, and
  static assets. Generation preserves the five displayed example IDs in order.
- `static/`: vanilla JavaScript, semantic HTML, and CSS. Use text nodes for model/catalog content.
  Preserve keyboard access, loading states, query invalidation, and the editable prompt.

Use `feln.FELNCompare` and `FELN.same` for scoring; do not duplicate their SQL normalization.
Dependencies on `feln`, `layers-json`, and optional vectorless retrieval are intentional.
Do not add a `gen-ai-toolkit` dependency. Keep the SPA free of frontend build dependencies.

Tests use synthetic vectors and mocked providers. The HTTP test binds a loopback socket.
Historical quality measurements require live evaluation; unit tests do not reproduce them.
