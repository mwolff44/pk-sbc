FROM python:2.7-jessie

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y \
  # psycopg2 dependencies
  && apt-get install -y build-essential gcc python-dev libssl-dev \
  && apt-get install -y libpq-dev \
  # Pillow dependencies
  && apt-get install -y libjpeg-dev zlib1g-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apt-get install -y libffi-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Import-export dependencies
  && apt-get install -y libxml2-dev libxslt-dev

# Requirements have to be pulled and installed here, otherwise caching won't work
RUN pip install pip-tools
COPY ./requirements /requirements
RUN pip-sync /requirements/dev.txt

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/local/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
