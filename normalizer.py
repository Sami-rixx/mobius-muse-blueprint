import csv
import json
from typing import Dict, List
from models import SchoolModel, Teacher, Subject, Class, Demand

class Normalizer:
    def __init__(self):
        self.errors: List[str] = []

    def normalize_from_csv(self, teachers_path, subjects_path, classes_path, demand_path) -> SchoolModel:
        model = SchoolModel()
        model.teachers = self._load_teachers_csv(teachers_path)
        model.subjects = self._load_subjects_csv(subjects_path)
        model.classes = self._load_classes_csv(classes_path)
        model.demands = self._load_demand_csv(demand_path)
        model.build_indexes()
        return model

    def _load_teachers_csv(self, path: str) -> Dict[str, Teacher]:
        teachers = {}
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    teacher = Teacher(
                        id=row['id'],
                        name=row['name'],
                        subjects=row.get('subjects', '').split(';') if row.get('subjects') else [],
                        max_weekly_load=int(row.get('max_weekly_load', 20)),
                        availability=json.loads(row.get('availability', '{}'))
                    )
                    teachers[teacher.id] = teacher
        except Exception as e:
            self.errors.append(f"Error loading teachers: {e}")
        return teachers

    def _load_subjects_csv(self, path: str) -> Dict[str, Subject]:
        subjects = {}
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    subject = Subject(
                        id=row['id'],
                        name=row['name'],
                        aliases=row.get('aliases', '').split(';') if row.get('aliases') else []
                    )
                    subjects[subject.id] = subject
        except Exception as e:
            self.errors.append(f"Error loading subjects: {e}")
        return subjects

    def _load_classes_csv(self, path: str) -> Dict[str, Class]:
        classes = {}
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cls = Class(id=row['id'], name=row['name'])
                    classes[cls.id] = cls
        except Exception as e:
            self.errors.append(f"Error loading classes: {e}")
        return classes

    def _load_demand_csv(self, path: str) -> List[Demand]:
        demands = []
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    demand = Demand(
                        id=row['id'],
                        class_id=row['class_id'],
                        subject_id=row['subject_id'],
                        weekly_periods=int(row['weekly_periods'])
                    )
                    demands.append(demand)
        except Exception as e:
            self.errors.append(f"Error loading demand: {e}")
        return demands
