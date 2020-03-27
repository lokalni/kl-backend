FROM python:3.7

RUN apt-get update && apt-get install -y \
       bash \
       dumb-init \
       gcc \
       make \
       postgresql \
       python3-dev \
   && pip install uwsgi

# Instal requirements and add code - use docker cache
COPY /requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . code
WORKDIR code

RUN DJ_SECRET_KEY=build_time DJ_DATABASES_DEFAULT_URL=postgresql://localhost/dummy DJ_ALLOWED_HOSTS=localhost python manage.py collectstatic --noinput

# Declare late to use as much cache as possible
ARG BUILD_COMMIT_SHA
ENV BUILD_COMMIT_SHA ${BUILD_COMMIT_SHA:-}

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uwsgi", "--ini", "uwsgi.ini"]
