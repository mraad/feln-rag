"""Embed FELN.json examples and search them. Inspired by gait's FELTextMeta + VSSNumpy.

Implemented independently; gen-ai-toolkit is not a dependency.

Layout per encoder: ``<dir>/data.json`` (examples) and ``<dir>/data.npz`` (embeddings).
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from zipfile import BadZipFile

import numpy as np


def slug(name: str) -> str:
    """Filesystem-safe encoder name; shared by the index cache dir and eval output files."""
    return name.replace("/", "_").replace(":", "_")


def load_examples(path: str | os.PathLike) -> list[dict]:
    """FELN.json (list of {text, meta}) or the jsonl that ``feln generate -o`` writes."""
    path = Path(path).expanduser()
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    return json.loads(path.read_text(encoding="utf-8"))


class Encoder:
    """``local:<sentence-transformer>`` or ``litellm:<model>``. Unit-normalised vectors."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.provider, self.model = name.split(":", 1) if ":" in name else ("local", name)
        self._st = None
        self._encode_lock = Lock()

    def encode(self, texts: list[str]) -> np.ndarray:
        texts = [t.lower() for t in texts]  # gait EncoderLocal lowercases too
        if self.provider == "local":
            # Local inference shares model/device state; concurrent MPS calls can crash Python.
            with self._encode_lock:
                if self._st is None:
                    from sentence_transformers import SentenceTransformer

                    self._st = SentenceTransformer(self.model)
                return self._st.encode(texts, normalize_embeddings=True, convert_to_numpy=True, batch_size=64)
        if self.provider == "litellm":
            import litellm

            out = []
            for i in range(0, len(texts), 64):
                resp = litellm.embedding(model=self.model, input=texts[i : i + 64])
                out.extend(d["embedding"] for d in sorted(resp.data, key=lambda d: d["index"]))
            arr = np.asarray(out, dtype=np.float32)
            return arr / np.maximum(np.linalg.norm(arr, axis=1, keepdims=True), 1e-9)
        raise ValueError(f"unknown encoder provider {self.provider!r}")


@dataclass
class Index:
    examples: list[dict]
    embeddings: np.ndarray  # (n, dim), unit-normalised

    @classmethod
    def build(cls, examples: list[dict], enc: Encoder) -> Index:
        return cls(examples, enc.encode([e["text"] for e in examples]))

    def dump(self, folder: str | os.PathLike) -> None:
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "data.json").write_text(json.dumps(self.examples, ensure_ascii=False, indent=2), encoding="utf-8")
        np.savez_compressed(folder / "data.npz", embeddings=self.embeddings)

    @classmethod
    def load(cls, folder: str | os.PathLike) -> Index:
        folder = Path(folder)
        with np.load(folder / "data.npz") as data:
            emb = data["embeddings"]
        return cls(json.loads((folder / "data.json").read_text(encoding="utf-8")), emb)

    def search(self, query: np.ndarray, top_k: int = 5) -> list[tuple[float, int]]:
        """Dot-product top-k for one query vector: ``[(score, corpus_id), ...]`` best first."""
        if top_k < 0:
            raise ValueError("top_k must be nonnegative")
        if top_k == 0 or not self.examples:
            return []
        scores = self.embeddings @ query.reshape(-1)
        k = min(top_k, len(scores))
        ids = np.argpartition(-scores, k - 1)[:k]
        ids = ids[np.argsort(-scores[ids])]
        return [(float(scores[i]), int(i)) for i in ids]


def build_or_load(examples: list[dict], enc: Encoder, cache_dir: str | os.PathLike) -> Index:
    texts = [e["text"] for e in examples]
    fingerprint = hashlib.sha256(json.dumps([enc.name, texts], ensure_ascii=False).encode()).hexdigest()
    folder = Path(cache_dir) / slug(enc.name) / fingerprint
    if (folder / "data.npz").exists() and (folder / "data.json").exists():
        try:
            idx = Index.load(folder)
        except (OSError, ValueError, KeyError, EOFError, BadZipFile):
            pass  # An interrupted cache write must not prevent rebuilding derived data.
        else:
            if idx.embeddings.ndim == 2 and len(idx.embeddings) == len(examples) and [e["text"] for e in idx.examples] == texts:
                idx.examples = examples  # Reuse vectors, but always use the current metadata.
                return idx
    idx = Index.build(examples, enc)
    idx.dump(folder)
    return idx
