from pydantic import BaseModel
from models.person import Gender
from models.student import Student

from datetime import date

class StudentInputAdd(BaseModel):
    
    # below fields are required
    first_name: str
    last_name: str
    middle_name: str

    # below fields are optional
    gender: Gender|None = None
    birth_date: date|None = None
    
    admission_year: int|None = None


class StudentInputUpdate(BaseModel):
    
    # we use Ellipsis to indicate that the field is not required and to distinguish it from None value and to make it easier to update only specified fields
    first_name: str|None = None
    last_name: str|None = None
    middle_name: str|None = None

    gender: Gender|None = None
    birth_date: date|None = None
    
    admission_year: int|None = None


# example of hiding field from output
class StudentOutputSearch(Student):
    
    class Config:
        exclude = {"created_at"}