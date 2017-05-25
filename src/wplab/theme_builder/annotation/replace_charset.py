from wplab.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'replace_charset'

class OpenReplaceCharset(OpenAnnotation):

    def __init__(self, params):
        if len(params) != 0:
            raise Exception("Include takes no parameter")

    @property
    def name(self):
        return NAME

    def open(self):
        self.context.write('<meta charset="<?php bloginfo( \'charset\' ); ?>">')

    def consume(self, line):
        pass

    def close(self):
        pass


class CloseReplaceCharset(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenReplaceCharset)
    add_annotation('/' + NAME, CloseReplaceCharset)
