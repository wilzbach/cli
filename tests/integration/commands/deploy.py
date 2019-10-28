# -*- coding: utf-8 -*-
import time

from pytest import mark


@mark.parametrize('with_message', [True, False])
@mark.parametrize('hard_deployment', [True, False])
@mark.parametrize('final_release_state', [
    'DEPLOYED', 'FAILED', 'UNKNOWN', 'TEMP_DEPLOYMENT_FAILURE'
])
@mark.parametrize('maintenance', [True, False])
@mark.parametrize('debug', [True, False])
@mark.parametrize('payload', [
    None, {'stories': {'foo'}, 'services': ['bar', 'baz']}
])
def test_deploy(runner, with_message, patch, hard_deployment,
                final_release_state, maintenance, payload,
                init_sample_app_in_cwd, debug):
    with runner.runner.isolated_filesystem():
        init_sample_app_in_cwd()

        # Relative imports are used here since we need to trigger
        # the cli init code in an isolated filesystem, inside an app dir.
        # Weird things happen otherwise. Not the most efficient way, but works.
        from story import api
        from story.commands import test
        from story.commands.deploy import deploy

        patch.object(test, 'compile_app', return_value=payload)
        patch.object(time, 'sleep')

        patch.object(api.Config, 'get')
        patch.object(api.Releases, 'create')
        patch.object(api.Releases, 'get', side_effect=[
            [{'state': 'QUEUED'}],
            [{'state': 'DEPLOYING'}],
            [{'state': final_release_state}],
        ])
        patch.object(api.Apps, 'maintenance', return_value=maintenance)

        args = []

        if with_message:
            message = 'hello world'
            args.append('--message')
            args.append(message)
        else:
            message = None

        if hard_deployment:
            args.append('--hard')

        if debug:
            args.append('--debug')

        if payload is None:
            result = runner.run(deploy, exit_code=1)
            assert result.stdout == ''
            return
        else:
            result = runner.run(deploy, exit_code=0, args=args)

        if maintenance:
            assert 'Your app is in maintenance mode.' in result.stdout
            return

        api.Config.get.assert_called_with('my_app')
        api.Releases.create.assert_called_with(
            api.Config.get(), payload, 'my_app', message, hard_deployment)

        assert time.sleep.call_count == 3

        test.compile_app.assert_called_with('my_app', debug=debug)

        if final_release_state == 'DEPLOYED':
            assert 'Configured 1 story' in result.stdout
            assert '- foo' in result.stdout
            assert 'Deployed 2 services' in result.stdout
            assert '- bar' in result.stdout
            assert '- baz' in result.stdout
            assert 'Created ingress route' in result.stdout
            assert 'Configured logging' in result.stdout
            assert 'Configured health checks' in result.stdout
            assert 'Deployment successful!' in result.stdout
        elif final_release_state == 'FAILED':
            assert 'Deployment failed!' in result.stdout
            assert 'story logs' in result.stdout
        elif final_release_state == 'TEMP_DEPLOYMENT_FAILURE':
            assert 'Deployment failed!' in result.stdout
            assert 'status.storyscript.io' in result.stdout
        else:
            assert f'An unhandled state of your app has been encountered ' \
                   f'- {final_release_state}' in result.stdout
            assert 'support@storyscript.io' in result.stdout
