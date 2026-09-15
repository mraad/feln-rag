import numpy as np

from feln_rag.index import Index
from feln_rag.rag import messages


def test_search_and_roundtrip(tmp_path):
    ex = [{"text": "a", "meta": {}}, {"text": "b", "meta": {}}, {"text": "c", "meta": {}}]
    emb = np.eye(3, dtype=np.float32)
    idx = Index(ex, emb)
    idx.dump(tmp_path)
    idx = Index.load(tmp_path)
    hits = idx.search(np.array([0.1, 0.9, 0.0], dtype=np.float32), top_k=2)
    assert [i for _, i in hits] == [1, 0]
    assert hits[0][0] > hits[1][0]


def test_messages_pairing():
    shots = [{"text": "q1", "meta": {"layers": ["A"], "where": [""], "relations": []}}]
    msgs = messages("sys", "q2", shots)
    assert [m["role"] for m in msgs] == ["system", "user", "assistant", "user"]
    assert msgs[-1]["content"] == "q2"
