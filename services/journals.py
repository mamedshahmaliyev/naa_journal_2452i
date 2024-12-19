from helpers.db import DB

from schemas.journal_input_output import *
from models.journal import Journal

class Journals:
    
    @classmethod
    def add(cls, inputData: JournalInputAdd) -> int:
        '''Add a journal item to the database and return the id of added item'''
        
        fields = ', '.join(inputData.model_dump().keys())
        values = ', '.join(['?']*len(inputData.model_dump().keys()))
        sql = f'INSERT INTO subjects ({fields}) values ({values})'
        
        return DB.execute(sql, tuple(inputData.model_dump().values()))    
    
    @classmethod
    def update(cls, id: int, inputData: JournalInputUpdate) -> Journal:
        '''Update journal by id, update only specified fields'''
        
        updateKeyValues = {field: value for field, value in inputData.model_dump().items() if field in inputData.model_fields_set}
                
        if updateKeyValues:
            updateSql = 'update journals set ' + ', '.join([f'{key} = ?' for key in updateKeyValues.keys()]) + ', updated_at=current_timestamp where id = ?'
            print(updateSql, (*updateKeyValues.values(), id))
            DB.execute(updateSql, (*updateKeyValues.values(), id))
            
        return cls.search(id=id)[0]
        
        
    @classmethod
    def search(
                cls, 
                id: int|None = None,
                kafedra: str|None = None,
                student_group: str|None = None,
                start_date: date|None = None,
                end_date: date|None = None,
                
                limit: int = 10,
                offset: int = 0
            ) -> list[JournalOutputSearch]:
        '''Search journals based on the provided filters'''
        
        sql = """
                SELECT j.*, sg.code || ' [id: '|| sg.id || ']' as student_group  
                FROM journals j 
                left join student_groups sg on sg.id = j.student_group_id
                """
        
        where, values = [], {}
        if id is not None:
            where.append("j.id = :id")
            values['id']=id
            
        if kafedra is not None:
            where.append("(kafedra = :kafedra)")
            values['kafedra']=f'%{kafedra}%'
        
        if student_group is not None:
            where.append("(student_group_id = :student_group or sg.code = :student_group)")
            values['student_group']=student_group
        
        if start_date is not None:
            where.append("start_date = :start_date")
            values['start_date']=start_date
        
        if end_date is not None:
            where.append("end_date = :end_date")
            values['end_date']=end_date
                
        sql += ' WHERE ' + ' AND '.join(where) if where else ''
        sql += f' LIMIT {limit} OFFSET {offset}'
        
        print(sql, values)
        return DB.select(sql, values)
    
    @classmethod
    def addJournalDummyData(cls):
        DB.execute(f'''INSERT INTO journals (id, kafedra, student_group_id, start_date, end_date) VALUES 
                    (1, 'Aerokosmik', 1, '2024-09-15', '2024-12-31')
                    ON CONFLICT DO NOTHING
                ''')
    
    