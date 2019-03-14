# -*- coding: utf-8 -*-
import re
from datetime import datetime

import click

import click_spinner

import requests

from .. import cli
from .. import options
from ..api import Apps


@cli.cli.command()
@click.option('--follow', '-f', is_flag=True, help='Follow the logs')
@click.option('--all', is_flag=True,
              help='Return logs from all services')
@options.app()
def logs(follow, all, app):
    """
    Fetch logs for your app
    """
    if follow:
        click.echo('-f (following log output) is not supported yet.')
        return

    cli.user()

    url = 'https://stories.asyncyapp.com/logs'
    click.echo(f'Retrieving logs for {app}... ', nl=False)
    params = {
        'access_token': cli.get_access_token(),
    }

    if all:
        params['all'] = 'true'

    with click_spinner.spinner():
        params['app_id'] = Apps.get_uuid_from_hostname(app)
        r = requests.get(url, params=params)

    click.echo()

    try:
        arr = r.json()
        assert isinstance(arr, list)
    except BaseException:
        click.echo('Logs for your app aren\'t available right now.\n'
                   'If this error persists, please shoot us an email '
                   'on support@asyncy.com', err=True)
        import sys
        sys.exit(1)

    cli.track('App Logs Retrieved', {'App name': app, 'Log count': len(arr)})

    if len(arr) == 0:
        click.echo(f'No logs found for {app}')
        return

    arr.reverse()  # Latest is at the head.

    for log in arr:
        if not all:
            message: str = log['payload']['message']
            level = log['payload']['level']
        else:
            message: str = log['payload']
            level = log['severity']

        level = level[:6].rjust(6)

        # Replace the ":" in the timezone field for datetime.
        ts = log['timestamp']
        ts = ts[0:ts.rindex(':')] + ts[ts.rindex(':') + 1:]
        if all:
            # Truncate milliseconds from the date
            # (sometimes this appears, and sometimes it doesn't appear)
            ts = re.sub(r'\.[0-9]*', '', ts)
            date = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S%z')
        else:
            date = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S.%f%z')

        pretty_date = date.astimezone().strftime('%b %d %H:%M:%S')

        tag = None
        if all:
            tag = log['resource'][1]['container_name'][:21]

        colourize_and_print(pretty_date, tag, level, message.strip())


def colourize_and_print(date, tag, level, message):
    level_col = 'green'  # Default for info.
    level = level.lower()
    if 'debug' in level:
        level_col = 'blue'
    elif 'warn' in level:
        level_col = 'yellow'
    elif 'crit' in level or 'error' in level:
        level_col = 'red'

    if tag:
        click.echo(f'{click.style(date, fg="white")} '
                   f'{click.style(level.upper(), fg=level_col)} '
                   f'{click.style(tag, fg="blue")}: '
                   f'{message}')
    else:
        click.echo(f'{click.style(date, fg="white")} '
                   f'{click.style(level.upper(), fg=level_col)} '
                   f'{message}')
