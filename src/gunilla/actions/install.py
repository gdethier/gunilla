from gunilla.actions.impl.container_file_actions import Install
from gunilla.workspace import workspace
import os

def run():
    os.chdir(workspace().directory)
    Install().run()
