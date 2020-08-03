FROM python:3.8
ENV LOCAL_RUN 0

RUN apt-get update && apt-get upgrade -y && apt-get install -y

ADD ./requirements /app/requirements
RUN pip install -r /app/requirements/base.txt

ADD ./compose/celery_beat/start_celery_beat.sh /app/djangoapps/start_celery_beat.sh

ADD ./djangoapps /app/djangoapps
COPY ./compose/chromedriver /app/chromedriver/

WORKDIR /app/djangoapps

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# COPY . .
CMD ["/bin/sh", "/app/djangoapps/start_celery_beat.sh"]