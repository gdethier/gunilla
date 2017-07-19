from gunilla.config import instance
import json
import os
import requests
import shutil
from zipfile import ZipFile


def download_extract(slug, dependency, descriptor, folder):
    version = dependency.version
    if version == 'latest':
        version = descriptor['version']
        print("Latest version of '{}' is '{}'".format(slug, version))

    download_request = requests.get(descriptor['versions'][version])
    shutil.rmtree('{}/{}'.format(folder, slug), True)
    zip_file_name = '{}/{}.zip'.format(folder, slug)
    with open(zip_file_name, 'w') as fd:
        for chunk in download_request.iter_content(chunk_size=128):
            fd.write(chunk)

    zip_file = ZipFile(zip_file_name)
    zip_file.extractall('{}'.format(folder))
    os.remove(zip_file_name)


def run():
    plugin_dependencies = instance().dependencies.plugins
    for slug in plugin_dependencies:
        dependency = plugin_dependencies[slug]
        version = dependency.version
        print("Downloading plugin '{}' at version '{}'".format(slug, version))

        descriptor = json.loads(requests.get('https://api.wordpress.org/plugins/info/1.0/{}.json'.format(slug)).text)
        download_extract(slug, dependency, descriptor, 'plugins')

    theme_dependencies = instance().dependencies.themes
    for slug in theme_dependencies:
        dependency = theme_dependencies[slug]
        version = dependency.version
        print("Downloading theme '{}' at version '{}'".format(slug, version))

        descriptor = json.loads(requests.get('https://api.wordpress.org/themes/info/1.1/?action=theme_information&request[slug]={}&request[fields][versions]=true'.format(slug)).text)
        download_extract(slug, dependency, descriptor, 'themes')
