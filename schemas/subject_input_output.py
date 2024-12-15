from pydantic import BaseModel


class SubjectInputAdd(BaseModel):
    name: str
    code: str
    hours: int
    
    # credits is optional
    credits: int|None = None


class SubjectInputUpdate(BaseModel):
    name: str|None = None
    code: str|None = None
    hours: int|None = None
    credits: int|None = None
    
    
class SubjectOutputSearch(BaseModel):
    id: int
    name: str
    code: str
    hours: int
    credits: int|None = None