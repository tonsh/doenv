FROM python:3.12-bullseye

WORKDIR /app

RUN pip install ipython

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
COPY .env.pro .env

ENV APP_NAME=doenv
ENV APP_PATH=/app/$APP_NAME
ENV PYTHONPATH=$PYTHONPATH:$APP_PATH/$APP_NAME

# EXPOSE 8000

CMD ["make", "lint"]
