from gunilla.config import instance as config_instance
from gunilla.environment import instance as env_instance
from gunilla.exceptions import WorkspaceException
import os


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
     restart: "no"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_PASSWORD: wordpress

volumes:
   db_data:
"""


class Workspace(object):

    def __init__(self, workspace_dir):
        self._dir = workspace_dir

    def is_configured(self):
        return os.path.exists(self._composer_file_name())
    
    def _composer_file_name(self):
        return os.path.join(self._composer_dir_name(), "docker-compose.yml")

    def _composer_dir_name(self):
        return os.path.join(self._dir, "gunilla", config_instance().project_name)

    def init(self):
        if self.is_configured() and not env_instance().force:
            raise WorkspaceException("Project seems to be already set up")

        print("Initializing project {}".format(config_instance().project_name))

        if not os.path.exists("prototypes"):
            os.mkdir("prototypes")
        if not os.path.exists("themes"):
            os.mkdir("themes")
        if not os.path.exists("plugins"):
            os.mkdir("plugins")

        if not os.path.exists(self._composer_dir_name()):
            os.makedirs(self._composer_dir_name())

        self._write_composer_file()

    def _write_composer_file(self):
        with open(self._composer_file_name(), 'w') as f:
            f.write(COMPOSER_FILE_CONTENT)

    def change_to_composer_dir(self):
        os.chdir(self._composer_dir_name())


_workspace_instance = None

def instance():
    global _workspace_instance
    if not _workspace_instance:
        _workspace_instance = Workspace(os.getcwd())
    return _workspace_instance
