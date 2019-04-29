# -*- coding: utf-8 -*-
import sys
from time import sleep

import click

import click_spinner

from .test import compile_app
from .. import cli, options
from ..api import Apps, Config, Releases


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
               f'been queued for deployment\n')

    click.echo('Waiting for deployment to complete... ', nl=False)
    with click_spinner.spinner():
        if Apps.maintenance(app, maintenance=None):
            click.echo()
            click.echo()
            click.echo('Your app is in maintenance mode.\n'
                       'Run the following to turn off it off:')
            cli.print_command('asyncy maintenance off')
            click.echo()
            click.echo('Once maintenance mode is turned off, '
                       'your app will be deployed immediately.')
            return

        state = 'QUEUED'
        while state in ['DEPLOYING', 'QUEUED']:
            state = Releases.get(app)[0]['state']
            sleep(0.5)

    click.echo()
    if state == 'DEPLOYED':
        click.echo(click.style('√', fg='green') + ' Deployed successfully!')
        click.echo(f'If your story listens to HTTP requests, visit {url}')
    elif state == 'FAILED':
        click.echo(click.style('X', fg='red') + ' Deployment failed!',
                   err=True)
        click.echo(
            'Please use the following command to view your app\'s logs:',
            err=True)
        cli.print_command('asyncy logs')
    else:
        click.echo(
            f'An unhandled state of your app has been encountered - {state}',
            err=True)
        click.echo(f'Please shoot an email to support@asyncy.com')
