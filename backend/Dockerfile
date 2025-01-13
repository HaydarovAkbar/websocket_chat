FROM python:3.9-slim

WORKDIR /backend

COPY . .
#COPY ./requirements/requirements.txt .
#RUN pip install -r requirements.txt
RUN pip install daphne
RUN pip install django
RUN pip install channels
RUN pip install channels-redis



EXPOSE 7000

CMD ["daphne", "-b", "0.0.0.0", "-p", "7000", "config.asgi:application"]