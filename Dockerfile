FROM python:3.6.5-alpine

WORKDIR /app
COPY app/ /app

RUN pip install -r requirements.txt

EXPOSE 34567

ENTRYPOINT ["python", "server.py"]