from models.student import Student
from helpers.db import DB

from schemas.teacher_input_output import *

class Teachers:
    
    @classmethod
    def add(cls, teacherData: TeacherInputAdd) -> int:
        '''Add a teacher to the database and return the id of added item'''
        
        studentId = DB.execute('''
                                INSERT INTO teachers (first_name, last_name, middle_name, gender, birth_date, academic_rank, scientific_degree)
                                values (?, ?, ?, ?, ?, ?, ?)
                                ''', 
                                (teacherData.first_name, teacherData.last_name, teacherData.middle_name, teacherData.gender, teacherData.birth_date, teacherData.academic_rank, teacherData.scientific_degree)
                            )        
        
        return studentId
    
    @classmethod
    def update(cls, id: int, teacherData: TeacherInputUpdate) -> Teacher:
        '''Update teacher by id, update only specified fields'''
        
        updateKeyValues = {}
        
        for field, value in teacherData.model_dump().items():
            # check if the field is in the model_fields_set and specified by user, if not, then skip it
            if field in teacherData.model_fields_set:
                updateKeyValues[field] = value
                
        if updateKeyValues:
            # here we build update query dynamically using list comprehension
            updateSql = 'update teachers set ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at=current_timestamp where id = ?'
            print(updateSql, (*updateKeyValues.values(), id))
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
            
        return cls.search(id=id)[0]
        
        
    @classmethod
    def search(
                cls, 
                id: int|None = None,
                name: str|None = None,
                academic_rank: AcademicRank|None = None,
                
                limit: int = 10,
                offset: int = 0
            ) -> list[Student]:
        '''Search teachers based on the provided filters'''
        
        sql = 'SELECT * FROM teachers '
        
        where, values = [], {}
        if id is not None:
            where.append("id = :id")
            values = {'id': f'{id}'}
            
        if name is not None:
            where.append("(first_name like :name OR last_name like :name OR middle_name like :name)")
            values = {'name': f'%{name}%'}
        
        if academic_rank is not None:
            where.append("academic_rank = :academic_rank")
            values['academic_rank'] = academic_rank.value
                
        sql += ' WHERE ' + ' AND '.join(where) if where else ''
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        print(sql, values)
        return DB.select(sql, values)
    
    @classmethod
    def addTeacherDummyData(cls):
        DB.execute(f'''INSERT INTO teachers 
                    (id, first_name, last_name, middle_name, gender, birth_date, academic_rank, scientific_degree) VALUES 
                    (1, 'Samir', 'Ağayev', 'Vəli', 'male', '1986-08-03', '{AcademicRank.docent.value}', '{ScientificDegree.phd.value}'),
                    (2, 'Nigar', 'Əhmədova', 'Azər', 'female', '1990-01-02', '{AcademicRank.professor.value}', null)
                    ON CONFLICT DO NOTHING
                ''')
    
    