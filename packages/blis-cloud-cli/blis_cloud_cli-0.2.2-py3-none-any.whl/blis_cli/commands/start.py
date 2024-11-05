import click
import os

from blis_cli.util import config
from blis_cli.util import docker_util


def run():
    if not os.path.exists(config.compose_file()):
        click.secho("Please run `blis install` and run this command again.", fg="red")
        return 1

    return docker_util.start_blis()
