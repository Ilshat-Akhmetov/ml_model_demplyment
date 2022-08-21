FROM python:3.9

LABEL test of an ml-model
MAINTAINER username
# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .
# dot point . means current working directory
COPY model_saved.pkl .
COPY pipeline_funcs.py .
COPY main.py .
COPY static/ ./static/
COPY template/ ./template/


# RUN apt-get update
# set -y to say yes when system asks if install libs or not
# RUN apt-get install -y python3-pip
# install dependencies
RUN pip3 install -r requirements.txt


# copy the content of the local src directory to the working directory
# COPY src/ .
# EXPOSE 5000
# command to run on container start
ENTRYPOINT [ "python", "./main.py" ] 
