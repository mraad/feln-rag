"""Few-shot FELN generation: retrieve nearest examples, pair them as user/assistant turns, ask the LLM."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable

import litellm
from feln import FELN
from layers_json.layers import Layer, Layers

from .index import Encoder, Index

Retriever = Callable[[str, int], list[dict]]  # (query, k) -> [{text, meta}, ...]

litellm.drop_params = True  # models without reasoning_effort ignore it

INSTRUCTIONS = """You are a geospatial query translator. Convert the user's natural-language request into a FELN JSON object:

{"layers": [...], "where": [...], "relations": [...]}

- `layers[0]` is the primary layer (features returned); `layers[1..]` are spatial filter layers. Use catalog layer names exactly.
- `where` has one SQL WHERE fragment per layer, same order; "" when no filter. Use DuckDB syntax with double-quoted lower-case column names and bare literals, exactly like the examples.
- `relations` has one entry per secondary layer: intersects, within, contains, "withinDistance <n> <unit>", "notWithinDistance <n> <unit>", or "" (no spatial join). Units: meters, kilometers, feet, miles.
- Every string literal must come from the column's listed values or coded keys. A layer noun like "oil wells" or "gas pipelines" is the layer's subtype column (see `subtype`) compared to the label's code, not a free-text column.
- Earlier user/assistant turns are worked examples only. Translate the LAST user message; never repeat an example's answer.
- Output only the JSON object.

# Layers
"""


def _layer_text(layer: Layer) -> str:
    lines = [f"## {layer.name} (alias: {layer.alias}, geometry: {layer.stype}, subtype column: {layer.subtype})"]
    lines += [f"- {h}" for h in layer.hints]
    lines.append("Columns:")
    for c in layer.columns:
        bits = [f"- {c.name} ({c.dtype})"]
        if c.alias and c.alias != c.name:
            bits.append(f"alias: {c.alias}")
        if c.keyval:
            bits.append("keyval: " + json.dumps(c.keyval, ensure_ascii=False))
        elif c.values:
            bits.append("values: " + json.dumps(c.values, ensure_ascii=False))
        lines.append(" | ".join(bits))
        lines += [f"    hint: {h}" for h in c.hints]
    return "\n".join(lines)


def system_prompt(layers: Layers) -> str:
    return INSTRUCTIONS + "\n\n".join(_layer_text(layer) for layer in layers)


def system_prompt_okf(bundle: str | os.PathLike) -> str:
    """Same instructions, but the catalog is the OKF bundle's concept docs verbatim (frontmatter included)."""
    docs = sorted(p for p in Path(bundle).expanduser().glob("*.md") if p.name != "index.md")
    if not docs:
        raise ValueError(f"no OKF concept documents found in {bundle}")
    return INSTRUCTIONS + "\n\n".join(p.read_text(encoding="utf-8") for p in docs)


def _parse(text: str) -> FELN | None:
    try:
        return FELN.model_validate(json.loads(text))
    except (ValueError, TypeError):
        return None


def messages(system: str, query: str, shots: list[dict]) -> list[dict]:
    msgs = [{"role": "system", "content": system}]
    for ex in shots:
        msgs.append({"role": "user", "content": ex["text"]})
        msgs.append({"role": "assistant", "content": json.dumps(ex["meta"], ensure_ascii=False)})
    msgs.append({"role": "user", "content": query})
    return msgs


def embedding_retriever(index: Index, enc: Encoder, queries: list[str] | None = None) -> Retriever:
    # Evaluation can embed the holdout in batches instead of one model call per query.
    unique = list(dict.fromkeys(queries or []))
    vectors = dict(zip(unique, enc.encode(unique))) if unique else {}

    def retrieve(query: str, k: int) -> list[dict]:
        if k < 0:
            raise ValueError("k must be nonnegative")
        if k == 0:
            return []
        vector = vectors[query] if query in vectors else enc.encode([query])[0]
        return [index.examples[i] for _, i in index.search(vector, top_k=k)]

    return retrieve


def vectorless_retriever(layers_path: str, examples: list[dict], model: str | None = None) -> Retriever:
    """VectorlessGAIT: LLM routes layers, then LLM picks example ids. Two calls per query."""
    import tempfile

    from vectorless_feln import Retriever as VLRetriever, build_index

    # build_index only takes paths, so round-trip the in-memory split through a temp file.
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as f:
        json.dump(examples, f, ensure_ascii=False)
        f.flush()
        vl = VLRetriever(build_index(layers_path, f.name), model=model)

    def retrieve(query: str, k: int) -> list[dict]:
        if k < 0:
            raise ValueError("k must be nonnegative")
        if k == 0:
            return []
        return [{"text": ex.text, "meta": ex.meta.raw} for ex in vl.retrieve(query, k=k).selected]

    return retrieve


def generate(
    query: str,
    system: str,
    retriever: Retriever,
    model: str | None = None,
    top_k: int = 5,
) -> tuple[FELN | None, str, list[dict]]:
    """Returns (parsed FELN or None, raw completion, retrieved examples)."""
    shots = retriever(query, top_k)
    resp = litellm.completion(
        model=model or os.environ["LLM_MODEL_NAME"],
        messages=messages(system, query, shots),
        temperature=0.0,
        reasoning_effort="none",  # gpt-5.x: temperature=0 only allowed with reasoning off
        response_format={"type": "json_object"},
        timeout=120,
    )
    raw = resp.choices[0].message.content or ""  # type: ignore[union-attr]
    return _parse(raw), raw, shots
