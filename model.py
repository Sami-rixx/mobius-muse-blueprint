from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

@dataclass
class Teacher:
    id: str
    name: str
    subjects: List[str]
    max_weekly_load: int
    availability: Dict[str, List[int]] = field(default_factory=dict)

@dataclass
class Subject:
    id: str
    name: str
    aliases: List[str] = field(default_factory=list)

@dataclass
class Class:
    id: str
    name: str

@dataclass
class Demand:
    id: str
    class_id: str
    subject_id: str
    weekly_periods: int

@dataclass
class SchoolModel:
    teachers: Dict[str, Teacher] = field(default_factory=dict)
    subjects: Dict[str, Subject] = field(default_factory=dict)
    classes: Dict[str, Class] = field(default_factory=dict)
    demands: List[Demand] = field(default_factory=list)
    teacher_subjects: Dict[str, Set[str]] = field(default_factory=dict)
    subject_demands: Dict[str, List[Demand]] = field(default_factory=dict)
    class_demands: Dict[str, List[Demand]] = field(default_factory=dict)

    def build_indexes(self):
        for tid, t in self.teachers.items():
            self.teacher_subjects[tid] = set(t.subjects)
        for d in self.demands:
            if d.subject_id not in self.subject_demands:
                self.subject_demands[d.subject_id] = []
            self.subject_demands[d.subject_id].append(d)
            if d.class_id not in self.class_demands:
                self.class_demands[d.class_id] = []
            self.class_demands[d.class_id].append(d)
