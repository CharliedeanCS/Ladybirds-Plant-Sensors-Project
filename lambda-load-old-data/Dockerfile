FROM python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m pip install 'boto3-stubs[essential]'

COPY lambda_load_s3.py .

CMD python3 lambda_load_s3.py

