from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, date

app = FastAPI()

class Subject:
    name: str
    code: str

class Group:
    code: str

class Student(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    birthdate: date
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class StudentManager:
    studentList: list[Student] = []
    
    def add(self, student: Student):
        self.studentList.append(student)
        
studentManager = StudentManager()
    

@app.get("/")
async def root():
    return {
        "message": "Salam",
        "description": "This is a simple API",
        "number": [1, 2, 3, 4, 5],
    }

@app.post("/students/add")
async def add(student: Student):
    '''This resource adds new student'''
    studentManager.add(student)

@app.get("/students/list")
async def list() -> list[Student]:
    return studentManager.studentList