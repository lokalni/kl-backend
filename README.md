# Overview

TeleKlasa system provides scalable and simple solution for e-learning. 

## System Users And Features

### Moderator users

Browsable interface allows for listing groups and managing students in a given group.

Moderator might use following features:
- Login using username and password or by using quick login url like http://localhost:8080/l/NAU1
- Login & quick access given group with http://localhost:8080/l/NAU1?g=group-1
- Create or delete group
  Add or delete student within a group
- Reset student personal access link in case it's lost or disclosed
- Create and join new lesson. Starting new lesson will allocate new BBB room and allow all students assigned 
to a group to join active room using their personal links. 


### Student users

For sake of simplicity, in most cases student user will require only a *single* access url.
In order to join active lesson student needs to use his personal link.
Personal student links look as follows:

http://localhost:8080/UCZEN1

### Admin users

Admin users manage moderators access, their able to create/revoke/reset access for moderators.


## Important Concepts

### Creating Groups

Ideally, Student needs only one access url. When creating your class, consider following structure:
- Group represents entity within school / course, grouping students
- Same Entity / Group might have lessons with different teachers and always use the same access url
- **It's best to think about Group as group of people, i.e. "grade 6A" not subject, i.e. "chemistry"**


### Conference Server Allocation

Each new lesson created by moderator allocates room on one of BBB swarm servers.
App implements algorithm for selecting optimal server and balance load.

### Students Active Lesson Routing

Students using their quick access link will land on a latest active room for their group.
Access to a conference room is active only if a room (conference) was previously created by a Moderator.

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
Web App is written in vue.js 


### Sample Data
You can use Makefile command ```reset_db``` to populate sample data into database. Consult Makefile for other useful commands.

