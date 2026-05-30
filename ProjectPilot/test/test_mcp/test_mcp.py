from mcp.core import MCPClient
path="/home/usr/spring-boot-kafka"
def test_list_directory():
    mcp = MCPClient(path)

    print("MCP started")
    
    result = mcp.call_tool("list_directory", {"path": path})

    print("RESULT:", result)

    assert result is not None

    mcp.process.terminate()
def list_tools():
    mcp = MCPClient(path)
    print(mcp.call_tool("list_tools", {}))