FROM python:3.8.2-alpine3.10

RUN adduser -D bulletin

WORKDIR /home/bulletin

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY bulletin bulletin
COPY manage.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP manage.py
ENV SECRET_KEY djdpod;flbmdl!kte23flmdolg.32pokrge#rr32

RUN chown -R bulletin:bulletin ./
USER bulletin

EXPOSE 5100
ENTRYPOINT ["./boot.sh"]