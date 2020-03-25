ON_BACKEND_RUN=docker-compose run --rm kl-backend

reset_db:
	${ON_BACKEND_RUN} bash -c 'echo "DROP SCHEMA public cascade; CREATE SCHEMA public" | python manage.py dbshell'
	${ON_BACKEND_RUN} python manage.py migrate
	${ON_BACKEND_RUN} python manage.py dbseed

clean_env:
	docker-compose down --volumes --rmi all --remove-orphans

makemigrations:
	${ON_BACKEND_RUN} python manage.py makemigrations

