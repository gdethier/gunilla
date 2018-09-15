from logging import getLogger
from gunilla.docker import DockerClient
from gunilla.workspace import workspace
from time import sleep


logger = getLogger(__name__)


class Infrastructure(object):

    def __init__(self):
        self.config = workspace().config()
        self.client = DockerClient()

    def start(self):
        self._create_db_volume()
        self._create_wordpress_volume()
        self._create_network()
        self._create_db_container()
        self._create_wordpress_container()

        self.db_container.start()
        self.wordpress_container.start()

        self._wait_container(self._wordpress_container_name())

    def _create_db_volume(self):
        volume_name = self._db_volume_name()
        self.db_volume = self._create_volume(volume_name)

    def _create_volume(self, volume_name):
        volume = self.client.get_volume(volume_name)
        if volume is None:
            return volume
        else:
            return self.client.create_volume(volume_name)

    def _db_volume_name(self):
        return self._base_name() + "_db_data"

    def _base_name(self):
        return "gunilla_" + self.config.project_name

    def _create_wordpress_volume(self):
        volume_name = self._wordpress_volume_name()
        self.wordpress_volume = self._create_volume(volume_name)

    def _wordpress_volume_name(self):
        return self._base_name() + "_wordpress_data"

    def _create_network(self):
        network_name = self._network_name()
        self.network = self.client.get_network(network_name)
        if self.network is None:
            self.network = self.client.create_network(network_name)

    def _network_name(self):
        return self._base_name() + "_default"

    def _create_db_container(self):
        container_name = self._db_container_name()
        self.db_container = self.client.get_container(container_name)
        if self.db_container is None:
            volumes = {
                self._db_volume_name(): {
                    'bind': '/var/lib/mysql',
                    'mode': 'rw'
                }
            }
            network_name = self._network_name()
            environment= {
                "MYSQL_ROOT_PASSWORD": "wordpress",
                "MYSQL_DATABASE": "wordpress",
                "MYSQL_USER": "wordpress",
                "MYSQL_PASSWORD": "wordpress"
            }
            self.db_container = self.client.create_container(name=container_name,
                                                             image="mysql:5.7",
                                                             volumes=volumes,
                                                             network_name=network_name,
                                                             environment=environment)
            self.network.disconnect(self.db_container)
            self.network.connect(self.db_container,
                                 aliases=["db"])

    def _db_container_name(self):
        return self._base_name() + "_db"

    def _create_wordpress_container(self):
        container_name = self._wordpress_container_name()
        self.wordpress_container = self.client.get_container(container_name)
        if self.wordpress_container is None:
            volumes = {
                self._wordpress_volume_name(): {
                    'bind': '/var/www/html',
                    'mode': 'rw'
                }
            }
            network_name = self._network_name()
            environment= {
                "WORDPRESS_DB_HOST": "db:3306",
                "WORDPRESS_DB_PASSWORD": "wordpress"
            }
            self.wordpress_container = self.client.create_container(name=container_name,
                                                                    image="wordpress:latest",
                                                                    volumes=volumes,
                                                                    network_name=network_name,
                                                                    environment=environment)

    def _wordpress_container_name(self):
        return self._base_name() + "_wordpress"

    def stop(self):
        self._stop_wordpress_container()
        self._stop_db_container()

    def _stop_wordpress_container(self):
        container = self.client.get_container(self._wordpress_container_name())
        if container:
            container.stop()

    def _stop_db_container(self):
        container = self.client.get_container(self._db_container_name())
        if container:
            container.stop()

    def clear(self):
        self.stop()
        self._remove_wordpress_container()
        self._remove_db_container()
        self._remove_network()
        self._remove_db_volume()

    def _remove_wordpress_container(self):
        self.client.remove_container(self._wordpress_container_name())

    def _remove_db_container(self):
        self.client.remove_container(self._db_container_name())

    def _remove_network(self):
        self.client.remove_network(self._network_name())

    def _remove_db_volume(self):
        self.client.remove_network(self._db_volume_name())

    def _wait_container(self, name):
        container = self.client.get_container(name)
        while container is None:
            container = self.client.get_container(name)
            print("Container not yet available, waiting for 3 secs...")
            sleep(3)

    def get_wordpress_container(self):
        return self.client.get_container(self._wordpress_container_name())

    def get_wordpress_container_ip(self):
        container = self.get_wordpress_container()
        if container:
            return container.get_ip(self._network_name())
        else:
            return None

    def clear_volumes(self):
        self.client.remove_volume(self._db_volume_name())
        self.client.remove_volume(self._wordpress_volume_name())


_instance = None


def infrastructure():
    global _instance
    if not _instance:
        _instance = Infrastructure()
    return _instance
