# models.py
from dataclasses import dataclass, field
from enum import Enum
from typing import List
class ProjectType(Enum):
    UNKNOWN = "unknown"
    PYTHON = "python"
    NODEJS = "nodejs"
    JAVA_MAVEN = "java-maven"
    JAVA_GRADLE = "java-gradle"
    PHP = "php"
    RUBY = "ruby"
    GO = "go"
    CSHARP = "csharp"

    def __str__(self):
        return self.value
@dataclass
class ProjectInfo:
    path: str = ""
    name: str = ""
    project_type: ProjectType = ProjectType.UNKNOWN
    confidence: float = 0.0
    markers_found: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    dependency_files: List[str] = field(default_factory=list)
    file_count: int = 0
    dir_count: int = 0
    total_size_mb: float = 0.0
    has_docker: bool = False
    docker_path: List[str] = field(default_factory=list)
    has_readme: bool = False
    readme_path: str = ""
    has_git: bool = False
    entry_points: List[str] = field(default_factory=list)
    stack_summary: str = ""
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "project_type": str(self.project_type),
            "confidence": round(self.confidence, 2),
            "markers_found": self.markers_found,
            "frameworks": self.frameworks,
            "dependency_files": self.dependency_files,
            "entry_points": self.entry_points,
            "stack_summary": self.stack_summary,
            "file_count": self.file_count,
            "dir_count": self.dir_count,
            "total_size_mb": round(self.total_size_mb, 2),
            "has_docker": self.has_docker,
            "has_readme": self.has_readme,
            "has_git": self.has_git
        }
    def summary(self) -> str:
        lines = [
            f"Project: {self.name}",
            f"Path: {self.path}",
            f"Type: {self.project_type}",
            f"Confidence: {self.confidence:.0%}",
            f"Files: {self.file_count}",
            f"Directories: {self.dir_count}",
            f"Size: {self.total_size_mb:.1f} MB",
            f"Markers: {', '.join(self.markers_found[:5]) if self.markers_found else 'None'}",
            f"Entry Points: {', '.join(self.entry_points) if self.entry_points else 'None'}",
            f"Docker: {'Yes' if self.has_docker else 'No'}",
            f"README: {'Yes' if self.has_readme else 'No'}",
            f"Git: {'Yes' if self.has_git else 'No'}",
            f"README Path: {self.readme_path or 'No README PATH'}",
            f"dockerfiles: {', '.join(self.docker_path) if self.docker_path else 'None'}",
        ]
        return "\n".join(lines)