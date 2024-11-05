import click
import os
import sys
import subprocess


def run(command: str, root=False):
    cmd = ["bash", "-c", command]
    if root:
        cmd = ["sudo"] + cmd

    if "BLIS_DEBUG" in os.environ and os.environ["BLIS_DEBUG"] == "true":
        click.echo("+ " + " ".join(cmd))

    proc = subprocess.run(cmd, capture_output=True)

    if proc.returncode == 0:
        return str(proc.stdout, "utf-8"), None
    else:
        return str(proc.stdout, "utf-8"), str(proc.stderr, "utf-8")


def sudo(command: str):
    use_sudo = os.geteuid() != 0
    return run(command, root=use_sudo)
