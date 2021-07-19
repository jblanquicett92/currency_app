FROM python:3.7-alpine
MAINTAINER Jorge Armando Blanquicett Matos

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip3 install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app


EXPOSE 8000

#CMD ["gunicorn", "--bind", ":8000", "app.wsgi:application"]

CMD gunicorn app.wsgi:application --bind 0.0.0.0:$PORT