FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip install --upgrade pip

# COPY ./app /app
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt