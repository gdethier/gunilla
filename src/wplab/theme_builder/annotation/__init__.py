annotations = {}

def add_annotation(name, annotation_class):
    if name in annotations:
        raise Exception("An annotation with name {} already exists".format(name))
    annotations[name] = annotation_class

def get_annotation(descriptor):
    annotation_class = annotations.get(descriptor.name)
    if not annotation_class:
        raise Exception("Annotation {} does not exist".format(descriptor.name))
    else:
        return annotation_class(descriptor.params)


class Annotation(object):

    def consume(self, line):
        raise Exception("Annotation subclass must define consume method")


class OpenAnnotation(Annotation):

    def is_open(self):
        return True

    def is_empty(self):
        return False

    @property
    def name(self):
        raise Exception("OpenAnnotation subclass must define name property")

    @property
    def closing(self):
        raise Exception("An open annotation does not close anything")

    def open(self):
        raise Exception("OpenAnnotation subclass must define open method")

    def close(self):
        raise Exception("OpenAnnotation subclass must define close method")


class CloseAnnotation(Annotation):

    def __init__(self, params):
        if len(params) > 0:
            raise Exception("Close annotation takes no parameter")

    def is_open(self):
        return False

    def is_empty(self):
        return False

    @property
    def name(self):
        return '/' + self.closing

    def closes(self, annotation):
        if not isinstance(annotation, OpenAnnotation):
            raise Exception("A close annotation can only close an open annotation")
        return annotation.name == self.closing

    @property
    def closing(self):
        raise Exception("Annotation subclass must define closing property")

    def consume(self, line):
        raise Exception("A close annotation cannot consume anything")


class EmptyAnnotation(Annotation):

    def is_open(self):
        return False

    def is_empty(self):
        return True
