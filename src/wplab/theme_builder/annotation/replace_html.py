from wplab.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'replace_html'

class OpenReplaceHtml(OpenAnnotation):

    def __init__(self, params):
        if len(params) != 0:
            raise Exception("Include takes no parameter")

    @property
    def name(self):
        return NAME

    def open(self):
        self.context.write('<html <?php language_attributes(); ?>>')

    def consume(self, line):
        pass

    def close(self):
        pass


class CloseReplaceHtml(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenReplaceHtml)
    add_annotation('/' + NAME, CloseReplaceHtml)
