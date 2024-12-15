from pydantic import BaseModel

from models.student_group import StudentGroup

class Journal(BaseModel):
    id: int
    kafedra: str
    student_group: StudentGroup
    
    # date in format YYYY-MM-DD
    # @todo replace with date type
    start_date: str
    end_date: str