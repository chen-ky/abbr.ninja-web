FROM docker.io/library/python:alpine

ARG GIT_HASH="Unknown"

RUN apk update \
    && apk upgrade

RUN adduser -H -D web

WORKDIR "/srv/shortener_frontend/"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .
COPY static static/.
COPY templates templates/.

RUN chown -R web:web /srv/shortener_frontend/ \
    && chmod 0550 -R /srv/shortener_frontend/ \
    && chmod 0440 /srv/shortener_frontend/static/css/*.css \
    && chmod 0440 /srv/shortener_frontend/static/css/theme/*.css \
    && chmod 0440 /srv/shortener_frontend/static/js/*.js \
    && chmod 0440 /srv/shortener_frontend/static/*.html \
    && chmod 0440 /srv/shortener_frontend/static/*.txt

EXPOSE 8080
USER web:web

ENV API_BASE_URL="http://127.0.0.1:8081/api/v1"
ENV HOST="0.0.0.0"
ENV PORT="8080"
ENV SENTRY_RELEASE=${GIT_HASH}
CMD ["python", "server.py"]
