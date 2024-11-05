import click
import docker
import shutil
import subprocess

from blis_cli.util import bash
from blis_cli.util import caddy
from blis_cli.util import config


def installed():
    return shutil.which("docker") is not None


def compose_v1_installed():
    if not installed():
        return False
    return shutil.which("docker-compose") is not None


def compose_v2_installed():
    if not installed():
        return False
    res = subprocess.run(["docker", "compose"], capture_output=True)
    return res.returncode == 0


def compose():
    if compose_v2_installed():
        return "docker compose"
    elif compose_v1_installed():
        return "docker-compose"
    else:
        return None


# Finds the _first_ container running the BLIS image.
def blis_container(client=None):
    try:
        client = client or docker.from_env()
        img_tag = config.compose_key("services.app.image")
        for container in client.containers.list():
            if img_tag in container.image.tags:
                return container
    except Exception as e:
        return None
    return None


def blis_is_running():
    return blis_container() is not None


def stop_blis_with_confirm():
    click.secho(
        "BLIS must be stopped in order to continue.",
        fg="yellow",
    )
    if not click.confirm("Continue stopping BLIS?"):
        return False
    click.echo("Stopping BLIS... ", nl=False)
    blis_container().stop()
    click.secho("Success!", fg="green")
    return True


# Starts BLIS containers
# Starting only "app" will ensure that all of the containers will come up at once.
# 'containers' can be specified to start containers in a certain order (if possible)
def start_blis(*containers):
    if not containers or len(containers) == 0:
        containers = ["db", "app"]

    for container in containers:
        click.echo(f"Starting BLIS {container}... ", nl=False)
        out, err = bash.run(
            f"{compose()} -f {config.compose_file()} up -d --wait {container}"
        )
        if err:
            click.secho("Failed", fg="red")
            click.echo(err, err=True)
            return 1
        else:
            click.secho("Success!", fg="green")

    return 0


def restart_caddy():
    if not caddy.installed():
        return

    click.echo(f"Restarting Caddy... ", nl=False)

    caddy_container = None

    try:
        client = docker.from_env()
        img_tag = config.compose_key("services.caddy.image")
        for container in client.containers.list():
            if img_tag in container.image.tags:
                caddy_container = container
                break
    except Exception as e:
        click.secho("Failed", fg="red")
        click.echo(e, err=True)
        return 1

    if caddy_container is not None:
        out, err = bash.run(
            f"{compose()} -f {config.compose_file()} restart caddy"
        )
        if err:
            click.secho("Failed", fg="red")
            click.echo(err, err=True)
            return 1
        else:
            click.secho("Success!", fg="green")
