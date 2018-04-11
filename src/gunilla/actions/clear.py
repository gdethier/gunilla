from gunilla.exceptions import ActionException
from gunilla.infra import infrastructure
from gunilla.workspace import workspace


def run():
    if not workspace().is_configured():
        raise ActionException("Project was not already set up")

    print("!!! WARNING !!!")
    print("Executing this action implies the deletion of all data")
    print("!!! WARNING !!!")
    print("")

    answer = raw_input("Do you really want to clear the project? [Yes,No]")
    if answer == 'Yes':
        infrastructure().clear()
