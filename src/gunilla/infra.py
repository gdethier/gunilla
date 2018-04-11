import subprocess

from logging import getLogger
from gunilla.docker import wait_wordpress_container
from gunilla.workspace import workspace


logger = getLogger(__name__)


COMPOSER_FILE_CONTENT = \
"""
version: '2'

services:
   db:
     image: mysql:5.7
     volumes:
       - db_data:/var/lib/mysql
     restart: "no"
     environment:
       MYSQL_ROOT_PASSWORD: wordpress
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: wordpress
   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     restart: "no"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_PASSWORD: wordpress

volumes:
   db_data:
"""


class Infrastructure(object):

    def define(self):
        with open(workspace()._composer_file_name(), 'w') as f:
            f.write(COMPOSER_FILE_CONTENT)

    def start(self):
        self._run_composer(['up', '-d'])
        wait_wordpress_container()

    def _run_composer(self, args):
        workspace().change_to_composer_dir()
        command_line = [ 'docker-compose' ]
        command_line.extend(args)
        subprocess.call(command_line)

    def stop(self):
        self._run_composer(['stop'])

    def clear(self):
        self.stop()
        self._run_composer(['down', '-v'])


_instance = None


def infrastructure():
    global _instance
    if not _instance:
        _instance = Infrastructure()
    return _instance
