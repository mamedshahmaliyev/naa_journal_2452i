from models.person import Person

from enum import Enum

class AcademicRank(str, Enum):
    lecturer = 'lecturer'
    docent = 'docent'
    professor = 'professor'

class ScientificDegree(str, Enum):
    bachelor = 'bachelor'
    master = 'master'
    phd = 'phd'

class Teacher(Person):
    academic_rank: AcademicRank|None = None
    scientific_degree: ScientificDegree|None = None
    