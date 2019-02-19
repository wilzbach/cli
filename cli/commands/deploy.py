# -*- coding: utf-8 -*-
import sys

import click

import click_spinner

from .test import compile_app
from .. import cli, options
from ..api import Config, Releases


@cli.cli.command()
@click.option('--message', is_flag=True, help='Deployment message')
@options.app(allow_option=False)
def deploy(app, message):
    """
    Deploy your app instantly to the Asyncy Cloud
    """
    cli.user()

    payload = compile_app(app, False)  # Also adds a spinner.

    if payload is None:
        sys.exit(1)  # Error already printed by compile_app.

    click.echo(f'Deploying app {app}... ', nl=False)

    with click_spinner.spinner():
        config = Config.get(app)
        release = Releases.create(config, payload, app, message)

    url = f'https://{app}.asyncyapp.com'
    click.echo()
    click.echo(click.style('√', fg='green') +
               f' Version {release["id"]} of your app has '
               f'been queued for deployment.\n\n'
               f'Check the deployment status with:')
    cli.print_command('asyncy releases list')
    click.echo()
    click.echo(f'If your story listens to HTTP requests, visit {url}')
