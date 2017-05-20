import os


class Context(object):

    def __init__(self, config):
        self._config = config
        self._output_file = None

    def set_current_output_file(self, name):
        if self._output_file:
            raise Exception("Curren output file ({}) is still open".format(self._current_output_path))
        self._current_output_path = os.path.join(self._config.theme_path, name)
        print("Writing to file {}".format(self._current_output_path))
        self._output_file = open(self._current_output_path, 'w')

    def write(self, line):
        if self._output_file is None:
            raise Exception("No open output file")
        self._output_file.write(line)
        if not line.endswith('\n'):
            self._output_file.write('\n')

    def close_current_output_file(self):
        self._output_file.close()
        self._output_file = None

    def close(self):
        if self._output_file:
            self.close_current_output_file()

    def snippet_path(self, name):
        return os.path.join('snippets', name)
