import subprocess
import json

class MCPClient:
    def __init__(self, project_path: str):
        self.project_path = project_path

        self.process = subprocess.Popen(
            [
                "npx",
                "-y",
                "@modelcontextprotocol/server-filesystem",
                project_path
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def send(self, payload: dict):
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()
    def receive(self):
        while True:
            line = self.process.stdout.readline()
            if line.strip():
                return json.loads(line)
    def call_tool(self, name: str, arguments: dict):
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        self.send(request)
        return self.receive()

    def read_file(self, path: str) -> str:
        result = self.call_tool("read_file", {"path": path})
        return self._extract_text(result)

    def list_directory(self, path: str) -> list:
        result = self.call_tool("list_directory", {"path": path})
        return self._extract_text(result)

    def batch_read(self, paths: list) -> dict:
        return {
            p: self.read_file(p) for p in paths
        }

    def _extract_text(self, tool_result):
        content = tool_result.get("result", {}).get("content", [])
        if content:
            return content[0].get("text", "")
        return ""