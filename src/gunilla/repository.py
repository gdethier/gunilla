import os
import shutil

class Repository(object):

    def __init__(self):
        self.base_dir = os.path.join(os.path.expanduser('~'), '.gunilla', 'repository')

    def exists(self, path_segments):
        return os.path.exists(self._file_path(path_segments))
    
    def _file_path(self, path_segments):
        return os.path.join(self.base_dir, *path_segments)

    def open(self, path_segments, binary=True):
        return open(self._file_path(path_segments), 'rb' if binary else 'r')

    def add(self, path_segments, external_file_path):
        repository_file_path = self._file_path(path_segments)
        os.makedirs(os.path.dirname(repository_file_path))
        shutil.copy(external_file_path, repository_file_path)

repository = None

def instance():
    global repository
    if repository is None:
        repository = Repository()
    return repository
