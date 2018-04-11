from gunilla.docker import print_howto
from gunilla.infra import infrastructure

def run():
    infrastructure().start()
    print_howto()
