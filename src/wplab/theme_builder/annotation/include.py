from wplab.theme_builder.annotation import EmptyAnnotation, add_annotation

NAME = 'include'

class Include(EmptyAnnotation):

    def __init__(self, params):
        if len(params) != 1:
            raise Exception("Include takes exactly one parameter")
        self._snippet = params[0]

    def execute(self):
        with open(self.context.snippet_path(self._snippet), 'r') as snippet_fd:
            for line in snippet_fd:
                self.context.write(line)

def register():
    add_annotation(NAME, Include)
