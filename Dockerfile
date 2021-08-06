FROM docker.io/library/python:alpine

RUN apk update \
    && apk upgrade

RUN pip install \
    bottle \
    paste \
    requests

RUN adduser -H -D web

WORKDIR "/srv/shortener_frontend/"

COPY index.html index.html
COPY robots.txt robots.txt
COPY server.py server.py
COPY static static/.

RUN chown -R web:web /srv/shortener_frontend/
RUN chmod 0550 -R /srv/shortener_frontend/ \
    && chmod 0440 /srv/shortener_frontend/*.html \
    && chmod 0440 /srv/shortener_frontend/static/css/*.css \
    && chmod 0440 /srv/shortener_frontend/static/css/theme/*.css \
    && chmod 0440 /srv/shortener_frontend/static/js/*.js

EXPOSE 8080

USER web:web
ENTRYPOINT ["python", "server.py"]
