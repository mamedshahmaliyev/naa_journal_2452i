import os

from fastapi import FastAPI, HTTPException, status, Query, Request, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from contextlib import asynccontextmanager
from helpers.db import DB

from services.students import Students
from services.teachers import *
from services.subjects import *



# this is a hack to make sure that the database is initialized and all tables are created
@asynccontextmanager
async def lifespan(_: FastAPI):
    # this part until yield is executed before application starts
    DB.init()
    yield

app = FastAPI(lifespan=lifespan, title='Journal API', version='1.0', tags=['test'])

# global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "name": type(e).__name__,
            "message": str(e)
        }
    )
    
# redirect to /docs root path
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def index():
    return "/docs"
    
    

#################### STUDENTS ROUTES ####################

# we use APIRouter to group the routes
# @todo create folder routes and add each route to the separate file
studentRouter = APIRouter(prefix="/students", tags=["Students"])

from schemas.student_input_output import *

@studentRouter.post("/add")
async def students_add(studentData: StudentInputAdd):
    return {'id': Students.addStudent(studentData=studentData)}

# example of using path parameter
@studentRouter.put("/update/{id}")
async def students_update(id: int, studentData: StudentInputUpdate):
    return Students.updateStudent(id=id, studentData=studentData)

@studentRouter.get("/search")
async def students_search(
            id: int|None = Query(None, ge=0),
            name: str|None = Query(None, max_length=50),
            gender: Gender|None = None,
            
            admission_year_from: int|None = Query(None, ge=1950),
            admission_year_to: int|None = None,

            limit: int|None = Query(10, gt=0),
            offset: int|None = Query(0, ge=0)
        ) -> list[StudentOutputSearch]:
    
    # here we use ** to unpack the locals() dictionary into keyword arguments
    return Students.searchStudents(**locals())

app.include_router(studentRouter)

    
    

    
#################### STUDENT GROUP ROUTES ####################

studentGroupRouter = APIRouter(prefix="/student_groups", tags=["Student Groups"])

from schemas.student_group_input_output import *

@studentGroupRouter.post("/add")
async def student_groups_add(studentGroupData: StudentGroupInputAdd):
    return {'id': Students.addStudentGroup(studentGroupData=studentGroupData)}

# example of using path parameter
@studentGroupRouter.put("/update/{id}")
async def student_groups_update(id: int, studentGroupData: StudentGroupInputUpdate):
    return Students.updateStudentGroup(id=id, studentGroupData=studentGroupData)

@studentGroupRouter.get("/search")
async def student_groups_search(
            id: int|None = Query(None, ge=0),
            code: str|None = Query(None, max_length=50),
            starosta: str|None = Query(None, max_length=50, description='Starosta name, surname, middle name or id'),
            limit: int|None = Query(10, gt=0),
            offset: int|None = Query(0, ge=0),
        ) -> list[StudentGroupOutputSearch]:
    
    # here we use ** to unpack the locals() dictionary into keyword arguments
    return Students.searchStudentGroups(**locals())

app.include_router(studentGroupRouter)








    
    

#################### TEACHERS ROUTES ####################


teacherRouter = APIRouter(prefix="/teachers", tags=["Teachers"])

from schemas.teacher_input_output import *

@teacherRouter.post("/add")
async def teachers_add(teacherData: TeacherInputAdd):
    return {'id': Teachers.add(teacherData=teacherData)}

# example of using path parameter
@teacherRouter.put("/update/{id}")
async def teachers_update(id: int, teacherData: TeacherInputUpdate):
    return Teachers.update(id=id, teacherData=teacherData)

@teacherRouter.get("/search")
async def teachers_search(
            id: int|None = Query(None, ge=0),
            name: str|None = Query(None, max_length=50),
            academic_rank: AcademicRank|None = None,

            limit: int|None = Query(10, gt=0),
            offset: int|None = Query(0, ge=0)
        ) -> list[Teacher]:
    return Teachers.search(**locals())

app.include_router(teacherRouter)





#################### SUBJECTS ROUTES ####################
subjectRouter = APIRouter(prefix="/subjects", tags=["Subjects"])

from schemas.subject_input_output import *

@subjectRouter.post("/add")
async def subjects_add(inputData: SubjectInputAdd):
    return {'id': Subjects.add(inputData=inputData)}

@subjectRouter.put("/update/{id}")
async def subjects_update(id: int, inputData: SubjectInputUpdate):
    return Subjects.update(id=id, inputData=inputData)

@subjectRouter.get("/search")
async def subjects_search(
            id: int|None = Query(None, ge=0),
            name: str|None = Query(None, max_length=50),
            code: str|None = Query(None, max_length=50),
            hours_from: int|None = Query(None, ge=0),
            hours_to: int|None = Query(None, ge=0),

            limit: int|None = Query(10, gt=0),
            offset: int|None = Query(0, ge=0)
        ) -> list[SubjectOutputSearch]:
    return Subjects.search(**locals())


app.include_router(subjectRouter)   





#################### JOURNAL ROUTES ####################
journalRouter = APIRouter(prefix="/journals", tags=["Journals"])

from schemas.journal_input_output import *
from services.journals import *

@journalRouter.post("/add")
async def journals_add(inputData: JournalInputAdd):
    return {'id': Journals.add(inputData=inputData)}

@journalRouter.put("/update/{id}")
async def journals_update(id: int, inputData: JournalInputUpdate):
    return Journals.update(id=id, inputData=inputData)

@journalRouter.get("/search")
async def journals_search(
            id: int|None = Query(None, ge=0),
            kafedra: str|None = None,
            student_group: str|None = Query(None, description="Student group id or code"),
            start_date: date|None = None,
            end_date: date|None = None,

            limit: int|None = Query(10, gt=0),
            offset: int|None = Query(0, ge=0)
        ) -> list[JournalOutputSearch]:
    return Journals.search(**locals())


app.include_router(journalRouter)   




#################### DATABASE ROUTES ####################

dummyDataRouter = APIRouter(tags=["Database"])

@dummyDataRouter.post("/populate_dummy_data")
async def populate_dummy_data():
    '''Populate the database with dummy data'''
    
    Students.addStudentDummyData()
    Students.addStudentGroupDummyData()
    Teachers.addTeacherDummyData()
    Subjects.addSubjectDummyData()
    Journals.addJournalDummyData()
    
    return True

@dummyDataRouter.post("/reset_database")
async def reset_database():
    '''Reset the database and truncate all data'''
    
    os.remove('journal.db')
    DB.init()
    
    return True

app.include_router(dummyDataRouter)

