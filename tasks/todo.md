# FELN RAG — build + encoder comparison

Source of truth: `feln_rag/data/NorthSea/{Layers.json,FELN.json}`.
Inspired by gait `FELNode`, with no gen-ai-toolkit dependency: SentenceTransformer encoder → numpy dot-product top-k →
few-shot user/assistant pairs → LLM → FELN. Score with `feln.FELNCompare`.

- [x] uv project on py3.13: sentence-transformers, numpy, litellm, feln (../feln), layers-json (../layers-json)
- [x] `index.py` — embed FELN.json texts, persist `data.json` + `data.npz` per encoder (gait FEL dir layout)
- [x] `rag.py` — encode query, top-k, build system prompt from Layers.json, few-shot pairs, LLM → FELN
- [x] `eval.py` — fixed holdout split; retrieval-only metrics (no LLM) across encoders; end-to-end structural/same
- [x] run retrieval comparison over cached ST models + ollama nomic
- [x] run end-to-end on holdout for best encoders + zero-shot baseline
- [x] report numbers
- [x] vectorless (VectorlessGAIT) retriever wired as `--encoders vectorless`, measured: parity, ~100× slower
- [x] review and simplify search; refresh cached metadata and serialize local model initialization
- [x] validate evaluation inputs and empty OKF catalogs; skip query retrieval for zero shots
- [x] preserve successful E2E results when individual requests fail, with explicit error rows
- [x] verify independence from gen-ai-toolkit while retaining feln and layers-json dependencies
- [x] document setup, cache behavior, evaluation output, and regression checks
