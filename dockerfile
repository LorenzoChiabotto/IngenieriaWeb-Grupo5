FROM python:3.8.3

RUN mkdir /webChat
WORKDIR /webChat

COPY . /webChat

RUN pip install -r requirements.txt

ENV EN_DOCKER=True

RUN mkdir /data
COPY db.sqlite3 /data

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]