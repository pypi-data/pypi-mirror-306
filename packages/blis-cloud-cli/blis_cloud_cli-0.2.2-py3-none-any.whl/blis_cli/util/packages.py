import click

from blis_cli.util import bash


def apt_update():
    return bash.sudo("DEBIAN_FRONTEND=noninteractive apt-get update")


def install(packages: list):
    click.echo(f"Installing packages: {', '.join(packages)}")
    return bash.sudo(
        f"DEBIAN_FRONTEND=noninteractive apt-get install -y {' '.join(packages)}"
    )


def remove(packages: list):
    click.echo(f"Removing packages: {', '.join(packages)}")
    return bash.sudo(
        f"DEBIAN_FRONTEND=noninteractive apt-get remove -y {' '.join(packages)}"
    )


def is_installed(package: str):
    _, err = bash.run(f"dpkg -s {package}")
    return err == None
