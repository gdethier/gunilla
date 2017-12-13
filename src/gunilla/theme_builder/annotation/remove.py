from gunilla.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'remove'

class OpenRemove(OpenAnnotation):

    def __init__(self, params):
        if len(params) != 0:
            raise Exception("Remove takes no parameter, got {}".format(len(params)))

    @property
    def name(self):
        return NAME

    def open(self):
        pass

    def consume(self, line):
        pass

    def close(self):
        pass


class CloseRemove(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenRemove)
    add_annotation('/' + NAME, CloseRemove)
