from importlib import resources
from pathlib import Path
from shutil import copy, copytree
from subprocess import call
from sys import argv
from textwrap import dedent
from tomllib import load

from pybrary import Rex

import plantree


config = plantree.config
root = resources.files(plantree) / '../projects'


def usage():
    cmd = argv[0].split('/')[-1]
    projects = '\n    '.join(get_projects().keys())
    print(dedent(f'''
        {cmd} config
            Edit config.

        {cmd} [name]
            Create project tree NAME.

    Projects:
        {projects}
    '''))


def get_projects():
    projects = {
        p.name: p.resolve()
        for p in root.glob('*')
        if p.is_dir()
    }
    return projects


def replace(txt, replacements):
    changed = txt
    for rex, value in replacements:
        if rex.find(changed):
            changed = rex.replace(value, changed)
    return changed != txt and changed


def rename(path, replacements):
    if renamed := replace(path.name, replacements):
        print('rename', path)
        path.rename(path.with_name(renamed))
        return True
    return False


def edit_file(path, replacements):
    try:
        txt = path.read_text()
    except Exception as x:
        print(f'\nread {path} ! {x}\n')
        return

    if changed := replace(txt, replacements):
        print('edit', path)
        with open(path, 'w') as out:
            out.write(changed)


def rename_dirs(root, replacements):
    go = True
    while go:
        go = False
        for path, dirs, files in root.walk():
            for d in dirs:
                go = go or rename(path / d, replacements)


def rename_files(root, replacements):
    for path, dirs, files in root.walk():
        for f in files:
            rename(path / f, replacements)


def edit_files(root, replacements):
    for path, dirs, files in root.walk():
        for f in files:
            edit_file(path / f, replacements)


def apply_config(name):
    cfg = config.config
    replacements = {
        (Rex(fr'(?<!_)_{key.upper()}_(?!_)'), value)
        for key, value in cfg.fields.items()
    }
    root = Path(name).rename(cfg.fields.name)
    rename_dirs(root, replacements)
    rename_files(root, replacements)
    edit_files(root, replacements)


def plant(name):
    print(f"\nInit {name}\n")
    path = get_projects()[name]
    config.edit()
    copytree(path, name)
    apply_config(name)


def main():
    match argv[1:]:
        case ['config']:
            config.edit()
        case ['help']:
            usage()
        case [name]:
            if get_projects().get(name):
                plant(name)
            else:
                usage()
        case []:
            plant('default')
