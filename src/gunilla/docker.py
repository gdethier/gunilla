from __future__ import absolute_import
from logging import getLogger
import docker
from docker.errors import NotFound


logger = getLogger(__name__)


class DockerClient(object):

    def __init__(self):
        self._client = docker.from_env(version='auto')

    def get_container(self, name):
        try:
            return Container(self._client.containers.get(name))
        except NotFound:
            return None

    def create_container(self, name=None, image=None, volumes=None, network_name=None, environment={}, ports={}):
        restart_policy = {
            "Name": "no",
            "MaximumRetryCount": 0
        }
        container = self._client.containers.create(image, name=name,
                                                   volumes=volumes,
                                                   network=network_name,
                                                   ports=ports,
                                                   environment=environment,
                                                   restart_policy=restart_policy)
        return Container(container)

    def remove_container(self, name):
        container = self.get_container(name)
        if container:
            container.remove()

    def get_volume(self, name):
        volumes = self._client.volumes.list(filters={"name": name})
        if len(volumes) > 0:
            return Volume(volumes[0])

    def create_volume(self, name):
        volume = self._client.volumes.create(name=name)
        return Volume(volume)

    def get_network(self, name):
        networks = self._client.networks.list(names=[name])
        if len(networks) > 0:
            return Network(networks[0])
    
    def create_network(self, name):
        network = self._client.networks.create(name=name)
        return Network(network)

    def remove_network(self, name):
        network = self.get_network(name)
        if network:
            network.remove()

    def remove_volume(self, name):
        volume = self.get_volume(name)
        if volume:
            volume.remove()


class Container(object):

    def __init__(self, container):
        self._container = container

    def get_ip(self, network_name):
        return self._container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']

    def start(self):
        self._container.start()

    def stop(self):
        self._container.stop()

    def remove(self):
        self._container.remove(v=True)

    @property
    def id(self):
        return self._container.id


class Volume(object):

    def __init__(self, volume):
        self._volume = volume

    def remove(self):
        self._volume.remove()


class Network(object):

    def __init__(self, network):
        self._network = network

    def remove(self):
        self._network.remove()

    def disconnect(self, container):
        self._network.disconnect(container._container)

    def connect(self, container, aliases=[]):
        self._network.connect(container._container,
                                 aliases=aliases)

