"""Diploma project "TODOLIST"""""


"""About the project
In the project, you can create boards, categories, tasks and goals
Registration is available in the project via the Vkontakte "VK" application
You can view and create goals through telegram bot"""


Start the project:

- Clone repository
- Install Python 3.10

- Install requirements:
pip install -r requirements.txt

- Create .env file with constants:
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
DB_HOST
DB_PORT
DEBUG
SECRET_KEY
VK_OAUTH2_KEY
VK_OAUTH2_SECRET
POSTGRES_HOST
BOT_TOKEN

- Create migrations:
python manage.py makemigrations

- Apply migrations:
python manage.py migrate

- Run server:
python manage.py runserver