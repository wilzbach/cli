# -*- coding: utf-8 -*-
import asyncio
import json
import sys
import time

import click

import click_spinner

import websockets
from websockets import WebSocketClientProtocol

from .. import cli
from .. import options
from ..api import Apps


@cli.cli.command()
@click.option('--follow', '-f', is_flag=True, help='Follow the logs')
@click.option('--last', '-n', default=100, help='Print the last n lines')
@click.option('--service', '-s', is_flag=True,
              help='Return logs from a service instead of the runtime')
@click.option('--service-name', '-sn',
              help='Return logs from the named service')
@click.option('--level', '-l', default='info',
              type=click.Choice(['debug', 'info', 'warning', 'error']),
              help='Specify the minimum log level')
@options.app()
def logs(follow, last, service, service_name, app, level):
    """
    Fetch logs for your app
    """

    if service and service_name is None:
        click.echo('When specifying -s/--service, '
                   '-sn/--service-name must be specified too', err=True)

        sys.exit()

    cli.user()

    click.echo(f'Retrieving logs for {app}... ', nl=False)
    with click_spinner.spinner():
        app_id = Apps.get_uuid_from_hostname(app)

    click.echo()

    cli.track('App Logs Requested', {
        'App name': app,
        'Follow': 'Yes' if follow else 'No',
        'Last N': last,
        'Source': 'Runtime' if service is False else 'Service',
        'Service Name': service_name if service else 'N/A',
        'Minimum level': level.capitalize()
    })

    asyncio.get_event_loop().run_until_complete(
        connect_and_listen(app_id, last, follow, service is False,
                           service,
                           service_name, level))
    return


async def ping_forever(websocket: WebSocketClientProtocol):
    while True:
        await websocket.send('{"command": "ping"}')
        await asyncio.sleep(10)


async def connect_and_listen(app_id, n, follow, runtime_logs,
                             service_logs,
                             service_name, level):
    async with websockets.connect('wss://logs.storyscript.io') as websocket:
        assert isinstance(websocket, WebSocketClientProtocol)

        auth_payload = {
            'command': 'auth', 'access_token': cli.get_access_token(),
            'id': cli.get_access_token(),
            'app_id': app_id
        }
        await websocket.send(json.dumps(auth_payload))

        try:
            auth_response = await websocket.recv()

            # Generally, the log server will close the connection instantly.
            # This authorised check is just for fun.
            # See https://github.com/storyscript/logstreamer#authentication.
            auth_response = json.loads(auth_response)
            if not auth_response['authorised']:
                raise websockets.exceptions.ConnectionClosed(-1, None)

        except websockets.exceptions.ConnectionClosed:
            click.echo('The log server sent an unauthorised response.\nAre '
                       'you sure you have access to view this app\'s logs?',
                       err=True)
            sys.exit(1)

        # Keep the connection alive by sending pings.
        asyncio.get_event_loop().create_task(ping_forever(websocket))

        # Send our filter payload.
        if runtime_logs:
            filter_payload = {
                'command': 'filter',
                'source': 'runtime',
                'level': level,
                'n': n,
                'watch': follow
            }
        else:
            assert service_logs is True
            filter_payload = {
                'command': 'filter',
                'source': 'service',
                'service_name': service_name,
                'level': level,  # Note: The upstream server ignores level.
                'n': n,
                'watch': follow
            }

        await websocket.send(json.dumps(filter_payload))

        while True:
            log = json.loads(await websocket.recv())
            # TODO: handle a connection close, but before that, investigate why the connection appears to close randomly
            date = time.strftime('%b %d %H:%M:%S',
                                 time.localtime(int(log['ts'] / 1000)))
            colourize_and_print(date, 'runtime',
                                log['level'], log['message'])


def colourize_and_print(date, tag, level, message):
    level_col = 'green'  # Default for info.
    level = level.lower()
    if 'debug' in level:
        level_col = 'blue'
    elif 'warn' in level:
        level_col = 'yellow'
    elif 'crit' in level or 'error' in level:
        level_col = 'red'

    level = level[:6].rjust(6)

    if tag:
        click.echo(f'{click.style(date, fg="white")} '
                   f'{click.style(level.upper(), fg=level_col)} '
                   f'{click.style(tag, fg="blue")}: '
                   f'{message}')
    else:
        click.echo(f'{click.style(date, fg="white")} '
                   f'{click.style(level.upper(), fg=level_col)} '
                   f'{message}')
