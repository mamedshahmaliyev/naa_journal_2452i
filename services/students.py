from models.student import Student
from models.student_group import StudentGroup
from helpers.db import DB

from schemas.student_input_output import *
from schemas.student_group_input_output import *

from fastapi import HTTPException, status

class Students:
    
    @classmethod
    def addStudent(cls, studentData: StudentInputAdd) -> int:
        '''Add a student to the database and return the id of the new student'''
        
        # @todo convert to dynamic query
        studentId = DB.execute('''
                                INSERT INTO students (first_name, last_name, middle_name, gender, birth_date, admission_year)
                                values (?, ?, ?, ?, ?, ?)
                                ''', 
                                (studentData.first_name, studentData.last_name, studentData.middle_name, studentData.gender, studentData.birth_date, studentData.admission_year)
                            )        
        
        return studentId
    
    @classmethod
    def updateStudent(cls, id: int, studentData: StudentInputUpdate) -> Student:
        '''Update student by id, update only specified fields'''
        
        # @todo add validation for id
        
        updateKeyValues = {}
        
        for field, value in studentData.model_dump().items():
            # check if the field is in the model_fields_set and specified by user, if not, then skip it
            if field in studentData.model_fields_set:
                updateKeyValues[field] = value
                
        if updateKeyValues:
            # here we build update query dynamically using list comprehension
            updateSql = 'update students set ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at=current_timestamp where id = ?'
            print(updateSql, (*updateKeyValues.values(), id))
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
            
        return cls.searchStudents(id=id)[0]
        
        
    @classmethod
    def searchStudents(
                cls, 
                id: int|None = None,
                name: str|None = None,
                
                # @todo add gender filter
                gender: Gender|None = None,
                
                admission_year_from: int|None = None,
                admission_year_to: int|None = None,
                
                limit: int = 10,
                offset: int = 0
            ) -> list[Student]:
        '''Search students based on the provided filters'''
        
        sql = 'SELECT * FROM students '
        
        where, values = [], {}
            
        if id is not None:
            where.append("id = :id")
            values = {'id': f'{id}'}
            
        if name is not None:
            # use parenthesis to group OR conditions
            where.append("(first_name like :name OR last_name like :name OR middle_name like :name)")
            values = {'name': f'%{name}%'}
        
        # @todo check if admission_year_from is less than admission_year_to, if they are equal, then we can use admission_year = :admission_year_from
        if admission_year_from is not None:
            where.append("admission_year >= :admission_year_from")
            values['admission_year_from'] = admission_year_from
        
        if admission_year_to is not None:
            where.append("admission_year <= :admission_year_to")
            values['admission_year_to'] = admission_year_to
                
        sql += ' WHERE ' + ' AND '.join(where) if where else ''
            
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        print(sql, values)
        
        return DB.select(sql, values)
    
    
    @classmethod
    def addStudentDummyData(cls):
        # use ON CONFLICT DO NOTHING to avoid duplicate entries and ignore if the entry already exists
        DB.execute(f'''INSERT INTO students 
                    (id, first_name, last_name, middle_name, gender, birth_date, admission_year) VALUES 
                    (1, 'Əli', 'Vəliyev', 'Salman', 'male', '2000-01-01', 2020),
                    (2, 'Leyla', 'Məmmədova', 'Həsən', 'female', '2001-11-10', 2020),
                    (3, 'Tural', 'Quliyev', 'Abbas', 'male', '2000-01-01', 2020)
                    ON CONFLICT DO NOTHING
                ''')
    
    
    # @todo extract student group related methods to the separate class
    
    
    @classmethod
    def addStudentGroup(cls, studentGroupData: StudentGroupInputAdd) -> int:
        '''Add a student group to the database and return the id of the new group'''
        
        if studentGroupData.starosta_student_id is not None:
            if not cls.searchStudents(id=studentGroupData.starosta_student_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Student with id {studentGroupData.starosta_student_id} does not exist')
        
        return DB.execute('''
                                INSERT INTO student_groups (code, starosta_student_id)
                                values (?, ?)
                                ''', 
                                (studentGroupData.code, studentGroupData.starosta_student_id)
                            )  
    
    
    @classmethod
    def updateStudentGroup(cls, id: int, studentGroupData: StudentGroupInputUpdate) -> StudentGroupOutputSearch:
        '''Update a student group and return updated group'''
        
        # @todo add validation for id
        
        if studentGroupData.starosta_student_id is not None:
            if not cls.searchStudents(id=studentGroupData.starosta_student_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Student with id {studentGroupData.starosta_student_id} does not exist')
        
        updateKeyValues = {field: value for field, value in studentGroupData.model_dump().items() if field in studentGroupData.model_fields_set}
                
        if updateKeyValues:
            updateSql = 'update student_groups set ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at=current_timestamp where id = ?'
            print(updateSql, (*updateKeyValues.values(), id))
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
            
        return cls.searchStudentGroups(id=id)[0]
    
    
    
    @classmethod
    def searchStudentGroups(
                cls, 
                id: int|None = None,
                code: str|None = None,
                starosta: str|None = None,
                limit: int = 10,
                offset: int = 0
            ) -> list[StudentGroupOutputSearch]:
        '''Search students based on the provided filters'''
        
        sql = 'SELECT sg.* FROM student_groups sg LEFT JOIN students s ON sg.starosta_student_id = s.id '
        
        where, values = [], {}
            
        if id is not None:
            where.append("sg.id = :id")
            values = {'id': f'{id}'}
            
        if code is not None:
            where.append("code like :code")
            values = {'code': f'%{code}%'}
        
        if starosta is not None:
            where.append("(s.id = :starosta_id OR s.first_name like :starosta OR s.last_name like :starosta OR s.middle_name like :starosta)")
            values = {'starosta': f'%{starosta}%', 'starosta_id': starosta}
                
        sql += ' WHERE ' + ' AND '.join(where) if where else ''
            
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        print(sql, values)
        
        items = DB.select(sql, values)
        
        for item in items:
            if item['starosta_student_id']:
                item['starosta'] = cls.searchStudents(id=item['starosta_student_id'])[0]
        
        return items
    
    
    @classmethod
    def addStudentGroupDummyData(cls):
        DB.execute('''INSERT INTO student_groups (id, code, starosta_student_id) VALUES (1, '2000i', 1) ON CONFLICT DO NOTHING''')
    