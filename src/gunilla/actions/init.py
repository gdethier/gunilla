from gunilla.config import config_file_path, init_config_file
from gunilla.exceptions import WorkspaceException, ActionException
from gunilla.workspace import instance
import os


def run():
    if not os.path.exists(config_file_path):
        init_config_file()

    try:
        instance().init()
    except WorkspaceException as e:
        raise ActionException(e)
