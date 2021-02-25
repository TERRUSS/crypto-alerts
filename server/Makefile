
run:
	python manage.py runserver --noreload

resetDB:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	rm db.sqlite3
	make updateDB

updateDB:
	python manage.py makemigrations
	python manage.py migrate

init:
	@echo "Installing dependencies"
	pipenv install django djangorestframework django-rest-auth django-allauth django-cors-headers python-dotenv requests apscheduler
	@echo "Setting up database"
	make updateDB
	@echo "You're all set ! You can now run the application : `make run`"