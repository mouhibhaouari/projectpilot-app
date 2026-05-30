from project_analyzer.core import ProjectAnalyzer
from ai_integration.core import generate_install_guide,docker_compose_install
def test_generate_install_guide():
    project_path = "/home/usr/docker-compose/full-stack-fastapi-template"
    analyzer = ProjectAnalyzer()
    result = analyzer.analyze(project_path)
    print("\n=== PROJECT INFO ===")
    print(result)
    if result.has_docker and result.docker_path:
        guide = docker_compose_install(result)
        print("\n=== DOCKER OUTPUT ===")
        print(guide)
        return
    if result.has_readme:
        guide = generate_install_guide(result)
        print("\n=== README AI GUIDE ===")
        print(guide)
        return
    print("\n=== NO INSTALL METHOD FOUND ===")