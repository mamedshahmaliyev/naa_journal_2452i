from helpers.db import DB

from schemas.subject_input_output import *
from models.subject import Subject

class Subjects:
    
    @classmethod
    def add(cls, inputData: SubjectInputAdd) -> int:
        '''Add a subject to the database and return the id of added item'''
        
        # generate dynamic query using list comprehension
        fields = ', '.join(inputData.model_dump().keys())
        values = ', '.join(['?']*len(inputData.model_dump().keys()))
        sql = f'INSERT INTO subjects ({fields}) values ({values})'
        
        return DB.execute(sql, tuple(inputData.model_dump().values()))    
    
    @classmethod
    def update(cls, id: int, inputData: SubjectInputUpdate) -> Subject:
        '''Update subject by id, update only specified fields'''
        
        updateKeyValues = {field: value for field, value in inputData.model_dump().items() if field in inputData.model_fields_set}
                
        if updateKeyValues:
            updateSql = 'update subjects set ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at=current_timestamp where id = ?'
            print(updateSql, (*updateKeyValues.values(), id))
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
        return cls.search(id=id)[0]
        
        
    @classmethod
    def search(
                cls, 
                id: int|None = None,
                name: str|None = None,
                code: str|None = None,
                hours_from: int|None = None,
                hours_to: int|None = None,
                
                # @todo add credits filter as well
                
                limit: int = 10,
                offset: int = 0
            ) -> list[SubjectOutputSearch]:
        '''Search subjects based on the provided filters'''
        
        sql = 'SELECT * FROM subjects '
        
        where, values = [], {}
        if id is not None:
            where.append("id = :id")
            values = {'id': f'{id}'}
            
        if code is not None:
            where.append("(code = :name)")
            values = {'code': code}
            
        if name is not None:
            where.append("(name like :name OR code like :name)")
            values = {'name': f'%{name}%'}
        
        if hours_from is not None:
            where.append("hours >= :hours_from")
            values['hours_from'] = hours_from
        
        if hours_to is not None:
            where.append("hours <= :hours_to")
            values['hours_to'] = hours_to
                
        sql += ' WHERE ' + ' AND '.join(where) if where else ''
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        print(sql, values)
        return DB.select(sql, values)
    
    @classmethod
    def addSubjectDummyData(cls):
        DB.execute(f'''INSERT INTO subjects (id, name, code, hours, credits) VALUES 
                    (1, 'Object Oriented Programming', 'OOP', 60, 5),
                    (2, 'Programming Basics - 2', 'PB2', 45, null)
                    ON CONFLICT DO NOTHING
                ''')
    
    