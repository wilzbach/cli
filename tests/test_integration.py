import pytest
from click.testing import CliRunner

from story.main import cli as _cli


@pytest.fixture
def cli():
    def function(*args):
        r = CliRunner().invoke(_cli, list(args))
        return r

    return function


def test_write_no_story(cli):
    c = cli('write')
    assert c.exit_code == 1
    assert 'Please specify a template' in c.output


def test_write_specified_story(cli):
    c = cli('write', 'http')
    assert 'http' in c.output
    assert c.exit_code == 0


def test_truth():
    assert True
