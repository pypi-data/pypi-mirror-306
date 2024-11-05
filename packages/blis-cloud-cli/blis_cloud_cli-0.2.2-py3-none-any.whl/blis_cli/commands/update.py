import click
import docker

from blis_cli.util import bash
from blis_cli.util import caddy
from blis_cli.util import config
from blis_cli.util import docker_util


def run():
    restart_blis = False
    if docker_util.blis_is_running():
        if not docker_util.stop_blis_with_confirm():
            return 1
        restart_blis = True

    click.echo("Updating BLIS... ", nl=False)
    out, err = bash.run(f"{docker_util.compose()} -f {config.compose_file()} pull app")
    if err:
        click.secho("Failed", fg="red")
        click.echo(err, err=True)
        return 1
    click.secho("Success!", fg="green")

    if not caddy.installed():
        click.echo("Installing Caddy... ", nl=False)
        try:
            caddy.install()
            click.secho("Success!", fg="green")
        except Exception as e:
            click.secho(e, fg="red")
            return 1

    if not config.volume_exists("blis-local"):
        config.add_volume("blis-local")
        config.add_mount("app", "blis-local", "/var/www/blis/local")
        click.echo("Created blis-local volume.")

    if restart_blis:
        return docker_util.start_blis("app")

    return 0
