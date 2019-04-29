# -*- coding: utf-8 -*-
import click

from .. import cli
from .. import options
from ..commands import releases


@cli.cli.command(name='releases:list', hidden=True)
@click.option('--limit', '-n', nargs=1, default=20,
              help='List N latest releases')
@options.app()
@click.pass_context
def list_command(ctx, app, limit):
    cli.print_deprecated_warning(alternative='asyncy releases list')
    ctx.forward(releases.list_command)


@cli.cli.command(name='releases:rollback', hidden=True)
@click.argument('version', nargs=1, required=False)
@options.app()
@click.pass_context
def rollback(ctx, version, app):
    cli.print_deprecated_warning(alternative='asyncy releases rollback')
    ctx.forward(releases.rollback)
