from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

from agent_runtime import AgentRuntime, RulePlanner, Task, Tool, ToolRegistry


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

registry = ToolRegistry(
    [
        Tool(
            "uppercase",
            "Convert text to uppercase",
            lambda data: data["text"].upper(),
        ),
        Tool(
            "word_count",
            "Count whitespace-separated words",
            lambda data: len(data["text"].split()),
        ),
    ]
)


def run_agent(tool_name: str, text: str):
    planner = RulePlanner(tool_name)

    def executor(action, _state):
        return registry.execute(action.name, action.input)

    return AgentRuntime(planner, executor).run(Task(text))


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type="application/json"):
        raw = body if isinstance(body, bytes) else body.encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/":
            self._send(200, (WEB / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        if self.path == "/app.js":
            self._send(200, (WEB / "app.js").read_bytes(), "text/javascript; charset=utf-8")
            return
        self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/run":
            self._send(404, json.dumps({"error": "not found"}))
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        tool = payload.get("tool", "uppercase")
        text = payload.get("text", "")
        if tool not in {"uppercase", "word_count"}:
            self._send(400, json.dumps({"error": "unknown tool"}))
            return

        state = run_agent(tool, text)
        self._send(
            200,
            json.dumps(
                {
                    "status": state.status.value,
                    "result": state.result,
                    "variables": state.variables,
                    "step": state.step,
                    "history": state.history,
                    "checkpoints": [
                        {
                            "step": cp.step,
                            "status": cp.status,
                            "action_index": cp.action_index,
                            "variables": cp.variables,
                        }
                        for cp in state.checkpoints
                    ],
                }
            ),
        )


if __name__ == "__main__":
    print("Agent Runtime UI: http://127.0.0.1:8000")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
