FROM python:3.8
ENV LOCAL_RUN 0

RUN apt-get update && apt-get install -y \
    python-dev \
    chromium \
    git-core \
    xvfb

ADD ./requirements /app/requirements
RUN pip install -r /app/requirements/base.txt

ADD ./compose/celery/start_celery.sh /app/djangoapps/start_celery.sh

ADD ./djangoapps /app/djangoapps
COPY ./compose/chromedriver /app/chromedriver/
WORKDIR /app/djangoapps

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# COPY . .
CMD ["/bin/sh", "/app/djangoapps/start_celery.sh"]