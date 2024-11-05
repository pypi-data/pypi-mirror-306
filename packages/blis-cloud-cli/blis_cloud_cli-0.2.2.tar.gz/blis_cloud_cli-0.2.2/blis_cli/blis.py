#!/usr/bin/env python3

import click
import os
import sys
import psutil

from blis_cli.util import config as blis_config
from blis_cli.util import docker_util as blis_docker_util
from blis_cli.util import environment as blis_env

from blis_cli.util import bash
from blis_cli.commands import docker as cmd_docker_grp
from blis_cli.commands import install as cmd_install
from blis_cli.commands import logs as cmd_logs_grp
from blis_cli.commands import start as cmd_start
from blis_cli.commands import status as cmd_status
from blis_cli.commands import stop as cmd_stop
from blis_cli.commands import update as cmd_update
from blis_cli.commands import domain as cmd_domain_grp
from blis_cli.commands import swap as cmd_swap_grp


@click.command()
def status():
    exit(cmd_status.run())


@click.command()
def install():
    exit(cmd_install.run())


@click.command()
def start():
    exit(cmd_start.run())


@click.command()
def stop():
    exit(cmd_stop.run())


@click.command()
def update():
    exit(cmd_update.run())


@click.group()
def entry_point():
    pass


def main():
    entry_point.add_command(install)
    entry_point.add_command(start)
    entry_point.add_command(status)
    entry_point.add_command(stop)
    entry_point.add_command(update)

    entry_point.add_command(cmd_logs_grp.entrypoint, "logs")
    entry_point.add_command(cmd_docker_grp.entrypoint, "docker")
    entry_point.add_command(cmd_domain_grp.entrypoint, "domain")
    entry_point.add_command(cmd_swap_grp.entrypoint, "swap")

    entry_point()

