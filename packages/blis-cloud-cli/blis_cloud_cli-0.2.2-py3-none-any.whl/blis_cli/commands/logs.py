import click
import docker
import tarfile
import tempfile

from blis_cli.util import config
from blis_cli.util import environment
from blis_cli.util import docker_util


@click.group()
def entrypoint():
    pass


def get_container_log_file(filename):
    try:
        c = docker_util.blis_container()

        # This is technically not required. We could probably extract logs from
        # a stopped BLIS since the /log folder is mounted as its own volume.
        # However... I don't know how to reliably do that right now.
        # And it would definitely need root.
        if c == None:
            click.secho("BLIS is not running.", fg="red")
            click.echo("Please start BLIS to see logs.")
            return 0

        with tempfile.TemporaryFile() as f:
            bits, stat = c.get_archive(filename)

            for chunk in bits:
                f.write(chunk)

            f.seek(0)
            tf = tarfile.open(fileobj=f)
            m = tf.extractfile(tf.getnames()[0])
            for chunk in m:
                click.echo(chunk, nl=False)

    except docker.errors.NotFound as e:
        click.echo("The log file was not found.", err=True)
        return 1
    except Exception as e:
        click.echo("There was a problem getting the logs for BLIS!", err=True)
        click.echo(e)
        return 1


@click.command()
def application():
    exit(get_container_log_file("/var/www/blis/log/application.log"))


@click.command()
def database():
    exit(get_container_log_file("/var/www/blis/log/database.log"))


@click.command(name="apache2/access")
def apache2_access():
    exit(get_container_log_file("/var/log/apache2/access.log"))


@click.command(name="apache2/error")
def apache2_error():
    exit(get_container_log_file("/var/log/apache2/error.log"))


entrypoint.add_command(application)
entrypoint.add_command(database)
entrypoint.add_command(apache2_access)
entrypoint.add_command(apache2_error)
