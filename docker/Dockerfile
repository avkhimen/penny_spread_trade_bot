FROM python:3.10-slim

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

WORKDIR /home/jovyan/app

CMD ["python", "main.py"]