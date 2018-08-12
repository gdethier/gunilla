from gunilla.exceptions import WorkspaceException, ActionException
from gunilla.workspace import workspace
import os
import logging

logger = logging.getLogger(__name__)

def run():
    workspace_directory = workspace().directory
    if not os.path.exists(workspace_directory):
        logger.debug("Creating workspace directory {}".format(workspace_directory))
        os.makedirs(workspace_directory)

    if not os.path.exists(workspace().config_file_path()):
        workspace().init_config_file()

    try:
        workspace().init()
    except WorkspaceException as e:
        raise ActionException(e)
