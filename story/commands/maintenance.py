# -*- coding: utf-8 -*-

import click

import click_spinner

from .. import api
from .. import cli
from .. import options


@cli.cli.group()
def maintenance():
    """
    Manage the availability of your apps
    """
    pass


@maintenance.command()
@options.app()
def check(app):
    """
    Returns if the application is in maintenance mode.
    """
    cli.user()
    click.echo(f'Fetching maintenance mode for {app}... ',
               nl=False)
    with click_spinner.spinner():
        enabled = api.Apps.maintenance(app=app, maintenance=None)
    if enabled:
        click.echo(click.style('ON. Application is disabled.',
                   bold=True, fg='red'))
    else:
        click.echo(click.style('off. Application is running.',
                   bold=True, fg='green'))


@maintenance.command()
@options.app()
def on(app):
    """
    Turns maintenance mode on.
    """
    cli.user()
    click.echo(f'Enabling maintenance mode for app {app}... ',
               nl=False)
    with click_spinner.spinner():
        app = api.Apps.maintenance(app=app, maintenance=True)
    click.echo(click.style('√', fg='green'))
    click.echo(click.style('Application is now in maintenance mode.',
                           dim=True))


@maintenance.command()
@options.app()
def off(app):
    """
    Turns maintenance mode off.
    """
    cli.user()
    click.echo(f'Disabling maintenance mode for app {app}... ',
               nl=False)
    with click_spinner.spinner():
        app = api.Apps.maintenance(app=app, maintenance=False)
    click.echo(click.style('√', fg='green'))
    click.echo(click.style('Application is now running.',
                           dim=True))
