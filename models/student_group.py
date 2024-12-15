from pydantic import BaseModel

from models.student import Student

class StudentGroup(BaseModel):
    code: str
    starosta: Student|None = None