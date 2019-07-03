# -*- coding: utf-8 -*-
from unittest import mock

from story.helpers import datetime


def test_list(runner, patch, init_sample_app_in_cwd):
    patch.object(datetime, 'parse_psql_date_str', side_effect=[
        'my_app_1_parsed_date',
        'my_app_2_parsed_date'
    ])

    patch.object(datetime, 'reltime', side_effect=[
        'my_app_1_reltime',
        'my_app_2_reltime',
    ])

    ts_app_1 = '2019-06-26T10:31:22.499142+00:00'
    ts_app_2 = '2018-12-17T10:19:56.659736+00:00'

    with runner.runner.isolated_filesystem():
        init_sample_app_in_cwd()

        from story import api
        from story.commands.apps import apps
        patch.object(api.Apps, 'list',
                     return_value=[
                         {
                             'name': 'my_app_1',
                             'timestamp': ts_app_1,
                             'maintenance': False
                         },
                         {
                             'name': 'my_app_2',
                             'timestamp': ts_app_2,
                             'maintenance': True
                         },
                     ]
                     )

        args = ['list']
        result = runner.run(apps, args=args)

    expected_output = """
   NAME         STATE            CREATED     
============================================
my_app_1   running          my_app_1_reltime
my_app_2   in maintenance   my_app_2_reltime
    """  # noqa (because there's a trailing whitespace in the header)

    assert result.stdout.strip() == expected_output.strip()

    assert datetime.reltime.mock_calls == [
        mock.call('my_app_1_parsed_date'),
        mock.call('my_app_2_parsed_date')
    ]

    assert datetime.parse_psql_date_str.mock_calls == [
        mock.call(ts_app_1),
        mock.call(ts_app_2)
    ]


def test_list_no_apps(runner, patch, init_sample_app_in_cwd):
    with runner.runner.isolated_filesystem():
        init_sample_app_in_cwd()

        from story import api
        from story.commands.apps import apps
        patch.object(api.Apps, 'list', return_value=[])

        args = ['list']
        result = runner.run(apps, args=args)

    assert 'No application found' in result.stdout
    assert 'story apps create' in result.stdout
