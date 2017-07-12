from gunilla.theme_builder.processor import Processor


class EndOfLineFixer(Processor):

    def process(self, line):
        if not line.endswith('\n'):
            return line + '\n'
        else:
            return line
