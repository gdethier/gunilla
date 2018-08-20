from gunilla.infra import infrastructure
from gunilla.workspace import workspace


def print_howto():
    print("Connect to WP via:")
    print("- http://{}/".format(infrastructure().get_wordpress_container_ip()))
    print("- http://{}/ (you need first to run 'register_host')".format(workspace().config().project_name))
    print("")
    print("Note: If it is the first time you start the project, you might have to wait a few minutes before WP is actually available.")


def run():
    infrastructure().start()
    print_howto()
