from pathlib import Path
import platform
from typing import Union, List
def to_path(path: Union[str, Path]) -> Path:
    if isinstance(path, Path):
        return path
    return Path(path)
def is_hidden_folder(path: Path) -> bool:
    if platform.system() != "Windows":
        for part in path.parts:
            if part.startswith('.'):
                return True
        return False
    import ctypes
    full_path = str(path)
    current_path = Path(full_path)
    while current_path != current_path.parent:  
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(current_path))
            if attrs != -1 and (attrs & 2):
                return True
        except Exception:
            if current_path.name.startswith('.'):
                return True
            current_path = current_path.parent
    return False
def should_skip_path(path: Path) -> bool:
    skip_folders = {
        'venv', 'env', '.venv', '__pycache__', 
        'node_modules', '.git', 'dist', 'build',
        '.idea', '.vscode', '.pytest_cache', 'target',
        '.mvn', '.gradle', 'vendor'
    }
    parts = path.parts
    for part in parts:
        if part in skip_folders:
            return True
    return False
def get_file_size_mb(path: Path) -> float:
    try:
        size_bytes = path.stat().st_size
        return size_bytes / (1024 * 1024)  
    except (PermissionError, OSError):
        return 0.0
def get_folder_size_mb(path: Path) -> float:
    total = 0
    skipped = 0
    for item in path.rglob('*'):
        try:
            if item.is_file():
                stat = item.stat()
                total += stat.st_blocks * 512
        except Exception as e:
            skipped += 1
            print(f"Skipped: {item} -> {e}")

    print(f"Total skipped files: {skipped}")
    return round(total / (1024 * 1024), 1)
def safe_scan(path: Path, pattern: str = "*") -> List[Path]:
    try:
        return list(path.glob(pattern))
    except PermissionError:
        return []
def get_file_extension(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix.startswith('.'):
        return suffix[1:] 
    return suffix
def is_source_file(file_path: Path) -> bool:
    source_extensions = {
        'py', 'js', 'jsx', 'ts', 'tsx',  
        'java', 'kt', 'scala',           
        'php', 'rb', 'go', 'rs',         
        'c', 'cpp', 'h', 'hpp',          
        'cs', 'fs',                      
        'swift', 'm',                    
    }
    ext = get_file_extension(file_path)
    return ext in source_extensions
def get_relative_path(full_path: Path, base_path: Path) -> str:
    try:
        return str(full_path.relative_to(base_path))
    except ValueError:
        return str(full_path)
def normalize_path_for_display(path: Path) -> str:
    path_str = str(path)    
    if platform.system() != "Windows":
        home = str(Path.home())
        if path_str.startswith(home):
            return "~" + path_str[len(home):]
    return path_str