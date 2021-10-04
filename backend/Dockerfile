FROM python:3.6.8

WORKDIR /code/root

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./root /code/root

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
