FROM python:3.10

EXPOSE 8000

WORKDIR /id_generator

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY /client ./client
COPY /metrics ./metrics
COPY /*.py ./

CMD ["python3", "main.py"]