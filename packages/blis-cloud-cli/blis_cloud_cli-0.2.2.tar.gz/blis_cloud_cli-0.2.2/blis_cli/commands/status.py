import click
import psutil

from blis_cli.util import caddy
from blis_cli.util import config
from blis_cli.util import environment as blis_env
from blis_cli.util import docker_util as blis_docker_util


def run():
    try:
        blis_installed = False
        click.echo("BLIS is installed: ", nl=False)
        if config.validate_compose():
            blis_installed = True
            click.secho("Yes!", fg="green")
        else:
            click.secho("No", fg="red")

        click.echo("BLIS is running: ", nl=False)
        if blis_docker_util.blis_is_running():
            click.secho("Yes!", fg="green")
        else:
            click.secho("No", fg="red")

        click.echo("Caddy is enabled: ", nl=False)
        if caddy.installed():
            click.secho("Yes!", fg="green")
        else:
            click.secho("No", fg="red")
            if blis_installed:
                click.secho("Custom domain support is disabled. Please run `blis domain add` to setup.", fg="red")

        total_ram = psutil.virtual_memory().total / (1024.0**3)
        swap_space = psutil.swap_memory().total / (1024.0**3)
        click.echo("Total RAM: ", nl=False)
        click.secho(f"{total_ram:.2f} GiB", fg="green", nl=False)
        if swap_space > 0:
            click.secho(f" (swap: {swap_space:.2f} GiB)", fg="green")
        else:
            click.echo()

        if total_ram < 0.9:
            click.secho(
                "1GB of RAM is recommended to run BLIS. Things might not work as expected!",
                fg="red",
            )

        click.echo("Supported Ubuntu distribution: ", nl=False)
        if blis_env.supported_distro():
            click.secho("Yes!", fg="green")
        else:
            click.secho("No", fg="red")
            click.echo("BLIS is supported on these Ubuntu distributions: ", nl=False)
            click.secho(", ".join(blis_env.SUPPORTED_DISTROS), fg="green")
            click.echo("You have: ", nl=False)
            click.secho(blis_env.distro(), fg="green")

        click.echo("Passwordless sudo: ", nl=False)
        if blis_env.can_sudo():
            click.secho("Yes!", fg="green")
        else:
            click.secho("No", fg="red")

        if (
            blis_docker_util.blis_container() == None
            and not blis_docker_util.installed()
        ):
            click.secho(
                "Please run `blis docker status` to check the status of Docker on your machine.",
                fg="yellow",
            )

        return 0
    except Exception as e:
        click.echo("There was a problem getting the status of BLIS!")
        click.echo(e)
        return 1
