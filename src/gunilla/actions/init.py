from gunilla.config import config_file_path as config_file_path_function, init_config_file
from gunilla.exceptions import WorkspaceException, ActionException
from gunilla.workspace import instance
import os
import logging

logger = logging.getLogger(__name__)

def run():
    config_file_path = config_file_path_function()

    config_file_dir = os.path.dirname(config_file_path)
    if not os.path.exists(config_file_dir):
        logger.debug("Creating workspace directory {}".format(config_file_dir))
        os.makedirs(config_file_dir)

    if not os.path.exists(config_file_path):
        init_config_file()

    try:
        instance().init()
    except WorkspaceException as e:
        raise ActionException(e)
