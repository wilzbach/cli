# -*- coding: utf-8 -*-
import click

from .. import cli
from .. import options
from ..commands import maintenance


@cli.cli.command(name='maintenance:check', hidden=True)
@options.app()
@click.pass_context
def maintenance_check(ctx, app):
    cli.print_deprecated_warning(alternative='asyncy maintenance check')
    ctx.forward(maintenance.check)


@cli.cli.command(name='maintenance:on', hidden=True)
@options.app()
@click.pass_context
def maintenance_on(ctx, app):
    cli.print_deprecated_warning(alternative='asyncy maintenance on')
    ctx.forward(maintenance.on)


@cli.cli.command(name='maintenance:off', hidden=True)
@options.app()
@click.pass_context
def maintenance_off(ctx, app):
    cli.print_deprecated_warning(alternative='asyncy maintenance off')
    ctx.forward(maintenance.off)
