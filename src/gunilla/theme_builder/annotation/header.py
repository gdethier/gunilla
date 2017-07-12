from gunilla.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'header'

class OpenHeader(OpenAnnotation):

    def __init__(self, params):
        if len(params) > 0:
            raise Exception("Header takes no parameter")

    @property
    def name(self):
        return NAME

    def open(self):
        self.context.set_current_output_file('header.php')

    def consume(self, line):
        self.context.write(line)

    def close(self):
        self.context.close_current_output_file()


class CloseHeader(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenHeader)
    add_annotation('/' + NAME, CloseHeader)
