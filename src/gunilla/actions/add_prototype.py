from gunilla.config import instance as config_instance, Prototype
from gunilla.environment import instance as environment_instance
import os
import json
from gunilla.actions.impl.template_folder import TemplateFolder

def run():
    prototype_name = environment_instance().prototype_name
    print("Adding prototype %s" % prototype_name)

    prototype_template_path = environment_instance().prototype_template_path
    prototype_template = TemplateFolder(prototype_template_path)
    prototype_path = os.path.join('prototypes', prototype_name)
    prototype_template.copy_to(prototype_path)

    prototype_data_path = os.path.join(prototype_template_path, 'gunilla-prototype.json')
    if not os.path.exists(prototype_data_path):
        raise Exception("%s does not contain a valid prototype template, missing 'gunilla-prototype.json'")

    os.remove(os.path.join(prototype_path, 'gunilla-prototype.json'))

    with open(prototype_data_path, 'r') as f:
        prototype_data = json.load(f)
        prototype = Prototype(prototype_data)
        config_instance().prototypes.add(prototype_name, prototype)
        config_instance().write()
