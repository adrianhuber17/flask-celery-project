FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#update Linux Advanced Package Tool
RUN apt-get update \
  # dependencies for building Python packages
  #install build-essentials required to compile software
  && apt-get install -y build-essential \
  # install psycopg2 dependencies to query postgresql
  && apt-get install -y libpq-dev \
  # Additional dependencies
  # install telnet to connect to a remote host
  # install netcat to allow for port listening and transfering of files across networked systems
  && apt-get install -y telnet netcat \
  # cleaning up unused files that are cached in the /var/lib/apt/lists/*
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#sed -i 's/\r$//g' will change all line endings in
#shell sctipts to convert from windows line endings to UNIX
#COPY the shell commands to the root directory of the final image
#use chmod +x to make file executable
COPY ./compose/local/flask/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/flask/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/flask/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/flask/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

WORKDIR /app

ENTRYPOINT ["/entrypoint"]