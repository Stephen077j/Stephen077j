import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from classifier import predict
from predict import load_model


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/predict":
            self.send_json(404, {"error": "not found"})
            return
        if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
            self.send_json(415, {"error": "expected JSON"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 8192:
                self.send_json(413, {"error": "invalid payload size"})
                return
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict) or not isinstance(data.get("text"), str) or len(data["text"]) > 2000:
                raise ValueError("text must be a string of at most 2000 characters")
            self.send_json(200, predict(load_model(), data["text"]))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self.send_json(422, {"error": str(exc)})
        except FileNotFoundError:
            self.send_json(503, {"error": "run python train.py first"})

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Local demo API listening on http://127.0.0.1:8765")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
