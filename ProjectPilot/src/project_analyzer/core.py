from pathlib import Path
import os
from .models import ProjectInfo, ProjectType
from .utils import to_path, should_skip_path, get_folder_size_mb, is_hidden_folder
class ProjectAnalyzer:
    def __init__(self):
        self._init_detection_patterns()

    def _init_detection_patterns(self):
        self.project_markers = {
            ProjectType.PYTHON: {
                'files': ['requirements.txt', 'setup.py', 'Pipfile', 'pyproject.toml', 'manage.py'],
                'folders': ['venv', 'env', '.venv']
            },
            ProjectType.NODEJS: {
                'files': ['package.json', 'yarn.lock', 'package-lock.json'],
                'folders': ['node_modules']
            },
            ProjectType.JAVA_MAVEN: {
                'files': ['pom.xml', 'mvnw', 'mvnw.cmd'],
                'folders': ['.mvn', 'src/main/java']
            },
            ProjectType.JAVA_GRADLE: {
                'files': ['build.gradle', 'gradlew', 'gradlew.bat', 'settings.gradle'],
                'folders': ['.gradle', 'src/main/java']
            },
            ProjectType.PHP: {
                'files': ['composer.json', 'composer.lock', 'artisan', 'wp-config.php'],
                'folders': ['vendor', 'wp-content']
            }
        }
    def analyze(self, path: str) -> ProjectInfo:
        project_path = to_path(path)
        if not project_path.exists():
            raise FileNotFoundError(f"Path does not exist: {project_path}")
        if not project_path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {project_path}")

        info = ProjectInfo(
            name=project_path.name,
            path=str(project_path),
            entry_points=[],
            stack_summary=""
        )
        self._scan_directory(project_path, info)
        self._check_important_files(project_path, info)
        self._detect_project_type(info)
        self._find_entry_points(project_path, info)
        return info
    def _scan_directory(self, path: Path, info: ProjectInfo):
        file_count, dir_count = 0, 0
        try:
            for root, dirs, files in os.walk(path):
                current_path = Path(root)
                if should_skip_path(current_path):
                    continue
                if current_path != path:
                    dir_count += 1
                for project_type, markers in self.project_markers.items():
                    for folder in markers['folders']:
                        if folder in dirs and f"{project_type.value}: folder:{folder}" not in info.markers_found:
                            info.markers_found.append(f"{project_type.value}: folder:{folder}")
                for file in files:
                    file_path = current_path / file
                    if is_hidden_folder(file_path):
                        continue
                    file_count += 1
                    self._check_marker_file(file_path, info)
        except PermissionError:
            pass
        info.file_count = file_count
        info.dir_count = dir_count
        info.total_size_mb = get_folder_size_mb(path)
    def _check_marker_file(self, file_path: Path, info: ProjectInfo):
        file_name = file_path.name
        for project_type, markers in self.project_markers.items():
            if file_name in markers['files']:
                marker = f"{project_type.value}: {file_name}"
                if marker not in info.markers_found:
                    info.markers_found.append(marker)
                info.dependency_files.append(str(file_path))
    def _check_important_files(self, path: Path, info: ProjectInfo):
        for name in ['README.md', 'README.txt', 'README', 'README.rst']:
            readme_file = path / name
            if readme_file.exists():
                info.has_readme = True
                info.readme_path = str(readme_file)
                break
        dockerfiles = list(path.rglob("Dockerfile"))
        compose_files = []
        for ext in ("yml", "yaml"):
            compose_files += list(path.rglob(f"compose*.{ext}"))
            compose_files += list(path.rglob(f"docker-compose*.{ext}"))
        all_docker = compose_files + dockerfiles
        if all_docker:
            info.has_docker = True
            def priority(p: Path):
                name = p.name.lower()
                is_compose = 0 if "compose" in name else 1
                depth = len(p.parts)
                return (is_compose, depth)
            sorted_docker = sorted(all_docker, key=priority)
            info.docker_path = [str(p) for p in sorted_docker]
        if (path / '.git').exists():
                    info.has_git = True
    def _detect_project_type(self, info: ProjectInfo):
        critical_markers = {
            ProjectType.PYTHON: ['requirements.txt', 'setup.py', 'manage.py', 'pyproject.toml'],
            ProjectType.NODEJS: ['package.json'],
            ProjectType.JAVA_MAVEN: ['pom.xml', 'mvnw'],
            ProjectType.JAVA_GRADLE: ['build.gradle', 'gradlew'],
            ProjectType.PHP: ['composer.json', 'artisan'],
        }
        detected_type = None
        for pt, markers in critical_markers.items():
            for marker in markers:
                if any(marker in f for f in info.markers_found):
                    detected_type = pt
                    break
            if detected_type:
                break
        if detected_type:
            info.project_type = detected_type
            info.confidence = 1.0
        else:
            type_counts = {pt: 0 for pt in ProjectType}
            for marker in info.markers_found:
                for pt in critical_markers.keys():
                    if pt.value in marker:
                        type_counts[pt] += 1
            best_type = max(type_counts, key=type_counts.get)
            if type_counts[best_type] > 0:
                info.project_type = best_type
                info.confidence = 0.5
            else:
                info.project_type = ProjectType.UNKNOWN
                info.confidence = 0.0
    def _find_entry_points(self, path: Path, info: ProjectInfo):
        entry_patterns = {
            ProjectType.PYTHON: ['main.py', 'run.py', 'wsgi.py', 'manage.py', 'app.py', 'application.py'],
            ProjectType.NODEJS: ['index.js', 'main.js', 'app.js', 'server.js'],
            ProjectType.JAVA_MAVEN: ['Application.java', 'Main.java'],
            ProjectType.JAVA_GRADLE: ['Application.java', 'Main.java'],
            ProjectType.PHP: ['index.php', 'artisan'],
        }
        for pattern in entry_patterns.get(info.project_type, []):
            for file in path.rglob(pattern):
                if file.is_file() and str(file) not in info.entry_points:
                    info.entry_points.append(str(file))