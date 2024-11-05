import click

from blis_cli.util import bash
from blis_cli.util import config
from blis_cli.util import docker_util as docker


def run():
    click.echo("Stopping BLIS... ", nl=False)
    out, err = bash.run(f"{docker.compose()} -f {config.compose_file()} down")
    if err:
        click.secho("Failed", fg="red")
        click.echo(err, err=True)
        return False

    click.secho("Success!", fg="green")

    return 0
