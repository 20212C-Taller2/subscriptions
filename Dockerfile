FROM python:3.8
WORKDIR /code
COPY ./requirements.txt ./alembic.ini /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./alembic /code/alembic
COPY ./app /code/app
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
