import click
import psutil
import socket

from blis_cli.util import caddy
from blis_cli.util import docker_util


@click.group()
def entrypoint():
    pass


@click.command()
def status():
    click.secho("Caddy is configured: ", nl=False)
    if caddy.installed():
        click.secho("Yes!", fg="green")
    else:
        click.secho("No", fg="red")
        click.echo("\nThere are no domains configured. Please run:")
        click.echo("  blis domain add [mydomain.example.com]")
        exit(0)

    domains = caddy.get_domains()
    if len(domains) < 1:
        click.echo("\nThere are no domains configured. Please run:")
        click.echo("  blis domain add [mydomain.example.com]")
        exit(0)

    # These are only "possible" IPs because the computer
    # might be behind a firewall/NAT and these will only contain
    # the local IP addresses.
    possible_ipv4_addrs = get_interfaces()

    for domain in domains:
        click.echo()
        click.secho(domain, fg="green")
        click.echo("IP Addresses: ", nl=False)
        ip_addrs = get_ipv4_by_hostname(domain)
        click.secho(", ".join(ip_addrs), fg="green")

        for ip in ip_addrs:
            if ip in possible_ipv4_addrs:
                # This is the 'happiest' path since the computer/VM has an IP that is facing the Internet.
                click.secho("Domain points to computer!")
                break

    exit(0)


@click.command()
@click.argument("name")
def add(name: str):
    current_domains = caddy.get_domains()
    if name in current_domains:
        click.echo(f"{name} is already configured as a domain.")
        return 0

    click.confirm(f"Do you want to add {name} as a domain?", abort=True)

    restart_blis = False
    if docker_util.blis_is_running():
        if not docker_util.stop_blis_with_confirm():
            return 1
        restart_blis = True

    if not caddy.installed():
        click.echo("Installing Caddy... ", nl=False)
        try:
            caddy.install()
            click.secho("Success!", fg="green")
        except Exception as e:
            click.secho(e, fg="red")
            return 1

    click.echo(f"Adding {name} to Caddyfile... ", nl=False)

    current_domains.append(name)
    caddy.set_domains(current_domains)

    click.secho("Success!", fg="green")

    if restart_blis:
        docker_util.start_blis("app")
        docker_util.restart_caddy()


@click.command()
def clear():
    click.secho("This will remove all of the domains from the configuration.", fg="red")
    click.confirm(f"Do you want to continue?", abort=True)

    restart_blis = False
    if docker_util.blis_is_running():
        if not docker_util.stop_blis_with_confirm():
            return 1
        restart_blis = True

    click.echo(f"Removing all domains from Caddyfile... ", nl=False)

    caddy.set_domains([])

    click.secho("Success!", fg="green")

    if restart_blis:
        docker_util.start_blis("app")
        docker_util.restart_caddy()


# Source:
# https://stackoverflow.com/questions/2805231/how-can-i-do-dns-lookups-in-python-including-referring-to-etc-hosts/66000439#66000439
# Licensed: CC BY-SA 4.0
def get_ipv4_by_hostname(hostname):
    # see `man getent` `/ hosts `
    # see `man getaddrinfo`
    try:
        return list(
            i[4][0]  # raw socket structure  # internet protocol info  # address
            for i in socket.getaddrinfo(hostname, 0)  # port, required
            if i[0] is socket.AddressFamily.AF_INET  # ipv4
            # ignore duplicate addresses with other socket types
            and i[1] is socket.SocketKind.SOCK_RAW
        )
    except Exception as e:
        click.secho(str(e), fg="red", nl=False)
        return []


def get_interfaces():
    addrs = psutil.net_if_addrs()
    ip_addrs = []
    for key in addrs:
        addr = addrs[key]
        for a in addr:
            if a.family == socket.AddressFamily.AF_INET:
                ip_addrs.append(a.address)

    return ip_addrs


entrypoint.add_command(add)
entrypoint.add_command(clear)
entrypoint.add_command(status)
