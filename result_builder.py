from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any
from rules.base import Finding, Severity

class GateStatus(Enum):
    BLOCKED = "BLOCKED"
    RISKY = "RISKY"
    READY_WITH_WARNINGS = "READY_WITH_WARNINGS"
    READY = "READY"

@dataclass
class GateResult:
    status: GateStatus
    findings: List[Finding]
    summary: Dict[str, Any]
    allocation_allowed: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "allocation_allowed": self.allocation_allowed,
            "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings]
        }

class ResultBuilder:
    @staticmethod
    def build(findings: List[Finding]) -> GateResult:
        severity_counts = {"FATAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        blocks_allocation = False
        for finding in findings:
            severity_counts[finding.severity.value] += 1
            if finding.blocks_allocation:
                blocks_allocation = True

        if severity_counts["FATAL"] > 0:
            status = GateStatus.BLOCKED
            allocation_allowed = False
        elif severity_counts["HIGH"] > 0:
            status = GateStatus.RISKY
            allocation_allowed = True
        elif severity_counts["MEDIUM"] > 0 or severity_counts["LOW"] > 0:
            status = GateStatus.READY_WITH_WARNINGS
            allocation_allowed = True
        else:
            status = GateStatus.READY
            allocation_allowed = True

        summary = {
            "total_findings": len(findings),
            "by_severity": severity_counts,
            "blocks_allocation": blocks_allocation,
        }
        return GateResult(status=status, findings=findings, summary=summary, allocation_allowed=allocation_allowed)
