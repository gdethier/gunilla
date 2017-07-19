from gunilla.config import instance
import os

def is_configured():
    return os.path.exists(instance().composer_file_name())
