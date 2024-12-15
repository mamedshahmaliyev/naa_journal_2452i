from pydantic import BaseModel, computed_field
from datetime import date

from enum import Enum

class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'

# an example of ABSTRACTION, we are abstracting Person model for our journaling system
class Person(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    
    # example of optional parameter
    gender: Gender|None = None
    
    # date in format YYYY-MM-DD
    birth_date: str|None = None
    
    # example of ENCAPSULATION, we are encapsulating the the logic of how full_name is calculated
    @computed_field
    @property
    def full_name(self) -> str:    
        return self.first_name + ' ' + self.last_name
    
    # another example of ENCAPSULATION, we are encapsulating the the logic of how age is calculated
    @property
    def age(self) -> int|None:
        if self.birth_date is None:
            return None
        return date.today().year - int(self.birth_date.split('-')[0])
    
    created_at: str
    updated_at: str|None = None

    
    