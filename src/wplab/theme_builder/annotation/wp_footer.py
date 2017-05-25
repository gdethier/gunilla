from wplab.theme_builder.annotation import EmptyAnnotation, add_annotation

NAME = 'wp_footer'

class WpFooter(EmptyAnnotation):

    def __init__(self, params):
        if len(params) != 0:
            raise Exception("Include takes no parameter")

    def execute(self):
        self.context.write('<?php wp_footer(); ?>')

def register():
    add_annotation(NAME, WpFooter)
