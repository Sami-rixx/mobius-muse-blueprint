from typing import List, Dict, Any
from models import SchoolModel
from rules.base import Finding, Severity
from rules.schema import SchemaRule
from rules.integrity import IntegrityRule
from rules.feasibility import FeasibilityRule

RULE_PACKS = [
    {"name": "Schema Rules", "rules": [
        SchemaRule.check_required_fields,
        SchemaRule.check_type_validity,
    ]},
    {"name": "Integrity Rules", "rules": [
        IntegrityRule.check_duplicate_ids,
        IntegrityRule.check_duplicate_natural_identity,
        IntegrityRule.check_unknown_references,
        IntegrityRule.check_cross_file_consistency,
    ]},
    {"name": "Feasibility Rules", "rules": [
        FeasibilityRule.check_global_capacity,
        FeasibilityRule.check_subject_coverage,
        FeasibilityRule.check_subject_specific_capacity,
        FeasibilityRule.check_teacher_qualification_for_demand,
    ]},
]

class GatecheckerEngine:
    def __init__(self, stop_on_fatal: bool = True):
        self.stop_on_fatal = stop_on_fatal
        self.findings: List[Finding] = []
        self.execution_log: List[str] = []

    def run(self, model: SchoolModel) -> List[Finding]:
        self.findings = []
        self.execution_log = []
        for pack in RULE_PACKS:
            self.execution_log.append(f"Running {pack['name']}...")
            for rule_func in pack['rules']:
                rule_findings = rule_func(model)
                self.findings.extend(rule_findings)
                for finding in rule_findings:
                    self.execution_log.append(f"  {finding.severity.value}: {finding.rule_code} - {finding.message}")
                if self.stop_on_fatal:
                    fatal_findings = [f for f in rule_findings if f.severity == Severity.FATAL]
                    if fatal_findings:
                        self.execution_log.append("  ⚠️ Stopping early due to FATAL findings")
                        return self.findings
        self.execution_log.append("✅ All rule packs completed")
        return self.findings
