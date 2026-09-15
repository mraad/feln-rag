"""Local vanilla-JS playground. Run with ``python -m feln_rag.web``."""

from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import cast

from dotenv import load_dotenv
from layers_json.layers import Layers

from .eval import NORTHSEA
from .index import Encoder, build_or_load, load_examples
from .rag import generate, system_prompt

STATIC = Path(__file__).with_name("static")


class Playground:
    def __init__(self, args: argparse.Namespace):
        self.prompt = system_prompt(Layers.load(str(args.layers.expanduser())))
        self.model = args.model
        self.encoder = Encoder(args.encoder)
        self.index = build_or_load(load_examples(args.feln), self.encoder, args.cache)
        if len(self.index.examples) < 5:
            raise ValueError("The playground needs at least five examples")

    def config(self) -> dict:
        return {"prompt": self.prompt, "model": self.model, "encoder": self.encoder.name,
                "count": len(self.index.examples)}

    def retrieve(self, query: str) -> dict:
        hits = self.index.search(self.encoder.encode([query])[0], 5)
        return {"examples": [{"id": i, "score": score, **self.index.examples[i]} for score, i in hits]}

    def complete(self, query: str, prompt: str, ids: list) -> dict:
        shots = [self.index.examples[i] for i in ids]
        pred, raw, _ = generate(query, prompt, lambda query, k: shots, model=self.model)
        return {"valid": pred is not None, "feln": pred.model_dump() if pred is not None else None, "raw": raw}


def handler_for(app: Playground):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Prompts, model output, and credentials never go into access logs.

        def send(self, status: int, content: bytes, mime: str):
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(content)

        def json(self, status: int, payload: dict):
            self.send(status, json.dumps(payload).encode(), "application/json; charset=utf-8")

        def local_request(self) -> bool:
            port = cast(ThreadingHTTPServer, self.server).server_port
            hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
            return (self.headers.get("Host") in hosts and
                    self.headers.get("Origin") in {None, *(f"http://{host}" for host in hosts)})

        def do_GET(self):
            if not self.local_request():
                return self.json(403, {"error": "Local requests only"})
            if self.path == "/api/config":
                return self.json(200, app.config())
            files = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
                     "/style.css": ("style.css", "text/css")}
            if self.path not in files:
                return self.json(404, {"error": "Not found"})
            name, mime = files[self.path]
            self.send(200, (STATIC / name).read_bytes(), mime + "; charset=utf-8")

        def do_POST(self):
            if not self.local_request():
                return self.json(403, {"error": "Local requests only"})
            if self.path not in {"/api/retrieve", "/api/generate"}:
                return self.json(404, {"error": "Not found"})
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                return self.json(415, {"error": "Expected application/json"})
            try:
                prompt, ids = "", []
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 200_000:
                    return self.json(413, {"error": "Request must be between 1 and 200,000 bytes"})
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError("Expected a JSON object")
                query = data.get("query")
                if not isinstance(query, str) or not query.strip() or len(query) > 10_000:
                    raise ValueError("Enter a query of 1–10,000 characters")
                if self.path == "/api/generate":
                    prompt, ids = data.get("prompt"), data.get("ids")
                    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 100_000:
                        raise ValueError("Enter a system prompt of 1–100,000 characters")
                    if not isinstance(ids, list):
                        raise ValueError("Retrieve five examples first")
                    # Validate IDs before calling the provider; provider errors stay private.
                    if len(ids) != 5 or any(type(i) is not int or not 0 <= i < len(app.index.examples) for i in ids) or len(set(ids)) != 5:
                        raise ValueError("Select five distinct example IDs from the corpus")
            except (ValueError, UnicodeDecodeError) as exc:
                return self.json(400, {"error": str(exc) if not isinstance(exc, json.JSONDecodeError) else "Invalid JSON"})
            try:
                result = app.retrieve(query) if self.path == "/api/retrieve" else app.complete(query, prompt, ids)
            except Exception:
                return self.json(502, {"error": "The model request failed. Check server model configuration and try again."})
            self.json(200, result)

    return Handler


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--feln", type=Path, default=NORTHSEA / "FELN.json")
    parser.add_argument("--layers", type=Path, default=NORTHSEA / "Layers.json")
    parser.add_argument("--cache", type=Path, default=Path("indices/playground"))
    parser.add_argument("--encoder", default="local:multi-qa-mpnet-base-dot-v1")
    parser.add_argument("--model", default=os.environ.get("LLM_MODEL_NAME"))
    args = parser.parse_args()
    if not args.model:
        parser.error("Set LLM_MODEL_NAME or pass --model")
    app = Playground(args)
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(app)) as server:
        print(f"FELN Studio → http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
