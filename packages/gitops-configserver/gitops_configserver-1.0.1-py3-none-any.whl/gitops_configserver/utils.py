from datetime import datetime, timezone
from os import makedirs, path
from shutil import rmtree, copyfile
from yaml import safe_load


def create_dir(path):
    makedirs(path, exist_ok=True)


def file_exists(fname):
    return path.isfile(fname)


def read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()


def write_to_file(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)


def remove_dir_with_content(dirpath):
    rmtree(dirpath, ignore_errors=True)


def load_yaml(filepath):
    with open(filepath, "r") as f:
        return safe_load(f.read())


def copy_file(src, dst):
    copyfile(src, dst)


def timestamp():
    return datetime.now(timezone.utc).isoformat()
