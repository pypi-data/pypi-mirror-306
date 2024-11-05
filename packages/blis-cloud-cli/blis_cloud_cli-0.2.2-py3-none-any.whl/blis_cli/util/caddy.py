import click
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import shutil
import subprocess
import re

from blis_cli.util import config
from blis_cli.util import docker_util


jinja2 = Environment(
    loader=FileSystemLoader(f"{os.path.dirname(__file__)}/../extra/templates/"),
    autoescape=select_autoescape(),
)

CADDY_STANZA_START = re.compile("^https://(.+) {\s?$")


def caddyfile():
    return os.path.join(config.basedir(), "Caddyfile")


def installed():
    caddyfile_exists = os.path.exists(caddyfile())
    caddy_stanza_present = config.compose_key("services.caddy")
    return caddyfile_exists and (caddy_stanza_present is not None)


def install():
    config.add_volume("caddy_data")
    config.add_volume("caddy_config")
    config.add_section_from_template("services.caddy")
    config.remove_key("services.app.ports")
    config.set_key("services.app.depends_on", ["db", "caddy"])


def set_domains(domains: list):
    try:
        template = jinja2.get_template("Caddyfile.j2")
        rendered = template.render(domains=domains)

        with open(os.path.join(config.basedir(), "Caddyfile"), "w") as f:
            f.write(rendered)
            return None
    except Exception as e:
        return e


def get_domains():
    domains = []
    try:
        with open(os.path.join(config.basedir(), "Caddyfile"), "r") as f:
            for line in f:
                res = CADDY_STANZA_START.match(line)
                if res:
                    domains.append(res.groups()[0])
    except FileNotFoundError as e:
        return []
    except Exception as e:
        click.secho("Error reading Caddyfile: " + e, fg="red")
        return []
    return domains
