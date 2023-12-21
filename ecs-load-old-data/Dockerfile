FROM python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m pip install 'boto3-stubs[essential]'

COPY ecs_load_to_s3.py .

CMD python3 ecs_load_to_s3.py

