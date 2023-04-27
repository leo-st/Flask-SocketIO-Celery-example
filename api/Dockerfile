# pull official base image
FROM python:3.10.5-bullseye

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc netcat

# install python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --requirement /requirements.txt

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN groupadd -g 1000 app
RUN useradd -m -u 1000 -g 1000 app


# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/api/


# copy project
# COPY . $HOME

COPY ./code $HOME/code
COPY ./api $HOME/api

RUN mkdir $HOME/data/ 
RUN mkdir $HOME/data/logs 

WORKDIR $APP_HOME 


# chown all the files to the app user
RUN chown -R app:app $HOME
# RUN dos2unix $APP_HOME


# change to the app user
USER app

# run entrypoint.sh
 ENTRYPOINT ["sh", "/home/app/api/entrypoint.sh"]