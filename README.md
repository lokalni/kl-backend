# Overview

Teleklasa system provides scalable and simple solution for e-learning.

## System Users And Features

### Moderator users

Browsable interface allows for listing groups and manage students in a given group.

Moderator might use following features:
- Login using username and password or by using quick login url like http://localhost:8080/l/NAU1
- Create or delete group
  Add or delete student within a group
- Reset student personal access link in case it's lost or disclosed
- Create and join new lesson. Starting new lesson will create new BBB room and allow all students assigned 
to a group to join active room using their personal links. 


### Student users

For sake of simplicity, in most cases student user will require only a *single* access url.
In order to join active lesson student needs to use his personal link.
Personal student links look as follows:

http://localhost:8080/UCZEN1

### Admin users

Admin users manage moderators access, their able to create/revoke/reset access for moderators.


## Important concepts


### Conference Server Allocation

Each new lesson created by moderator allocates room on one of BBB swarm servers.
App implements algorithm for selecting optimal server and balance load.

### Students Active Lesson Routing

Students using their quick access link will land on the latest active room for their group.
Access to a conference room is active only if a room (conference) was previously created by the a Moderator.

When a Student uses his personal link and his group does not have active, he/she will be dropped into the limbo, waiting for room to open.


# Local development

### Start App
`docker-compose up`

### Make Migrations
`docker-compose run --rm kl-backend python manage.py makemigrations <app_name like kl_conferences>`

### Django Admin
Open `http://localhost:8000/admin`, log in with admin/admin credentials.

### Services

- Backend server is located at localhost:8000.
Backend is written in Django+DRF

- Webpack dev server is available at localhost:8080.
Webapp is written in vue.js 


