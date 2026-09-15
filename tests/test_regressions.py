from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
import sys
import time

import numpy as np
import pytest

from feln_rag.eval import main, split
from feln_rag.index import Encoder, Index, build_or_load
from feln_rag.rag import embedding_retriever, system_prompt_okf, vectorless_retriever


def test_cached_vectors_use_current_metadata(tmp_path, monkeypatch):
    old = [{"text": "same", "meta": {"layers": ["old"]}}]
    new = [{"text": "same", "meta": {"layers": ["new"]}}]
    monkeypatch.setattr(Encoder, "encode", lambda self, texts: np.ones((len(texts), 2)))
    build_or_load(old, Encoder("local:test"), tmp_path)
    monkeypatch.setattr(Encoder, "encode", lambda *args: pytest.fail("cache miss"))
    enc = Encoder("local:test")  # No model should be loaded for a cache hit.
    cached = build_or_load(new, enc, tmp_path)
    assert cached.examples == new
    np.testing.assert_array_equal(cached.embeddings, [[1, 1]])
    assert enc._st is None


def test_cache_separates_corpora_and_colliding_encoder_slugs(tmp_path, monkeypatch):
    calls = []
    def encode(self, texts):
        calls.append((self.name, texts))
        return np.ones((len(texts), 2))
    monkeypatch.setattr(Encoder, "encode", encode)
    for name, text in [("local:a/b", "a"), ("local:a_b", "a"), ("local:a/b", "b")] * 2:
        build_or_load([{"text": text, "meta": {}}], Encoder(name), tmp_path)
    assert len(calls) == 3


def test_interrupted_cache_is_rebuilt(tmp_path, monkeypatch):
    calls = []
    def encode(self, texts):
        calls.append(texts)
        return np.ones((len(texts), 2))
    monkeypatch.setattr(Encoder, "encode", encode)
    examples = [{"text": "a", "meta": {}}]
    enc = Encoder("local:test")
    build_or_load(examples, enc, tmp_path)
    next(tmp_path.rglob("data.npz")).write_bytes(b"truncated")
    np.testing.assert_array_equal(build_or_load(examples, enc, tmp_path).embeddings, [[1, 1]])
    assert len(calls) == 2


def test_batched_retrieval_and_zero_shot_setup():
    from feln_rag.eval import make_retriever
    calls = []
    def encode(texts):
        calls.append(texts)
        return np.array([[1, 0] if t == "a" else [0, 1] for t in texts])
    examples = [{"text": "a"}, {"text": "b"}]
    retrieve = embedding_retriever(Index(examples, np.eye(2)), SimpleNamespace(encode=encode), ["a", "b", "a"])
    assert retrieve("a", 1) == examples[:1]
    assert retrieve("b", 1) == examples[1:]
    assert calls == [["a", "b"]]
    for name in ("local:unused", "vectorless"):
        assert make_retriever(name, SimpleNamespace(top_k=0), [])("query", 0) == []


def test_search_matches_full_sort():
    rng = np.random.default_rng(0)
    vectors = rng.normal(size=(100, 8))
    query = rng.normal(size=8)
    index = Index([{}] * len(vectors), vectors)
    for k in (0, 1, 5, 100, 101):
        assert [i for _, i in index.search(query, k)] == np.argsort(-(vectors @ query))[:k].tolist()
    with pytest.raises(ValueError):
        index.search(query, -1)
    assert Index([], np.empty((0, 8))).search(query) == []


def test_model_loads_once_across_workers(monkeypatch):
    loads = []
    active = []

    class Model:
        def __init__(self, name):
            loads.append(name)
            time.sleep(0.02)

        def encode(self, texts, **kwargs):
            active.append(True)
            try:
                assert len(active) == 1
                time.sleep(0.01)
                return np.ones((len(texts), 2))
            finally:
                active.pop()

    monkeypatch.setitem(sys.modules, "sentence_transformers", SimpleNamespace(SentenceTransformer=Model))
    enc = Encoder("local:test")
    with ThreadPoolExecutor(8) as pool:
        assert len(list(pool.map(enc.encode, [["query"]] * 16))) == 16
    assert loads == ["test"]


def test_embedding_response_order(monkeypatch):
    import litellm

    monkeypatch.setattr(litellm, "embedding", lambda **kwargs: SimpleNamespace(data=[
        {"index": 1, "embedding": [0, 2]}, {"index": 0, "embedding": [3, 0]},
    ]))
    np.testing.assert_array_equal(Encoder("litellm:test").encode(["a", "b"]), np.eye(2))


def test_zero_shots_skips_embedding_and_vectorless_calls(monkeypatch):
    def fail(*args, **kwargs):
        pytest.fail("retrieval should not run with zero shots")

    monkeypatch.setitem(sys.modules, "vectorless_feln", SimpleNamespace(
        build_index=lambda *args: None,
        Retriever=lambda *args, **kwargs: SimpleNamespace(retrieve=fail),
    ))
    for retrieve in (
        embedding_retriever(Index([], np.empty((0, 2))), SimpleNamespace(encode=fail)),
        vectorless_retriever("unused", []),
    ):
        assert retrieve("query", 0) == []
        with pytest.raises(ValueError):
            retrieve("query", -1)


def test_invalid_evaluation_inputs_and_catalog(tmp_path):
    examples = [{"text": str(i)} for i in range(4)]
    for holdout in (-1, 0, 4, 5):
        with pytest.raises(ValueError):
            split(examples, holdout, 0)
    train, test = split(examples, 2, 0)
    assert split(examples, 2, 0) == (train, test)
    assert len(train) == len(test) == 2
    assert {e["text"] for e in train}.isdisjoint(e["text"] for e in test)
    for option in ("--limit", "--top-k"):
        with pytest.raises(SystemExit) as exc:
            main(["e2e", option, "-1"])
        assert exc.value.code == 2
    with pytest.raises(ValueError, match="no OKF"):
        system_prompt_okf(tmp_path)


def test_e2e_preserves_successes_when_a_request_fails(tmp_path, monkeypatch):
    import json
    from feln import FELN
    from feln_rag import eval as evaluation

    meta = {"layers": ["Wells"], "where": [""], "relations": []}
    examples = [{"text": text, "meta": meta} for text in ("success", "failure")]

    def generate(query, *args, **kwargs):
        if query == "failure":
            raise TimeoutError("request timed out")
        return FELN.model_validate(meta), json.dumps(meta), []

    monkeypatch.setattr(evaluation, "generate", generate)
    monkeypatch.setattr(evaluation, "system_prompt_okf", lambda path: "catalog")
    evaluation.e2e(SimpleNamespace(
        catalog="okf", okf=tmp_path, limit=0, out=tmp_path,
        encoders=["none"], model="unused", top_k=0,
    ), [], examples)
    rows = [json.loads(line) for line in (tmp_path / "e2e_okf_none.jsonl").read_text().splitlines()]
    assert rows[0]["same"] is True
    assert "error" not in rows[0]
    assert rows[1]["valid"] == 0
    assert rows[1]["error"] == "TimeoutError: request timed out"
