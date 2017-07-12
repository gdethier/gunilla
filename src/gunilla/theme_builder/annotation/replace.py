from gunilla.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'replace'

class OpenReplace(OpenAnnotation):

    def __init__(self, params):
        if len(params) != 1:
            raise Exception("Replace takes exactly one parameter")
        self._snippet = params[0]

    @property
    def name(self):
        return NAME

    def open(self):
        with open(self.context.snippet_path(self._snippet), 'r') as snippet_fd:
            for line in snippet_fd:
                self.context.write(line)

    def consume(self, line):
        pass

    def close(self):
        pass


class CloseReplace(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenReplace)
    add_annotation('/' + NAME, CloseReplace)
