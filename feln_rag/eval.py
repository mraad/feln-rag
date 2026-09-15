"""Compare retrievers for FELN RAG.

    python -m feln_rag.eval retrieval [--encoders a b ...] [--top-k 5]
    python -m feln_rag.eval e2e --encoders local:BAAI/bge-base-en-v1.5 none [--limit 50]

Fixed holdout split (seed) so every retriever sees the same queries and the same corpus.
``retrieval`` needs no extractor LLM: it scores how close the retrieved metas are to the gold meta.
``e2e`` runs the LLM and scores the generated FELN with ``feln.FELNCompare``.
"""

from __future__ import annotations

import argparse
import os
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dotenv import load_dotenv
from feln import FELN, FELNCompare
from feln.generate import records_to_jsonl
from layers_json.layers import Layers

from .index import Encoder, build_or_load, load_examples, slug
from .rag import Retriever, embedding_retriever, generate, system_prompt, system_prompt_okf, vectorless_retriever

NORTHSEA = Path(__file__).with_name("data") / "NorthSea"
DEFAULT_ENCODERS = [
    "local:multi-qa-mpnet-base-dot-v1",  # gait EMB_MODEL_NAME default
    "local:multi-qa-mpnet-base-cos-v1",
    "local:all-mpnet-base-v2",
    "local:all-MiniLM-L6-v2",
    "local:multi-qa-MiniLM-L6-dot-v1",
    "local:BAAI/bge-small-en-v1.5",
    "local:BAAI/bge-base-en-v1.5",
    "local:BAAI/bge-large-en-v1.5",
    "litellm:ollama/nomic-embed-text",
]
WORKERS = 8  # concurrent extractor calls per retriever; litellm is thread-safe


def split(examples: list[dict], holdout: int, seed: int) -> tuple[list[dict], list[dict]]:
    if not 0 < holdout < len(examples):
        raise ValueError("holdout must leave at least one training and one test example")
    order = list(range(len(examples)))
    random.Random(seed).shuffle(order)
    test = [examples[i] for i in order[:holdout]]
    train = [examples[i] for i in order[holdout:]]
    return train, test


def make_retriever(
    name: str, args: argparse.Namespace, train: list[dict], queries: list[str] | None = None,
) -> Retriever:
    """'none' = zero-shot; 'vectorless' = VectorlessGAIT LLM retriever; else an embedding encoder."""
    if name == "none" or args.top_k == 0:
        return lambda query, k: []
    if name == "vectorless":
        return vectorless_retriever(str(args.layers), train, model=args.model)
    enc = Encoder(name)
    return embedding_retriever(build_or_load(train, enc, args.cache), enc, queries)


def _mean(rows: list[dict], key: str) -> float:
    return statistics.mean(r[key] for r in rows)


def retrieval(args: argparse.Namespace, train: list[dict], test: list[dict]) -> None:
    gold = [FELN.model_validate(t["meta"]) for t in test]
    print(f"{'encoder':40s} {'best@k':>7s} {'partial@k':>9s} {'top1':>6s} {'layers@k':>8s} {'prim@1':>6s} {'sec':>6s}")
    for name in args.encoders:
        t0 = time.perf_counter()
        retriever = make_retriever(name, args, train, [t["text"] for t in test])
        rows = []
        for g, t in zip(gold, test):
            cands = [FELN.model_validate(s["meta"]) for s in retriever(t["text"], args.top_k)]
            scores = [FELNCompare.structural(g, c) for c in cands]
            layers = sorted(x.lower() for x in g.layers)
            rows.append(
                {
                    "best": max(scores, default=0.0),
                    "partial": max((FELNCompare.partial(g, c) for c in cands), default=0.0),
                    "top1": scores[0] if scores else 0.0,
                    "layers": float(any(sorted(x.lower() for x in c.layers) == layers for c in cands)),
                    "prim": float(bool(cands) and cands[0].layers[0].lower() == g.layers[0].lower()),
                }
            )
        print(
            f"{name:40s} {_mean(rows, 'best'):7.3f} {_mean(rows, 'partial'):9.3f} {_mean(rows, 'top1'):6.3f} "
            f"{_mean(rows, 'layers'):8.3f} {_mean(rows, 'prim'):6.3f} {time.perf_counter() - t0:5.0f}s"
        )


