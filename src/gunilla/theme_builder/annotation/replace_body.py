from gunilla.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'replace_body'

class OpenReplaceBody(OpenAnnotation):

    def __init__(self, params):
        if len(params) != 0:
            raise Exception("Include takes no parameter")

    @property
    def name(self):
        return NAME

    def open(self):
        self.context.write('<body <?php body_class(); ?>>')

    def consume(self, line):
        pass

    def close(self):
        pass


class CloseReplaceBody(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenReplaceBody)
    add_annotation('/' + NAME, CloseReplaceBody)
