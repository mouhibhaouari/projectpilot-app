# ProjectPilot

ProjectPilot is a FastAPI service that analyzes a target project folder and returns:

- basic project metadata (type, markers, entry points, file stats)
- install/run hints inferred from Docker files or README content

## What This API Does

The API exposes one endpoint:

- `POST /analyze`

Request body:

```json
{
	"path": "/absolute/path/to/project"
}
```

Response contains:

- `project`: analyzed metadata from `ProjectAnalyzer`
- `install`: installation guidance source and result

## Requirements

- Linux/macOS/Windows
- Python 3.12+ recommended
- `pip`

## Quick Start

Run these commands from the project root.

### 1. Create virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
```

Windows (PowerShell):

```powershell
python -m venv .venv
```

### 2. Install dependencies

Linux/macOS:

```bash
./.venv/bin/pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\pip install -r requirements.txt
```

### 3. Run the API server

Linux/macOS:

```bash
./.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### 4. Open Swagger UI

- http://127.0.0.1:8000/docs

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
	-H "Content-Type: application/json" \
	-d '{"path":"/absolute/path/to/your/project"}'
```

## Running Tests

Linux/macOS:

```bash
./.venv/bin/pytest
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\pytest
```

## Notes

- Prefer using `.venv` created locally for reliable execution.
- If your target project path does not exist, `/analyze` returns HTTP 404.
- If the target path is not a directory, `/analyze` returns HTTP 400.