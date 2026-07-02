from models import SchoolModel
from normalizer import Normalizer
from engine import GatecheckerEngine
from result_builder import ResultBuilder, GateResult

def run_gatecheck(teachers_csv=None, subjects_csv=None, classes_csv=None, demand_csv=None, json_file=None):
    normalizer = Normalizer()
    engine = GatecheckerEngine()
    builder = ResultBuilder()

    if json_file:
        model = normalizer.normalize_from_json(json_file)
    else:
        if not all([teachers_csv, subjects_csv, classes_csv, demand_csv]):
            raise ValueError("Either provide all CSV files or a JSON file")
        model = normalizer.normalize_from_csv(teachers_csv, subjects_csv, classes_csv, demand_csv)

    if normalizer.errors:
        from rules.base import Finding, Severity
        findings = [Finding(
            rule_code="N001", severity=Severity.FATAL,
            message="Normalization failed", entity_type="Normalizer",
            entity_id="normalization", evidence={"errors": normalizer.errors},
            suggested_fix="Fix the input files", blocks_allocation=True
        )]
        return builder.build(findings)

    findings = engine.run(model)
    return builder.build(findings)

def print_result(result: GateResult):
    print("\n" + "="*60)
    print("BLUEPRINT GATECHECKER RESULTS")
    print("="*60)
    status_icon = {"BLOCKED": "❌", "RISKY": "⚠️", "READY_WITH_WARNINGS": "✅", "READY": "✅✅"}
    print(f"\nStatus: {status_icon.get(result.status.value, '')} {result.status.value}")
    print(f"Allocation Allowed: {'YES' if result.allocation_allowed else 'NO'}")
    print(f"\nSummary:")
    print(f"  Total Findings: {result.summary['total_findings']}")
    print(f"  FATAL: {result.summary['by_severity']['FATAL']}")
    print(f"  HIGH: {result.summary['by_severity']['HIGH']}")
    print(f"  MEDIUM: {result.summary['by_severity']['MEDIUM']}")
    print(f"  LOW: {result.summary['by_severity']['LOW']}")
    if result.findings:
        print(f"\nFindings:")
        for i, finding in enumerate(result.findings, 1):
            print(f"\n  {i}. [{finding.severity.value}] {finding.rule_code}")
            print(f"     Entity: {finding.entity_type}({finding.entity_id})")
            print(f"     Message: {finding.message}")
            print(f"     Fix: {finding.suggested_fix}")
            if finding.blocks_allocation:
                print(f"     ⚠️ BLOCKS ALLOCATION")
    else:
        print("\n✅ No findings! Data is valid.")
    print("\n" + "="*60)

if __name__ == "__main__":
    print("Blueprint Gatechecker - School Timetable Validation Engine")
    result = run_gatecheck(
        teachers_csv="gatechecker/sample_data/teachers.csv",
        subjects_csv="gatechecker/sample_data/subjects.csv",
        classes_csv="gatechecker/sample_data/classes.csv",
        demand_csv="gatechecker/sample_data/demand.csv"
    )
    print_result(result)
