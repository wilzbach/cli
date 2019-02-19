# -*- coding: utf-8 -*-
import json
import os
import sys

import click

import click_spinner

import emoji

from .. import cli


@cli.cli.command()
@click.option('--debug', is_flag=True, help='Compile in debug mode')
def test(debug):
    """
    Compile your project and check for any errors
    """

    cli.user()

    app_name = cli.get_app_name_from_yml() or 'Not created'
    tree = compile_app(app_name, debug)

    if tree is None:
        sys.exit(1)

    count = len(tree.get('stories', {}))

    if count == 0:
        click.echo(click.style('\tX', fg='red') + ' No stories found')
        sys.exit(1)
    else:
        for k, v in tree['stories'].items():
            click.echo(click.style('\t√', fg='green') + f' {k}')

    click.echo(click.style('√', fg='green') +
               emoji.emojize(' Looking good! :thumbs_up:'))
    click.echo()
    click.echo('Deploy your app with:')
    cli.print_command('asyncy deploy')


def compile_app(app_name_for_analytics, debug) -> dict:
    """
    Compiles, prints pretty info, and returns the compiled tree.
    :return: The compiled tree
    """
    from storyscript.App import App
    click.echo(click.style('Compiling Stories...', bold=True))

    with click_spinner.spinner():
        try:
            stories = json.loads(App.compile(os.getcwd()))
        except BaseException as e:
            click.echo('Failed to compile project:\n', err=True)
            click.echo(click.style(str(e.error), fg='red'), err=True)
            stories = None

        result = 'Success'
        count = 0

        if stories is None:
            result = 'Failed'
        else:
            count = len(stories.get('stories', {}))

        cli.track('App Compiled', {
            'App name': app_name_for_analytics,
            'Result': result,
            'Stories': count
        })

    return stories
