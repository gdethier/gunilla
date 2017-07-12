from gunilla.theme_builder.annotation import EmptyAnnotation, add_annotation

NAME = 'wp_head'

class WpHead(EmptyAnnotation):

    def __init__(self, params):
        if len(params) != 0:
            raise Exception("Include takes no parameter")

    def execute(self):
        self.context.write('<?php wp_head(); ?>')

def register():
    add_annotation(NAME, WpHead)
