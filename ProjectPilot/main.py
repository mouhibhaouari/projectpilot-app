import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
from src.project_analyzer.core import ProjectAnalyzer
from src.ai_integration.core import general_install_guide , docker_compose_install, fix_setup_error,readme_install_guide
from src.mcp.core import MCPClient

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AnalyzeRequest(BaseModel):
    path: str

@app.post("/analyze")
def analyze_project(request: AnalyzeRequest):
    analyzer = ProjectAnalyzer()

    try:
        info = analyzer.analyze(request.path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Path does not exist")
    except NotADirectoryError:
        raise HTTPException(status_code=400, detail="Path is not a directory")
    project_json = info.to_dict()
    mcp = MCPClient(request.path)
    mcp.init()
    try:
        if info.has_docker and info.docker_path:
            install_result = docker_compose_install(info,mcp)

            return {
            "project": project_json,
            "install": {
                "source": "docker",
                "result": install_result,
            },
        }
        if info.has_readme:
            install_result = general_install_guide(info, mcp)

            return {
                "project": project_json,
                "install": {
                    "source": "readme",
                    "result": install_result,
                },
            }
        install_result = readme_install_guide(info, mcp)

        return {
            "project": project_json,
            "install": {
                "source": "general",
                "result": install_result,
            },
        }

    finally:
        if mcp.process:
            mcp.process.terminate()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("\n" + "="*80)
    print("[WebSocket] Connection established")
    print("="*80)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(f"\n[WebSocket] Received message: {message}")            
            if message.get("type") == "error":
                command = message.get("command", "unknown")
                exit_code = message.get("exitCode", 1)
                project_path = message.get("projectPath", "")
                error_output = message.get("errorOutput", "")
                
                print(f"[WebSocket] Processing error:")
                print(f"  - Command: {command}")
                print(f"  - Exit Code: {exit_code}")
                print(f"  - Project Path: {project_path}")
                print(f"  - Error Output (first 200 chars): {error_output[:200] if error_output else 'None'}")                
                print(f"[WebSocket] Calling fix_setup_error()...")
                result = fix_setup_error(
                    failed_command=command,
                    exit_code=exit_code,
                    error_message=error_output,
                    project_path=project_path
                )
                
                print(f"[WebSocket] fix_setup_error() returned: {result}")
                response = {
                            "type": "fix",
                            "result": {
                                "success": result.get("success", False),
                                "suggestion": result.get("suggestion", ""),
                                "alternative_commands": result.get("alternative_commands", []),
                                "next_steps": result.get("next_steps", ""),
                                "error": result.get("error"),
                                "raw": result.get("raw")
                            }
                        }
                print(f"[WebSocket] Sending fix response:\n{json.dumps(response, indent=2)}")
                await websocket.send_text(json.dumps(response))
                print("[WebSocket] Response sent successfully")
                
    except Exception as e:
        print(f"\n[WebSocket ERROR] Exception: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"[WebSocket ERROR] Traceback:\n{traceback.format_exc()}")
        try:
            error_response = {
                    "type": "fix",
                    "result": {
                        "success": False,
                        "suggestion": f"Error processing request: {str(e)}",
                        "alternative_commands": [],
                        "next_steps": "Please try again or check the connection",
                        "error": str(e),
                        "raw": None
                    }
                }
            await websocket.send_text(json.dumps(error_response))
        except:
            pass
    finally:
        print("WebSocket connection closed")
