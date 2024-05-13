
#every docker instruction creates a new image layer
# optimizing the docker file to use cache layer  will significantly decrease build t#time of image
# base image contains all the necessary dependencies to run the python application
FROM python:3.10-slim-bullseye

# install os dependencies && avoid unnecessary packages && avoid extra space for cac# hing, 
RUN apt-get update && \
  apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential \
  default-libmysqlclient-dev \
  libssl-dev \
  libffi-dev \
  libpq-dev \
  pkg-config && \
  pip install --no-cache-dir --upgrade pip

# /app directory is working directory for container
WORKDIR /app

# copies the code from host machine to container /app directory 
COPY ./requirements.txt /app

RUN pip install --no-cache-dir --requirement /app/requirements.txt

# currently directory where we run docker build command in 
# copies the entire code from current directory into app folder
COPY . /app

#our app listen to port 5000
EXPOSE 5000

# default command to run when container starts
CMD ["python3", "server.py"]

