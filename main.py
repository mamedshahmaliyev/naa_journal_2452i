from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Salam",
        "description": "This is a simple API",
        "number": [1, 2, 3, 4, 5],
    }

@app.get("/add")
async def add(first_number: int, second_number: int):
    '''This resource dds two numbers and returns its sum'''
    return {
        "sum": first_number + second_number,
    }

@app.get("/minus")
async def minus(a: int, b: int):
    '''This resource subtracts two numbers and returns the result a-b'''
    return {
        "sub": a - b,
    }