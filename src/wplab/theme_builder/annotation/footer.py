from wplab.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'footer'

class OpenFooter(OpenAnnotation):

    def __init__(self, params):
        if len(params) > 0:
            raise Exception("Header takes no parameter")

    @property
    def name(self):
        return NAME

    def open(self):
        self.context.set_current_output_file('footer.php')

    def consume(self, line):
        self.context.write(line)

    def close(self):
        self.context.close_current_output_file()


class CloseFooter(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenFooter)
    add_annotation('/' + NAME, CloseFooter)
