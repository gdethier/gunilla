import logging
from gunilla.exceptions import ActionException
import os
import subprocess
from gunilla.infra import infrastructure

logger = logging.getLogger(__name__)


class ContainerFileAction(object):

    def run(self):
        container = infrastructure().get_wordpress_container()
        if not container:
            raise ActionException("This WP project must first be started")
        self.run_with_container()

    def copy_to_container(self, local_path, container_path, owner = None):
        self.docker_exec(['cp', local_path, '{}:{}'.format(infrastructure().get_wordpress_container().id, container_path)])
        if owner:
            self.exec_on_container(['chown', '-R', '{}:{}'.format(owner, owner), container_path])

    def copy_from_container(self, container_path, local_path):
        self.docker_exec(['cp', '{}:{}'.format(infrastructure().get_wordpress_container().id, container_path), local_path])

    def exec_on_container(self, command_line):
        full_command_line = ['exec', '{}'.format(infrastructure().get_wordpress_container().id)]
        full_command_line.extend(command_line)
        self.docker_exec(full_command_line)

    def docker_exec(self, args):
        command_line = ['docker']
        command_line.extend(args)
        subprocess.call(command_line)

    def run_on_container(self, local_script, remote_script):
        self.copy_to_container(local_script, remote_script)
        self.exec_on_container(['chmod', 'a+rx', remote_script])
        self.exec_on_container(['/bin/sh', '-c', remote_script])


class Install(ContainerFileAction):

    def run_with_container(self):
        self.copy_components('themes')
        self.copy_components('plugins')

    def copy_components(self, component_type):
        if os.path.isdir(component_type):
            self.copy_to_container('{}/.'.format(component_type), '/var/www/html/wp-content/{}/'.format(component_type), 'www-data')
        else:
            logger.debug("%s is not a component dir" % os.path.abspath(component_type))


class Uninstall(ContainerFileAction):

    def run_with_container(self):
        self.remove_components('themes')
        self.remove_components('plugins')

    def remove_components(self, component_type):
        if os.path.isdir(component_type):
            for dir_item in os.listdir('{}'.format(component_type)):
                self.docker_exec(['exec', '{}'.format(infrastructure().get_wordpress_container().id), 'rm', '-rf', '/var/www/html/wp-content/{}/{}'.format(component_type, dir_item)])


ENABLE_MULTISITE_SCRIPT = \
"""
# Below command inspired by https://github.com/docker-library/wordpress/issues/195#issuecomment-271382403
sed -r -e 's/\\r$//' /var/www/html/wp-config.php | awk '/^\/\*.*stop editing.*\*\/$/ { print("define( \\"WP_ALLOW_MULTISITE\\", true );") } { print }' > temp.php
chown --reference /var/www/html/wp-config.php temp.php
mv temp.php /var/www/html/wp-config.php
"""

class EnableMultisite(ContainerFileAction):

    def run_with_container(self):
        script_file = '/tmp/enable_multisite.sh'
        with open(script_file, 'w') as f:
            f.write(ENABLE_MULTISITE_SCRIPT)
        self.run_on_container(script_file, script_file)


class CompleteMultisite(ContainerFileAction):

    def run_with_container(self):
        self.edit_config()
        self.edit_htaccess()

    def edit_config(self):
        config_file = '/var/www/html/wp-config.php'
        temp_file = '/tmp/wp-config.php'
        self.edit_file(config_file, temp_file)

    def edit_file(self, remote_file, temp_file):
        self.copy_from_container(remote_file, temp_file)
        subprocess.call(['vim', temp_file])
        self.copy_to_container(temp_file, remote_file)

    def edit_htaccess(self):
        htaccess_file = '/var/www/html/.htaccess'
        temp_file = '/tmp/wp-config.php'
        self.edit_file(htaccess_file, temp_file)
