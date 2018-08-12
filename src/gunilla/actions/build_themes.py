from gunilla.theme_builder import run_builder
from gunilla.workspace import workspace

def run():
    run_builder(workspace().directory)
