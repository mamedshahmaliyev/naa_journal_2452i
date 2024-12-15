from pydantic import BaseModel
from models.person import Gender
from models.teacher import *


from datetime import date

class TeacherInputAdd(BaseModel):
    
    # below fields are required
    first_name: str
    last_name: str
    middle_name: str

    # below fields are optional
    gender: Gender|None = None
    birth_date: date|None = None
    
    academic_rank: AcademicRank|None = None
    scientific_degree: ScientificDegree|None = None


class TeacherInputUpdate(BaseModel):
    
    # we use Ellipsis to indicate that the field is not required and to distinguish it from None value and to make it easier to update only specified fields
    first_name: str|None = None
    last_name: str|None = None
    middle_name: str|None = None

    gender: Gender|None = None
    birth_date: date|None = None
    
    academic_rank: AcademicRank|None = None
    scientific_degree: ScientificDegree|None = None