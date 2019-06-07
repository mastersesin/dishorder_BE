FROM python:3.7.3-stretch
WORKDIR /code
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN ln -s /usr/lib/apt/methods/http /usr/lib/apt/methods/https
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y unixodbc unixodbc-dev
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]