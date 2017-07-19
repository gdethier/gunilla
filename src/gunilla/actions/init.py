from gunilla.actions.validations import is_configured
from gunilla.config import instance
import os

from gunilla.exceptions import ActionException


COMPOSER_FILE_CONTENT = \
"""
version: '2'

services:
   db:
     image: mysql:5.7
     volumes:
       - db_data:/var/lib/mysql
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: wordpress
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: wordpress

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_PASSWORD: wordpress
volumes:
   db_data:
"""


def _write_composer_file():
    with open(instance().composer_file_name(), 'w') as f:
        f.write(COMPOSER_FILE_CONTENT)


def run():
    if is_configured():
        raise ActionException("Project seems to be already set up")

    print("Initializing project {}".format(instance().project_name))

    os.mkdir("prototypes")
    os.mkdir("themes")
    os.mkdir("plugins")
    os.makedirs(instance().composer_dir_name())
    _write_composer_file()
