FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app

COPY key.json /app
COPY app.py  /app
COPY project  /app
COPY predict_image_classification_tom.py  /app
COPY requirements.txt /app

EXPOSE 5000


RUN pip install -r requirements.txt 

RUN cd /app
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"
CMD ["python3", "app.py"]