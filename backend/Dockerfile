FROM python:3.6.8

WORKDIR /code/root

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./root /code/root

EXPOSE 8080

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "-w", "4"]

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]