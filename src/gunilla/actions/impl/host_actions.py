from gunilla.config import instance
from gunilla.docker import get_wordpress_container_ip
from gunilla.exceptions import ActionException
import shutil
import time


class HostAction(object):
    
    def __init__(self):
        self.host_file = '/etc/hosts'

    def host_registered(self):
        with open(self.host_file) as f:
            line = f.readline()
            while line:
                if instance().project_name in line:
                    return True
                line = f.readline()
        return False

    def backup(self):
        backup_file = '/tmp/hosts.backup.' + str(int(round(time.time() * 1000)))
        shutil.copy(self.host_file, backup_file)

    def run(self):
        self._validate()
        self.backup()
        self._run_after_backup()

    def temp_file(self):
        return '/tmp/hosts.' + str(int(round(time.time() * 1000)))

    def deregister(self):
        temp_file = self.temp_file()
        with open(temp_file, 'w') as f:
            with open(self.host_file) as host_file:
                for line in host_file:
                    if not instance().project_name in line:
                        f.write(line)
        shutil.move(temp_file, self.host_file)

    def register(self, ip_address):
        if not ip_address:
            raise ActionException("No IP address detected")
        temp_file = self.temp_file()
        with open(temp_file, 'w') as f:
            with open(self.host_file) as host_file:
                for line in host_file:
                    f.write(line)
            f.write('{}\t{}\n'.format(ip_address, instance().project_name))
        shutil.move(temp_file, self.host_file)


class RegisterHost(HostAction):

    def _validate(self):
        if self.host_registered():
            raise ActionException("Host '{}' is already registered".format(instance().project_name))

    def _run_after_backup(self):
        ip_address = get_wordpress_container_ip()
        self.register(ip_address)


class DeregisterHost(HostAction):
    
    def _validate(self):
        if not self.host_registered():
            raise ActionException("Host '{}' was not registered".format(instance().project_name))

    def _run_after_backup(self):
        self.deregister()


class ReregisterHost(HostAction):

    def _validate(self):
        if not self.host_registered():
            raise ActionException("Host '{}' was not registered".format(instance().project_name))

    def _run_after_backup(self):
        ip_address = get_wordpress_container_ip()
        self.deregister()
        self.register(ip_address)
