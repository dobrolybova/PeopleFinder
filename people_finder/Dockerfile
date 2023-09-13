FROM python:3.10

EXPOSE 8080

WORKDIR /people_finder

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY /migration ./migration
COPY alembic.ini alembic.ini
COPY /*.py ./

CMD ["python3", "main.py"]