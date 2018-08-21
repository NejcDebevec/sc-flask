# Start with a Python image.
FROM python:3.6

ENV PYTHONUNBUFFERED 1

# Install required packages, remove cache when done
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        nginx \
        supervisor && \
        pip3 install -U pip setuptools && \
        pip3 install -U uwsgi && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

# Copy and install requirements.
ADD ./requirements.txt /code/requirements.txt
RUN pip install -Ur requirements.txt

# setup configs
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Copy config if you want to use nginx with flask
#COPY config/nginx-app.conf /etc/nginx/sites-available/default
COPY config/supervisor-app.conf /etc/supervisor/conf.d/

# copy code and create required config files
COPY . /code/

# Specify the command to run when the image is run.
CMD ["supervisord", "-n"]
