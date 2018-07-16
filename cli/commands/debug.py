# -*- coding: utf-8 -*-

import json
from glob import glob

import click
import click_spinner
import delegator
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer

from .. import cli


@cli.cli.command()
@click.option('--pager', '-p', is_flag=True, help='Review payload only')
@click.option('--message', '-m',
              help='A short or long message about what went wrong.')
def debug(pager, message):
    """
    Upload a support bundle
    """
    assert cli.user()
    cli.track('Support Bundle')

    if not pager and not message:
        click.echo(click.style('About to send a support bundle '
                               'to our team for analysis.', dim=True))
        click.echo(click.style('Tell us a little about what happened.',
                               bold=True))
        message = click.prompt('Message')

    click.echo(click.style('Building support bundle... ', bold=True), nl=False)
    with click_spinner.spinner():

        def file(path):
            try:
                return (
                    path,
                    json.loads(cli.run(f'exec -T bootstrap cat {path}').out)
                )
            except Exception:
                return (path, None)

        def read(path):
            with open(path, 'r') as file:
                return path, file.read()

        def container(id):
            try:
                data = json.loads(delegator.run(f'docker inspect {id}').out)[0]
                return data['Name'], data
            except Exception:
                return id, None

        bundle = {
            'message': message,
            'files': {
                'volume': dict(map(file, ('/asyncy/config/stories.json',
                                          '/asyncy/config/services.json',
                                          '/asyncy/config/environment.json'))),
                'stories': dict(map(read,
                                    (glob('*.story') + glob('**/*.story'))))
            },
            'logs': cli.run('logs').out.split('\n'),
            'versions': {
                'docker': delegator.run('docker version').out.split('\n'),
                'compose': cli.run('version').out.split('\n')
            },
            'containers': dict(map(container,
                                   cli.run('ps -q').out.split('\n')))
        }

    click.echo('Done')

    if pager:
        bundle.pop('logs')
        click.echo_via_pager(
            highlight(
                json.dumps(bundle, indent=4),
                JsonLexer(),
                TerminalFormatter()
            )
        )

    else:
        click.echo(click.style('Uploading support bundle... ', bold=True),
                   nl=False)
        with click_spinner.spinner():
            cli.sentry.captureMessage(f'Support Bundle: {message[:20]}',
                                      extra=bundle)
        click.echo('Done')