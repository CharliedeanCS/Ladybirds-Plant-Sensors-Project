FROM python:latest

RUN mkdir -p /data

COPY requirements.txt .
COPY install_sql.sh .
COPY lambda_load_s3.py .

RUN pip3 install -r requirements.txt
RUN bash install_sql.sh

CMD python3 lambda_load_s3.py

