import logging
import os

from gunilla.config import Config
from gunilla.environment import environment
from gunilla.exceptions import WorkspaceException
from gunilla.actions.impl.template_folder import TemplateFolder
import json

logger = logging.getLogger(__name__)


class Workspace(object):

    def __init__(self, workspace_dir):
        self._dir = workspace_dir
        self._config = None

    def is_configured(self):
        return os.path.exists(os.path.join(self._dir, "prototypes")) and \
            os.path.exists(os.path.join(self._dir, "themes")) and \
            os.path.exists(os.path.join(self._dir, "plugins"))

    def config(self):
        if not self._config:
            self._config = self._read_config()
        return self._config

    def _read_config(self):
        config = Config()
        config.read(self.config_file_path())
        return config

    def init(self):
        if self.is_configured() and not environment().force:
            raise WorkspaceException("Project seems to be already set up")

        print("Initializing project {}".format(self.config().project_name))

        project_template_path = environment().project_template_path
        if project_template_path is None:
            self._create_default_dirs()
        else:
            logger.debug("Reading project template from {}".format(project_template_path))
            project_name = self.config().project_name
            project_template = TemplateFolder(project_template_path)
            project_template.copy_to(self._dir)
            self._fix_project_config(project_name)

    def _create_default_dirs(self):
        prototypes_path = os.path.join(self._dir, "prototypes")
        if not os.path.exists(prototypes_path):
            os.mkdir(prototypes_path)
        themes_path = os.path.join(self._dir, "themes")
        if not os.path.exists(themes_path):
            os.mkdir(themes_path)
        plugins_path = os.path.join(self._dir, "plugins")
        if not os.path.exists(plugins_path):
            os.mkdir(plugins_path)

    def _fix_project_config(self, project_name):
        self._read_config()
        self.config().project_name = project_name
        self._write_config()

    def _write_config(self):
        self.config().write(self.config_file_path())

    def change_to_composer_dir(self):
        os.chdir(self._composer_dir_name())

    def prototype_path(self, prototype_name):
        return os.path.join(self._dir, "prototypes", prototype_name)

    def dir_exists(self):
        return os.path.exists(self._dir)

    def init_config_file(self):
        config_map = {}
        config_map["name"] = input("Project name: ")
        with open(self.config_file_path(), 'w') as f:
            json.dump(config_map, f, indent=4)

    def config_file_path(self):
        if environment().workspace:
            return os.path.join(environment().workspace, 'gunilla.json')
        else:
            return 'gunilla.json'

    @property
    def directory(self):
        return self._dir

    def add_prototype(self, prototype_name, prototype):
        self.config().prototypes.add(prototype_name, prototype)
        self._write_config()


_workspace_instance = None


def workspace():
    global _workspace_instance
    if not _workspace_instance:
        if environment().workspace:
            logger.debug("Using workspace %s" % environment().workspace)
            _workspace_instance = Workspace(os.path.abspath(environment().workspace))
        else:
            logger.debug("Using default workspace (current directory)")
            _workspace_instance = Workspace(os.getcwd())
    return _workspace_instance
