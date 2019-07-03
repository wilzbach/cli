import json
import os
import sys
from tempfile import NamedTemporaryFile

from click.testing import CliRunner, Result

# import delegator

import pytest

STORYSCRIPT_CONFIG = {
    'id': os.environ.get('STORYSCRIPT_INT_CONF_USER_ID', 'my_user_id'),
    'access_token': os.environ.get('STORYSCRIPT_INT_CONF_ACCESS_TOKEN',
                                   'my_access_token'),
    'email': 'me@me.com'
}


@pytest.fixture
def pre_init_cli_runner():
    def wrapper(init_with_config_path='config.json',
                write_default_config=True):
        if write_default_config:
            with open(init_with_config_path, 'w') as f:
                f.write(json.dumps(STORYSCRIPT_CONFIG))
        from story import cli
        cli.init(config_path=init_with_config_path)

    return wrapper


@pytest.fixture
def runner(magic, pre_init_cli_runner):
    cli_runner = CliRunner()

    def function(command_function, stdin: str = None,
                 init_with_config_path='config.json',
                 write_default_config=True,
                 exit_code: int = 0,
                 args: list = []) -> Result:
        pre_init_cli_runner(init_with_config_path, write_default_config)

        result = cli_runner.invoke(
            command_function,
            input=stdin,
            args=args)

        if result.exception is not None \
                and not isinstance(result.exception, SystemExit):
            print(result.exc_info)
            # TODO: find a way to print the exception traceback
            # TODO: it's not straightforward
            assert False

        assert result.exit_code == exit_code, result.stdout
        return result

    out = magic()
    out.run = function
    out.runner = cli_runner
    return out


# @pytest.fixture
# def cli():
#     def function(*args, logged_in=True):
#
#         tf = NamedTemporaryFile().name
#
#         if logged_in:
#             # Create a temporary config file.
#             with open(tf, 'w') as f:
#                 f.write(json.dumps(STORYSCRIPT_CONFIG))
#
#         # Make temporary file.
#         args = ' '.join(args)
#         c = delegator.run(f'story {args}', env={'TOXENV': 'true',
#                                                 'STORY_CONFIG_PATH': tf})
#
#         os.remove(tf)
#         return c
#
#     return function


@pytest.fixture
def magic(mocker):
    """
    Shorthand for mocker.MagicMock. It's magic!
    """
    return mocker.MagicMock


@pytest.fixture
def patch_init(mocker):
    """
    Makes patching a class' constructor slightly easier
    """
    def patch_init(item):
        mocker.patch.object(item, '__init__', return_value=None)
    return patch_init


@pytest.fixture
def patch_many(mocker):
    """
    Makes patching many attributes of the same object simpler
    """
    def patch_many(item, attributes):
        for attribute in attributes:
            mocker.patch.object(item, attribute)
    return patch_many


@pytest.fixture
def patch(mocker, patch_init, patch_many):
    mocker.patch.init = patch_init
    mocker.patch.many = patch_many
    return mocker.patch


@pytest.fixture
def init_sample_app_in_cwd():
    def cb():
        with open('story.yml', 'w') as f:
            f.write('app_name: my_app\n')

        os.mkdir('src')
        os.mkdir('src/b')
        with open('src/a.story', 'w') as f:
            f.write('a = 1 + 0\n')

        with open('src/b/b.story', 'w') as f:
            f.write('b = 0 + 1\n')

    return cb


@pytest.fixture
def app_dir():
    pass
