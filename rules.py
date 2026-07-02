from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

class Severity(Enum):
    FATAL = "FATAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class Finding:
    rule_code: str
    severity: Severity
    message: str
    entity_type: str
    entity_id: str
    evidence: Dict[str, Any]
    suggested_fix: str
    blocks_allocation: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_code": self.rule_code,
            "severity": self.severity.value,
            "message": self.message,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "evidence": self.evidence,
            "suggested_fix": self.suggested_fix,
            "blocks_allocation": self.blocks_allocation
        }