def e2e(args: argparse.Namespace, train: list[dict], test: list[dict]) -> None:
    system = system_prompt_okf(args.okf) if args.catalog == "okf" else system_prompt(Layers.load(str(args.layers)))
    test = test[: args.limit or None]
    gold = [FELN.model_validate(t["meta"]) for t in test]
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"{'encoder':40s} {'valid':>6s} {'same':>6s} {'struct':>7s} {'partial':>8s}")
    for name in args.encoders:
        retriever = make_retriever(name, args, train)

        def run(t: dict) -> tuple[FELN | None, str, list[dict]] | Exception:
            try:
                return generate(t["text"], system, retriever, model=args.model, top_k=args.top_k)
            except Exception as exc:
                return exc  # Preserve other paid results when one request fails.

        with ThreadPoolExecutor(WORKERS) as pool:
            results = list(pool.map(run, test))
        rows = []
        for t, g, result in zip(test, gold, results):
            pred, raw, shots = (None, "", []) if isinstance(result, Exception) else result
            rows.append(
                {
                    "text": t["text"],
                    "gold": t["meta"],
                    "pred": pred.model_dump() if pred else raw,
                    "valid": float(pred is not None),
                    "same": bool(pred and g.same(pred)),
                    "structural": FELNCompare.structural(g, pred) if pred else 0.0,
                    "partial": FELNCompare.partial(g, pred) if pred else 0.0,
                    "shots": [x["text"] for x in shots],
                }
            )
            if isinstance(result, Exception):
                rows[-1]["error"] = f"{type(result).__name__}: {result}"
        (out_dir / f"e2e_{args.catalog}_{slug(name)}.jsonl").write_text(records_to_jsonl(rows), encoding="utf-8")
        print(
            f"{name:40s} {_mean(rows, 'valid'):6.3f} {_mean(rows, 'same'):6.3f} "
            f"{_mean(rows, 'structural'):7.3f} {_mean(rows, 'partial'):8.3f}   "
            f"(n={len(rows)}, errors={sum('error' in row for row in rows)})"
        )


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["retrieval", "e2e"])
    ap.add_argument("--feln", type=Path, default=NORTHSEA / "FELN.json")
    ap.add_argument("--layers", type=Path, default=NORTHSEA / "Layers.json")
    ap.add_argument("--okf", type=Path, default=NORTHSEA / "okf", help="OKF bundle dir (e2e --catalog okf)")
    ap.add_argument("--catalog", choices=["layers", "okf"], default="layers", help="e2e: catalog rendered in the system prompt")
    ap.add_argument(
        "--encoders",
        nargs="+",
        default=DEFAULT_ENCODERS,
        help="encoder names, 'vectorless' (VectorlessGAIT), or 'none' = zero-shot (e2e only)",
    )
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--holdout", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0, help="e2e: cap holdout queries")
    ap.add_argument("--model", default=os.environ.get("LLM_MODEL_NAME"))
    ap.add_argument("--cache", type=Path, default=Path("indices"))
    ap.add_argument("--out", type=Path, default=Path("out"))
    args = ap.parse_args(argv)
    if args.top_k < 0 or args.limit < 0:
        ap.error("--top-k and --limit must be nonnegative (0 means no shots / no limit)")
    try:
        train, test = split(load_examples(args.feln), args.holdout, args.seed)
    except ValueError as exc:
        ap.error(str(exc))
    print(f"corpus={len(train)} holdout={len(test)} top_k={args.top_k}")
    (retrieval if args.mode == "retrieval" else e2e)(args, train, test)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
