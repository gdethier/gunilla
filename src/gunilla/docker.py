from __future__ import absolute_import
import docker
from docker.errors import NotFound
from gunilla.config import instance
from time import sleep


def get_wordpress_container():
    client = docker.from_env(version='auto')
    return client.containers.get(instance().wordpress_container_name())

def get_wordpress_container_ip():
    container = get_wordpress_container()
    return container.attrs['NetworkSettings']['Networks']['{}_default'.format(instance().container_base_name())]['IPAddress']

def wait_wordpress_container():
    while True:
        try:
            return get_wordpress_container()
        except NotFound:
            print("Container not yet available, waiting for 3 secs...")
            sleep(3)

def print_howto():
    print("Connect to WP via:")
    print("- http://{}/".format(get_wordpress_container_ip()))
    print("- http://{}/ (you need first to run 'register_host')".format(instance().project_name))
    print("")
    print("Note: If it is the first time you start the project, you might have to wait a few minutes before WP is actually available.")
