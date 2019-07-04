# -*- coding: utf-8 -*-
import asyncio

from pytest import mark

from story import api, cli


@mark.parametrize('level', [None, 'info', 'debug', 'warning', 'error'])
@mark.parametrize('follow', [True, False])
@mark.parametrize('last', [10, 100, 4000, None])
@mark.parametrize('service,service_name', [
    (False, None),
    (True, None),
    (True, 'my_service'),
])
def test_logs_command(runner, init_sample_app_in_cwd, patch, level, follow,
                      last, service, service_name):
    patch.object(asyncio, 'get_event_loop')
    patch.object(cli, 'track')
    patch.object(api.Apps, 'get_uuid_from_hostname')

    args = []

    if service:
        args.append('-s')

    if service_name:
        args.append('-sn')
        args.append(service_name)

    if follow:
        args.append('-f')

    if level:
        args.append('-l')
        args.append(level)

    if last:
        args.append('-n')
        args.append(last)

    with runner.runner.isolated_filesystem():
        init_sample_app_in_cwd()

        from story.commands import logs
        patch.object(logs, 'connect_and_listen_with_retry')

        result = runner.run(logs.logs, args=args)

    assert 'Retrieving logs for my_app' in result.stdout

    api.Apps.get_uuid_from_hostname.assert_called_with('my_app')

    expected_service_name = 'N/A'
    if service:
        if service_name:
            expected_service_name = service_name
        else:
            expected_service_name = '*'

    cli.track.assert_called_with('App Logs Requested', {
        'App name': 'my_app',
        'Follow': 'Yes' if follow else 'No',
        'Last N': last if last else 10,
        'Source': 'Service' if service else 'Runtime',
        'Service Name': expected_service_name,
        'Minimum level': 'Info' if level is None else level.capitalize()
    })

    logs.connect_and_listen_with_retry.assert_called_with(
        api.Apps.get_uuid_from_hostname.return_value,
        last if last else 10,
        follow,
        service is False,
        service,
        '*' if service_name is None else service_name,
        'info' if level is None else level
    )

    asyncio.get_event_loop.return_value.run_until_complete.assert_called_with(
        logs.connect_and_listen_with_retry.return_value
    )
