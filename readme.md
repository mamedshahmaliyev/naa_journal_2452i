# How to install and run locally

1. run `pip install -r requirements.txt`
2. run `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
3. navigate to `http://127.0.0.1:8000/docs` and check out documentation
4. execute /populate_dummy_data api endpoint to populate dummy data or /reset_database endpoint to reset the database and remove all data

# How to deploy

1. Use online platforms like https://render.com to deploy the project. Currently this project is deployed to: https://naa-journal-2452i.onrender.com. It may take few minutes to load for the first time.
1. Use `pip install -r requirements.txt` as build command.
1. Use `uvicorn main:app --host 0.0.0.0 --port 80` as start command.

# TODO
1. Search for @todo comments
1. Implement delete functionality

# Project Structure

1. **helpers** - Contains helper and utility classes, currently only [`db.py`](helpers/db.py) helper class, to execute queries against the database.
2. **models** - Contains model (or entity) classes that describe objects and their properties and map to the database.
3. **schemas** - Contains Pydantic schemas for API input and output validation. 
4. **services** - Contains classes for manipulating entities and communicating with the database. Services include:
5. **migrations** - Contains SQL scripts for initializing the database.
6. **main.py** - The entry point of the application, initializes the FastAPI app and defines the API routes.
7. **requirements.txt** - Lists the project dependencies.
8. **readme.md** - Project documentation.