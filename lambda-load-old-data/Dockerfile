FROM python:latest

RUN mkdir -p /data

COPY requirements.txt .
COPY lambda_load_s3.py .

RUN pip install -r requirements.txt

CMD python3 lambda_load_s3.py

