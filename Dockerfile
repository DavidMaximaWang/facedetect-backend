FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app

COPY / /app

EXPOSE 5000


RUN pip install -r requirements.txt 

RUN cd /app
CMD ["python3", "app.py"]