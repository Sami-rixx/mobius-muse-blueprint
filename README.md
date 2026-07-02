# mobius-muse-blueprint
CBC-compliant school timetable system for Kenyan private schools
# Blueprint Gatechecker

A validation-first rules engine for school timetabling. Checks if school data is structurally complete, internally consistent, and feasible before timetable generation.

## Quick Start

```python
from gatechecker.main import run_gatecheck

result = run_gatecheck(
    teachers_csv="teachers.csv",
    subjects_csv="subjects.csv",
    classes_csv="classes.csv",
    demand_csv="demand.csv"
)

print(result.status)  # BLOCKED, RISKY, READY_WITH_WARNINGS, or READY
print(result.findings) # List of all issues
