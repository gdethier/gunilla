import os
from gunilla.theme_builder.processor.end_of_line_fixer import EndOfLineFixer
from gunilla.theme_builder.processor.link_processor import LinkProcessor


class Context(object):

    def __init__(self, config):
        self._config = config
        self._output_file = None
        self._init_processor_chain()

    def _init_processor_chain(self):
        self._processor_chain = []
        self._processor_chain.append(LinkProcessor())
        self._processor_chain.append(EndOfLineFixer())

    def set_current_output_file(self, name):
        if self._output_file:
            raise Exception("Curren output file ({}) is still open".format(self._current_output_path))
        self._current_output_path = os.path.join(self._config.theme_path, name)
        print("Writing to file {}".format(self._current_output_path))
        self._output_file = open(self._current_output_path, 'w')

    def write(self, line):
        if self._output_file is None:
            raise Exception("No open output file")
        self._output_file.write(self._apply_processor_chain(line))

    def _apply_processor_chain(self, line):
        for processor in self._processor_chain:
            line = processor.process(line)
            if line is None:
                raise Exception("Processor {} returned None".format(processor))
        return line

    def close_current_output_file(self):
        self._output_file.close()
        self._output_file = None

    def close(self):
        if self._output_file:
            self.close_current_output_file()

    def snippet_path(self, name):
        return os.path.join('snippets', name)
