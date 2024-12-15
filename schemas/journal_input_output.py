from pydantic import BaseModel
from datetime import date, datetime

class JournalInputAdd(BaseModel):
    kafedra: str
    student_group_id: int
    start_date: date
    end_date: date

class JournalInputUpdate(BaseModel):
    kafedra: str|None = None
    student_group_id: int|None = None
    start_date: date|None = None
    end_date: date|None = None
    
    
class JournalOutputSearch(BaseModel):
    id: int
    kafedra: str
    student_group_id: int
    start_date: date
    end_date: date
    created_at: datetime
    updated_at: datetime