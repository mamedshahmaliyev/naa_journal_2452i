
# example of class using constructor, without using BaseModel
class Subject:
    def __init__(self, id: int, name: str, code: str, hours: int, credits: int = None):
        self.id = id
        self.name = name
        self.code = code
        self.hours = hours
        self.credits = credits
