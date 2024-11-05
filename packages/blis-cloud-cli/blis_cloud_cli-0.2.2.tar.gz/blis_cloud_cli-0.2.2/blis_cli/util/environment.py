import os
import subprocess
import pwd
import grp


def can_sudo():
    result = subprocess.run(["sudo", "-n", "echo", "hello"], capture_output=True)
    return result.returncode == 0 and result.stdout == b"hello\n"


def distro():
    result = subprocess.run(
        ["grep", "DISTRIB_CODENAME", "/etc/lsb-release"], capture_output=True
    )
    if result.returncode == 0:
        return result.stdout.decode("utf-8").strip().split("=")[1]


def user():
    return pwd.getpwuid(os.getuid())[0]


def in_docker_grp():
    try:
        return user() in grp.getgrnam("docker")[3]
    except KeyError:
        return False


SUPPORTED_DISTROS = set(["focal", "jammy", "noble"])


def supported_distro():
    return distro() in SUPPORTED_DISTROS
