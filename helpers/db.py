import sqlite3
 
# helper class to work with database
class DB:
    
    @classmethod
    def init(cls):
        '''Create database and all the necessary tables'''
        with open('migrations/base.sql') as f:
            sql = f.read()
            sqlite3.connect(cls.dbFile(), isolation_level=None).executescript(sql)
        
    @classmethod
    def dbFile(cls):
        return 'journal.db'
            
    @classmethod
    def execute(cls, sql, params=()):
        '''Execute the sql query and return lastrowid'''
        with sqlite3.connect(cls.dbFile(), isolation_level=None) as conn:
            crs = conn.cursor()
            crs.execute(sql, params)
            return crs.lastrowid
    
    @classmethod
    def select(cls, sql, params=()) -> list:
        '''select and return associated rows as a list of dictionaries'''
        with sqlite3.connect(cls.dbFile(), isolation_level=None) as conn:
            conn.row_factory = sqlite3.Row
            crs = conn.cursor()
            crs.execute(sql, params)
            return [dict(row) for row in crs.fetchall()] or []
        
        
    