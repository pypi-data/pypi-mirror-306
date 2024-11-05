import click
import docker as lib_docker
import getpass
import os
import requests
import shutil

from blis_cli.util import bash
from blis_cli.util import config
from blis_cli.util import docker_util
from blis_cli.util import environment as env
from blis_cli.util import packages


@click.group()
def entrypoint():
    pass


@click.command()
def install():
    # If Docker is installed, and we are in the docker group, we will not need root privileges.
    if not (env.in_docker_grp() and docker_util.installed()):
        if not (os.geteuid() == 0 or env.can_sudo()):
            click.secho(
                "Docker must be installed. You must run this script as root or have passwordless sudo privileges.",
                fg="red",
            )
            exit(1)

        install_docker()

        # Returns a success code because we probably succeeded and installed Docker, but we need to log out and log back in.
        exit(0)

    # We might have Docker installed, but not be in the docker group.
    if docker_util.installed() and not env.in_docker_grp():
        click.secho(
            "You have Docker installed, but you are not in the docker group.",
            fg="yellow",
        )
        # Try to fix the problem...
        if env.can_sudo():
            bash.sudo(f"usermod -aG docker {getpass.getuser()}")
            click.echo("Please log out and log back in, and run this command again.")
            exit(0)
        else:
            click.secho(
                "You must run this script as root or have passwordless sudo privileges.",
                fg="red",
            )
        exit(1)

    click.secho("Docker is installed!", fg="green")


def install_docker():
    click.echo("Setting up Docker... ")
    packages.remove(["docker", "docker-engine", "docker.io", "containerd", "runc"])
    packages.install(["ca-certificates", "curl", "gnupg", "lsb-release"])
    bash.sudo("mkdir -p /etc/apt/keyrings")
    bash.run(
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o - | sudo tee /etc/apt/keyrings/docker.gpg >/dev/null"
    )
    bash.run(
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
    )
    packages.apt_update()
    packages.install(
        [
            "docker-ce",
            "docker-ce-cli",
            "containerd.io",
            "docker-compose-plugin",
            "docker-buildx-plugin",
        ]
    )
    bash.sudo(f"usermod -aG docker {getpass.getuser()}")
    bash.sudo("systemctl enable docker.service")
    bash.sudo("systemctl start docker.service")
    click.secho("Success!", fg="green")
    click.echo("Please log out and log back in, and run this command again.")


@click.command()
def purge():
    if not env.can_sudo():
        click.secho("You must have root privileges to run this.", fg="red")
        exit(1)

    packages.remove(["docker", "docker-engine", "docker.io", "containerd", "runc"])
    packages.remove(
        [
            "docker-ce",
            "docker-ce-cli",
            "containerd.io",
            "docker-compose-plugin",
            "docker-buildx-plugin",
        ]
    )
    packages.apt_update()


@click.command()
def status():
    docker_ok = True
    click.echo("Docker is accessible? ", nl=False)
    try:
        client = lib_docker.from_env()
        client.containers.list()
        click.secho("Yes", fg="green")
    except Exception as e:
        docker_ok = False
        print(e)
        click.secho("No", fg="red")

    cmd = "blis docker install"
    if not env.can_sudo():
        cmd = "sudo " + cmd

    if not docker_ok:
        click.echo("Docker is not accessible. Please run:")
        click.echo("  " + cmd)
        return 0

    click.echo("Docker Compose is installed? ", nl=False)
    if docker_util.compose_v2_installed():
        click.secho("v2", fg="green")
    elif docker_util.compose_v1_installed():
        click.secho("v1", fg="green")
    else:
        click.secho("No", fg="red")
        click.echo("Docker Compose is not installed. Please run:")
        click.echo("  " + cmd)
        return 0


entrypoint.add_command(install)
entrypoint.add_command(purge)
entrypoint.add_command(status)
