from dataclasses import dataclass
from typing import Optional
@dataclass
class AIOutput:
    setup_steps: list[str]
    run_steps: list[str]
    notes: Optional[list[str]] = None