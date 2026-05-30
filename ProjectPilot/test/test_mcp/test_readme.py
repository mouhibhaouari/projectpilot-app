from project_analyzer.core import ProjectAnalyzer
from mcp.core import MCPClient
from ai_integration.core import general_install_guide , dockerfile_install_agent
def test_readme_agent():
    path = "/home/usr/AI-project-Runner"

    analyzer = ProjectAnalyzer()

    info = analyzer.analyze(path)

    mcp = MCPClient(path)

    mcp.init()

    result = general_install_guide(info, mcp)

    print("\nFINAL RESULT:\n")
    print(result)

    assert result is not None

    mcp.process.terminate()