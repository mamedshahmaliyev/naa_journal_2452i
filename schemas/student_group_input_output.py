from pydantic import BaseModel

from schemas.student_input_output import StudentOutputSearch

class StudentGroupInputAdd(BaseModel):
    code: str
    starosta_student_id: int|None = None


class StudentGroupInputUpdate(BaseModel):
    code: int|None = None
    starosta_student_id: int|None = None

class StudentGroupOutputSearch(BaseModel):
    id: int
    code: str
    
    # here we use StudentOutputSearch to represent the starosta
    starosta: StudentOutputSearch|None = None