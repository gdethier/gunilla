from gunilla.config import DependencyType
from gunilla.environment import environment
from gunilla.exceptions import ActionException
from gunilla.repository import instance as repo_instance
from gunilla.workspace import workspace
import json
import os
import requests
import shutil
from zipfile import ZipFile
import tempfile

repository = repo_instance()

def run():
    os.chdir(workspace().directory)
    plugin_dependencies = workspace().config().dependencies.plugins
    copy_dependencies(plugin_dependencies, 'https://api.wordpress.org/plugins/info/1.0/{}.json', 'plugins')

    theme_dependencies = workspace().config().dependencies.themes
    copy_dependencies(theme_dependencies, 'https://api.wordpress.org/themes/info/1.1/?action=theme_information&request[slug]={}&request[fields][versions]=true', 'themes')


def copy_dependencies(dependencies, url_template, folder):
    for slug in dependencies:
        dependency = dependencies[slug]
        if dependency.type == DependencyType.DOWNLOAD:
            download_dependency(dependencies, slug, url_template, folder)
        elif dependency.type == DependencyType.FOLDER:
            copy_folder_dependency(dependencies, slug, folder)
        else:
            print("Skipping dependency {}".format(slug))


def download_dependency(dependencies, slug, url_template, folder):
    dependency = dependencies[slug]
    version = dependency.version
    print("Downloading plugin '{}' at version '{}'".format(slug, version))

    if version != 'latest':
        path_segments = [folder, slug, version, '%s-%s.zip' % (slug, version)]
        if repository.exists(path_segments):
            extract(path_segments, folder)
            return

    descriptor = json.loads(requests.get(url_template.format(slug)).text)
    if environment().debug:
        print("Downloaded descriptor: %s" % json.dumps(descriptor, indent=2))
    download_extract(slug, dependency, descriptor, folder)


def download_extract(slug, dependency, descriptor, folder):
    version = dependency.version
    if version == 'latest':
        version = descriptor['version']
        print("Latest version of '{}' is '{}'".format(slug, version))

    if version not in descriptor['versions']:
        print("Version {} does not seem to be available".format(version))
        print("Available versions are:")
        sorted_versions = []
        for key in descriptor['versions']:
            sorted_versions.append(key)
        sorted_versions.sort()
        for version in sorted_versions:
            print(version)
        raise ActionException("Provided version is not available")

    path_segments = [folder, slug, version, '%s-%s.zip' % (slug, version)]
    if not repository.exists(path_segments):
        download_request = requests.get(descriptor['versions'][version])
        file_handle, path = tempfile.mkstemp()
        with os.fdopen(file_handle, 'w') as file_object:
            for chunk in download_request.iter_content(chunk_size=128):
                file_object.write(chunk)
        repository.add(path_segments, path)
        os.remove(path)
    else:
        print("Found in local repository")

    extract(path_segments, folder)

def extract(path_segments, folder):
    with repository.open(path_segments) as f:
        zip_file = ZipFile(f)
        zip_file.extractall('{}'.format(folder))

def copy_folder_dependency(dependencies, slug, folder):
    dependency = dependencies[slug]
    src_folder = dependency['path']
    dest_folder = os.path.join(folder, slug)

    print("Copying plugin '{}' files from folder '{}'".format(slug, src_folder))
    shutil.rmtree(dest_folder, True)
    shutil.copytree(src_folder, dest_folder, True, None)
