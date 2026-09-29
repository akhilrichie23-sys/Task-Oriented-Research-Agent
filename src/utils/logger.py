import json
import os
from datetime import datetime

class AuditLogger:
    def __init__(self, log_dir: str = "outputs/audit_logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"execution_trace_{session_id}.json")
        self.logs = []

    def log_step(self, step_name: str, details: dict):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step_name,
            "details": details
        }
        self.logs.append(entry)
        self._flush()

    def _flush(self):
        with open(self.log_file, "w") as f:
            json.dump(self.logs, f, indent=2)
