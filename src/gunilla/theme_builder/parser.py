from gunilla.theme_builder.annotation import get_annotation
from gunilla.theme_builder.annotation.content import register as register_content
from gunilla.theme_builder.annotation.descriptor import AnnotationDescriptor
from gunilla.theme_builder.annotation.footer import register as register_footer
from gunilla.theme_builder.annotation.header import register as register_header
from gunilla.theme_builder.annotation.include import register as register_include
from gunilla.theme_builder.annotation.replace import register as register_replace

from gunilla.theme_builder.annotation.replace_body import register as register_replace_body
from gunilla.theme_builder.annotation.replace_charset import register as register_replace_charset
from gunilla.theme_builder.annotation.replace_html import register as register_replace_html
from gunilla.theme_builder.annotation.wp_footer import register as register_wp_footer
from gunilla.theme_builder.annotation.wp_head import register as register_wp_head
from gunilla.theme_builder.context import Context


register_content()
register_footer()
register_header()
register_include()
register_replace()
register_replace_body()
register_replace_charset()
register_replace_html()
register_wp_footer()
register_wp_head()


class HtmlParser(object):

    def __init__(self, config, html_file):
        self._html_file = html_file
        self._annotation_stack = []
        self._context = Context(config)

    def parse(self):
        with open(self._html_file, 'r') as fd:
            for line in fd:
                new_annotation = self._try_extract_annotation(line)
                if new_annotation:
                    self._handle_new_annotation(new_annotation)
                else:
                    if len(self._annotation_stack) > 0:
                        self._annotation_stack[-1].consume(line)

            self._context.close()

            if len(self._annotation_stack) > 0:
                raise Exception("Some annotations are still open")

    def _handle_new_annotation(self, new_annotation):
        new_annotation.context = self._context
        if new_annotation.is_empty():
            new_annotation.execute()
        elif new_annotation.is_open():
            self._annotation_stack.append(new_annotation)
            new_annotation.open()
        else:
            self._close_current_annotation(new_annotation)

    def _close_current_annotation(self, close_annotation):
        if len(self._annotation_stack) == 0:
            raise Exception("No {} annotation to close".format(close_annotation.closing))
        if close_annotation.closes(self._annotation_stack[-1]):
            closed_annotation = self._annotation_stack.pop()
            closed_annotation.close()
        else:
            raise Exception("Trying to close {} with {}".format(self._annotation_stack[-1].name, close_annotation.closing))

    def _try_extract_annotation(self, line):
        descriptor = self._try_extract_annotation_descriptor(line)
        if descriptor:
            return get_annotation(descriptor)
    
    def _try_extract_annotation_descriptor(self, line):
        annotation_string = self._try_extract_annotation_string(line)
        if annotation_string:
            return AnnotationDescriptor(annotation_string)

    def _try_extract_annotation_string(self, line):
        line = line.strip()
        if line.startswith('<!--') and line.endswith('-->'):
            line = line[4:-3].strip()
            if line.startswith('wplab:'):
                return line[6:]
