import click
import os
import psutil
import socket

from blis_cli.util import bash


@click.group()
def entrypoint():
    pass


@click.command()
def status():
    swap_space = psutil.swap_memory().total / (1024.0**3)
    swap_enabled = (swap_space > 0)

    if swap_enabled:
        click.echo("Swap space: ", nl=False)
        click.secho(f"{swap_space:.2f} GB", fg="green")
    else:
        click.secho("Swap space is not configured.", fg="red")

    exit(0)


# Creates a 1 GB swap file
# TODO: make it more configurable
@click.command()
def create():
    if os.path.exists("/swapfile"):
        click.echo("Swapfile already exists.")
        exit(1)

    if psutil.swap_memory().total > 0:
        click.echo("A swap partition or swap file is already configured.")
        exit(1)

    bash.run("dd if=/dev/zero of=/swapfile bs=1024 count=1048576", root=True)
    bash.run("mkswap /swapfile", root=True)
    bash.run("chmod 600 /swapfile", root=True)
    bash.run("swapon /swapfile", root=True)
    bash.run("echo -e \"# Added by blis-cloud-cli\\n/swapfile\\tnone\\tswap\\tsw\\t0\\t0\" | tee -a /etc/fstab", root=True)

    click.secho("Swapfile created!", fg="green")
    exit(0)

entrypoint.add_command(status)
entrypoint.add_command(create)
