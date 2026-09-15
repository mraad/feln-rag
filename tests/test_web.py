import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from threading import Thread
from types import SimpleNamespace

from feln import FELN
from feln_rag import web


def test_local_api_and_exact_examples(monkeypatch):
    examples = [{"text": f"query {i}", "meta": {"layers": ["Wells"], "where": [""], "relations": []}}
                for i in range(7)]
    app = object.__new__(web.Playground)
    app.index = SimpleNamespace(examples=examples)
    app.prompt = "public catalog"
    app.model = "test-model"
    app.encoder = SimpleNamespace(name="local:test")
    captured = []

    def generate(query, prompt, retriever, **kwargs):
        shots = retriever(query, 5)
        captured.append((query, prompt, shots))
        if query == "fail":
            raise RuntimeError("secret-provider-detail")
        return FELN.model_validate(shots[0]["meta"]), "{}", shots

    monkeypatch.setattr(web, "generate", generate)
    monkeypatch.setattr(app, "retrieve", lambda query: {"examples": [
        {"id": i, "score": 1 - i / 10, **examples[i]} for i in range(5)]})
    with ThreadingHTTPServer(("127.0.0.1", 0), web.handler_for(app)) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()

        def request(path, data=None, headers=None):
            conn = HTTPConnection("127.0.0.1", server.server_port)
            conn.request("GET" if data is None else "POST", path,
                         None if data is None else json.dumps(data),
                         {"Content-Type": "application/json", **(headers or {})})
            response = conn.getresponse()
            body = response.read().decode()
            conn.close()
            return response.status, body

        try:
            assert "FELN Studio" in request("/")[1]
            assert request("/../.env")[0] == 404
            assert request("/api/config", headers={"Host": "attacker.example"})[0] == 403
            assert json.loads(request("/api/config")[1])["prompt"] == app.prompt
            assert len(json.loads(request("/api/retrieve", {"query": "wells"})[1])["examples"]) == 5
            payload = {"query": "wells", "prompt": "custom public prompt", "ids": [4, 2, 0, 3, 1]}
            code, body = request("/api/generate", payload)
            assert code == 200 and json.loads(body)["valid"]
            assert captured[-1] == ("wells", "custom public prompt", [examples[i] for i in payload["ids"]])
            for bad_ids in ([0] * 5, [-1, 0, 1, 2, 3], [True, 1, 2, 3, 4], [0, 1, 2, 3, 99]):
                assert request("/api/generate", {**payload, "ids": bad_ids})[0] == 400
            assert request("/api/generate", payload, {"Origin": "https://attacker.example"})[0] == 403
            assert request("/api/retrieve", {"query": "   "})[0] == 400
            assert request("/api/retrieve", ["bad shape"])[0] == 400
            assert request("/api/generate", {**payload, "prompt": ""})[0] == 400
            code, body = request("/api/generate", {**payload, "query": "fail"})
            assert code == 502 and "secret-provider-detail" not in body
            assert len(captured) == 2
        finally:
            server.shutdown()
            thread.join()
