from gunilla.actions.validations import is_configured
from gunilla.exceptions import ActionException
from gunilla.actions.impl.docker_composer_actions import Clear

def run():
    if not is_configured():
        raise ActionException("Project was not already set up")

    print("!!! WARNING !!!")
    print("Executing this action implies the deletion of all data")
    print("!!! WARNING !!!")
    print("")

    answer = raw_input("Do you really want to clear the project? [Yes,No]")
    if answer == 'Yes':
        Clear().run()
