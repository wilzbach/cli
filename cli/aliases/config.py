# -*- coding: utf-8 -*-
import click

from .. import cli
from .. import options
from ..commands import config


@cli.cli.command(name='config:list', hidden=True)
@options.app()
@click.pass_context
def config_list(ctx, app):
    cli.print_deprecated_warning(alternative='asyncy config list')
    ctx.forward(config.list_command)


@cli.cli.command(name='config:set', hidden=True)
@click.argument('variables', nargs=-1)
@click.option('--message', '-m', nargs=1, default=None,
              help='(optional) Message why variable(s) were created.')
@options.app()
@click.pass_context
def config_set(ctx, variables, app, message):
    cli.print_deprecated_warning(alternative='asyncy config set')
    ctx.forward(config.set_command)


@cli.cli.command(name='config:get', hidden=True)
@click.argument('variables', nargs=-1)
@options.app()
@click.pass_context
def config_get(ctx, variables, app):
    cli.print_deprecated_warning(alternative='asyncy config get')
    ctx.forward(config.get)


@cli.cli.command(name='config:del', hidden=True)
@click.argument('variables', nargs=-1)
@click.option('--message', '-m', nargs=1, default=None,
              help='(optional) Message why variable(s) were deleted.')
@options.app()
@click.pass_context
def config_del(ctx, variables, app, message):
    cli.print_deprecated_warning(alternative='asyncy config del')
    ctx.forward(config.del_command)
