import os
import shutil

class TemplateFolder(object):

    def __init__(self, template_path):
        self.template_path = template_path

    def copy_to(self, destination_path):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        for item_name in os.listdir(self.template_path):
            source_item_path = os.path.join(self.template_path, item_name)
            destination_item_path = os.path.join(destination_path, item_name)
            self._copy_item(source_item_path, destination_item_path)

    def _copy_item(self, source_path, destination_path):
        self._clear_destination(destination_path)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)

    def _clear_destination(self, destination_path):
        if os.path.exists(destination_path):
            if os.path.isdir(destination_path):
                shutil.rmtree(destination_path)
            else:
                os.remove(destination_path)
