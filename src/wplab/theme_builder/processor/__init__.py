class Processor(object):

    def process(self, line):
        raise Exception("Processor subclasses must implement process")
