# kl-backend
klasa.lokalni.pl - backend server

# Requests
After start app is available at localhost:8000

- List groups `localhost:8000/groups/`
- Create lesson `curl -X POST -H 'Content-Type: application/json' http://localhost:8000/groups/1/create_lesson/`
- List lessons `localhost:8000/rooms/`

# Common ops

### Start app
`docker-compose up`

### Make migrations
`docker-compose run --rm kl-backend python manage.py makemigrations <app_name like kl_conferences>`

