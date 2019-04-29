# -*- coding: utf-8 -*-
import click

from .. import cli
from .. import options
from ..commands import apps


@cli.cli.command(name='apps:list', hidden=True)
@click.pass_context
def apps_list(ctx):
    cli.print_deprecated_warning(alternative='asyncy apps list')
    ctx.forward(apps.list_command)


@cli.cli.command(name='apps:create', hidden=True)
@click.argument('name', nargs=1, required=False)
@click.option('--team', type=str,
              help='Team name that owns this new Application')
@click.pass_context
def apps_create(ctx, name, team):
    cli.print_deprecated_warning(alternative='asyncy apps create')
    ctx.forward(apps.create)


@cli.cli.command(name='apps:url', hidden=True)
@options.app()
@click.pass_context
def apps_url(ctx, app):
    cli.print_deprecated_warning(alternative='asyncy apps url')
    ctx.forward(apps.url)


@cli.cli.command(name='apps:destroy', hidden=True)
@options.app()
@click.option('--confirm', is_flag=True,
              help='Do not prompt to confirm destruction.')
@click.pass_context
def apps_destroy(ctx, confirm, app):
    cli.print_deprecated_warning(alternative='asyncy apps destroy')
    ctx.forward(apps.destroy)
