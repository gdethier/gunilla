from wplab.theme_builder.annotation import OpenAnnotation, CloseAnnotation, add_annotation

NAME = 'content'

class OpenContent(OpenAnnotation):

    def __init__(self, params):
        if len(params) != 1 and len(params) != 2:
            raise Exception("Content takes 1 or 2 parameters, got {}".format(len(params)))

        self._content_file = params[0]
        if len(params) > 1:
            self._template_name = params[1]
        else:
            self._template_name = None


    @property
    def name(self):
        return NAME

    def open(self):
        self.context.set_current_output_file(self._content_file)
        self.context.write('<?php')
        self.context.write('get_header();')
        if self._template_name:
            self._write_template_header()
        self.context.write('?>')

    def _write_template_header(self):
        self.context.write("/*")
        self.context.write("/* Template Name: {}".format(self._template_name))
        self.context.write(" */")

    def consume(self, line):
        self.context.write(line)

    def close(self):
        self.context.write('<?php')
        self.context.write('get_footer();')
        self.context.write('?>')
        self.context.close_current_output_file()


class CloseContent(CloseAnnotation):

    @property
    def closing(self):
        return NAME

def register():
    add_annotation(NAME, OpenContent)
    add_annotation('/' + NAME, CloseContent)
