# -*- coding: utf-8 -*-
import pkgutil

import click

import emoji

from .. import cli


@cli.cli.command()
@click.argument('story', default='-',
                type=click.Choice(['http', 'every', 'function',
                                   'if', 'loop', 'twitter',
                                   'slack-bot', 'subscribe',
                                   'every', 'websocket', '-']))
def bootstrap(story):
    """Pre–defined templates to bootstrap your app!"""
    if story != '-':
        data = pkgutil.get_data('cli', f'stories/{story}.story')
        click.echo(data)
        app_name = cli.get_app_name_from_yml()
        if app_name is None:
            app_name = 'Not created yet'

        cli.track('App Bootstrapped',
                  {'App name': app_name, 'Template used': story})

    else:
        click.echo(click.style('Choose a template', bold=True))
        click.echo(click.style('   http', fg='cyan') +
                   '      - serverless http endpoint')
        click.echo(click.style('   function', fg='cyan') +
                   '  - generic function')
        click.echo(click.style('   if', fg='cyan') +
                   '        - if/then')
        click.echo(click.style('   loop', fg='cyan') +
                   '      - for loop')
        click.echo(click.style('   twitter', fg='cyan') +
                   '   - stream tweets')
        click.echo('')

        click.echo(click.style('Coming soon', bold=True) +
                   ' -- Under active development')
        click.echo(click.style('   slack-bot', fg='cyan') +
                   ' - Slack bot')
        click.echo(click.style('   subscribe', fg='cyan') +
                   ' - event subscriptions')
        click.echo(click.style('   every', fg='cyan') +
                   '     - periodic run this')
        click.echo(click.style('   websocket', fg='cyan') +
                   ' - websocket support')
        click.echo('')

        click.echo(
            '  Run $ ' +
            click.style('story bootstrap :template_name: ', fg='magenta') +
            emoji.emojize(':backhand_index_pointing_left:')
        )
        click.echo('')

        click.echo(click.style('Learn more:', bold=True))
        click.echo('  - Examples: ' +
                   click.style('https://github.com/topics/storyscript-example',
                               fg='cyan'))
        click.echo('  - Services: ' +
                   click.style('https://hub.storyscript.io/', fg='cyan'))
        click.echo('')
