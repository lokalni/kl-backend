# kl-backend
klasa.lokalni.pl - backend server

# Requests
After start app is available at localhost:8000

Try these:

1. List groups `localhost:8000/groups/`
2. Create lesson `curl -X POST -H 'Content-Type: application/json' http://localhost:8000/groups/1/create_lesson/`
3. List lessons `localhost:8000/rooms/`
4. Try join with student URL
 - http://localhost:8000/rooms/join/SEBA
 - http://localhost:8000/rooms/join/DUPA

# Common ops

### Start app
`docker-compose up`

### Make migrations
`docker-compose run --rm kl-backend python manage.py makemigrations <app_name like kl_conferences>`

### Django Admin
Open `http://localhost:8000/admin`, log in with admin/admin credentials.