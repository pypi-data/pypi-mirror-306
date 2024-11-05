import click
import os
import yaml
from yaml import SafeDumper

SafeDumper.add_representer(
    type(None),
    lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:null", ""),
)


compose_file_disclaimer = """
#####
# This file is an example docker-compose file for deploying BLIS to a cloud provider
# This file is used as a template, but will be rewritten by the BLIS tool as necessary.

"""


def basedir():
    return os.path.expanduser("~/.blis")


def make_basedir():
    if not os.path.exists(basedir()):
        os.makedirs(basedir())


def compose_file():
    return os.path.join(basedir(), "docker-compose.yml")


def validate_compose():
    if not os.path.exists(compose_file()):
        return False

    dcmp = _open_compose()
    if dcmp is None:
        return False

    if "name" not in dcmp:
        click.echo("Missing 'name' in docker-compose.yml", err=True)
        return False

    return True


def _open_compose():
    try:
        with open(compose_file(), "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None
    except yaml.YAMLError as e:
        click.echo(e, err=True)
        return None


def _save_compose(contents):
    try:
        with open(compose_file(), "w") as f:
            f.write(compose_file_disclaimer)
            yaml.safe_dump(contents, f)
    except Exception as e:
        click.secho(e, err=True)
        return False
    return True


def _load_template_yml():
    try:
        with open(f"{os.path.dirname(__file__)}/../extra/docker-compose.yml", "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        click.secho(e, err=True)
        return None


def compose_key(key: str, contents=None):
    if contents is None:
        contents = _open_compose()
        if contents is None:
            return None

    keys = key.split(".")
    val = contents
    for k in keys:
        if k not in val:
            return None
        val = val[k]

    return val


def add_volume(volname, opts=None):
    if compose_key(f"volumes.{volname}"):
        return False, "already exists"

    contents = _open_compose()
    contents["volumes"][volname] = opts
    _save_compose(contents)


def volume_exists(volname):
    contents = _open_compose()
    return volname in contents["volumes"]


def add_mount(svc: str, volname: str, path: str):
    contents = _open_compose()
    vols = contents["services"][svc]["volumes"]
    if not vols:
        vols = []
    mount = f"{volname}:{path}"
    if mount not in vols:
        vols.append(mount)
    contents["services"][svc]["volumes"] = vols
    _save_compose(contents)


def add_section_from_template(keyname: str):
    template_section = compose_key(keyname, _load_template_yml())
    contents = _open_compose()

    keys = keyname.split(".")
    last = keys.pop()

    val = contents
    for k in keys:
        if k not in val:
            return False
        val = val[k]

    val[last] = template_section

    _save_compose(contents)

    return True


def remove_key(keyname):
    contents = _open_compose()

    keys = keyname.split(".")
    last = keys.pop()

    val = contents
    for k in keys:
        if k not in val:
            return False
        val = val[k]

    val.pop(last, None)

    _save_compose(contents)

    return True


def set_key(keyname, value):
    contents = _open_compose()

    keys = keyname.split(".")
    last = keys.pop()

    val = contents
    for k in keys:
        if k not in val:
            return False
        val = val[k]

    val[last] = value

    _save_compose(contents)

    return True
