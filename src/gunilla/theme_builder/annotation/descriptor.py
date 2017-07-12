class AnnotationDescriptor(object):

    def __init__(self, string):
        self.parse(string)

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params

    def parse(self, string):
        open_parenthesis_index= string.find('(')
        if open_parenthesis_index == -1:
            self._name = string
            self._params = []
        else:
            close_parenthesis_index = string.find(')', open_parenthesis_index + 1)
            if close_parenthesis_index != -1:
                self._name = string[0:open_parenthesis_index]
                self._params = string[open_parenthesis_index + 1:close_parenthesis_index].split(',')
            else:
                raise Exception("Bad annotation format: {}".format(string))
