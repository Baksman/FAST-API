python3 -m venv venv
source venv/bin/activate
pip freeze
uvicorn nameofifle:[name of instance] --reload
uvicorn app.main:app --reload

# alembic 
alembic init
alembic revision -m "descritpion of the revision"
alembic current
alembic  head
alembic history
alembic upgrade revision-number(or head is head is where we want to upgrade +n)
alembic downgrade revision-number(or -n  (where n is no of back revision))
alembi revision --autogenerate -m "commit message"

# requiremnt.txt
pip freeze > requirement.txt
pip install -r requirement.txt

# heroku
heroku logs -t
heroku ps restart