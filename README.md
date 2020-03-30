# kl-backend
klasa.lokalni.pl - backend server

# Requests
After start app is available at localhost:8000

Try these:

- List groups http://localhost:8000/groups/

-  Create lesson `curl -X POST -H 'Content-Type: application/json' http://localhost:8000/groups/1/start_lesson/`
This call will create BBB room and redirect you to the conference.

-  List lessons http://localhost:8000/rooms/

-  Try joining with student URL
 - http://localhost:8000/rooms/join/SEBA
 - http://localhost:8000/rooms/join/BRIAN

# Common ops

### Start app
`docker-compose up`

### Make migrations
`docker-compose run --rm kl-backend python manage.py makemigrations <app_name like kl_conferences>`

### Django Admin
Open `http://localhost:8000/admin`, log in with admin/admin credentials.
