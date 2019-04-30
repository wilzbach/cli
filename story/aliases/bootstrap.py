# -*- coding: utf-8 -*-
import click

from .. import cli
from .. import options
from ..commands import bootstrap


@cli.cli.command(name='bootstrap', hidden=True)
# @options.app()
@click.argument('story', default='-', type=click.Choice(bootstrap.CHOICES))
#
@click.argument(
    'output_file', default=None, type=click.Path(exists=False), required=False
)
@click.pass_context
def config_list(ctx, **kwargs):
    cli.print_deprecated_warning(alternative='story write')
    ctx.forward(bootstrap.write)
