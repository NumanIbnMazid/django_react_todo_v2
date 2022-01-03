FROM python:3.8

# Install curl, node, & yarn
RUN apt-get -y install curl \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash \
    && apt-get install nodejs \
    && curl -o- -L https://yarnpkg.com/install.sh | bash

WORKDIR /app/backend

# Install Python dependencies
COPY ./backend/requirements.txt /app/backend/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Install JS dependencies
WORKDIR /app/frontend

COPY ./frontend/package.json ./frontend/yarn.lock /app/frontend/
RUN $HOME/.yarn/bin/yarn install

# Add the rest of the code
COPY . /app/

# Build static files
RUN $HOME/.yarn/bin/yarn build

# Have to move all static files other than index.html to root/
# for whitenoise middleware
WORKDIR /app/frontend/build

RUN mkdir root && mv *.ico *.js *.json root

# Collect static files
RUN mkdir /app/backend/staticfiles

WORKDIR /app

# SECRET_KEY is only included here to avoid raising an error when generating static files.
# Be sure to add a real SECRET_KEY config variable in Heroku.
RUN DJANGO_SETTINGS_MODULE=config.settings.production \
    SECRET_KEY='django-insecure-#ny22i8ykr7v5&-h0kf*a6vph0(cbkip)or3=pe%k01jz*-@si' \
    DATABASE_URL='postgres://kpidvoyybapdjx:f0421b1054e510e42af9e303f829c5050969f5fee41cc10fe8393ebd8090abf1@ec2-23-21-229-200.compute-1.amazonaws.com:5432/d89kehtsrh6ds2' \
    python3 backend/manage.py collectstatic --noinput

EXPOSE $PORT

CMD python3 backend/manage.py runserver 0.0.0.0:$PORT