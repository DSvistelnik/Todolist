The project "TODOLIST"

Start the project:

- Clone repository
- Install Python 3.10

- Install requirements:
pip install -r requirements.txt
- 
- Create .env file with constants:
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
DB_HOST
DB_PORT
DEBUG
SECRET_KEY

- Create migrations:
python manage.py makemigrations

- Apply migrations:
python manage.py migrate

- Run server:
python manage.py runserver