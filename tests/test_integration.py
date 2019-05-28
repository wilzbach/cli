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


@pytest.mark.parametrize(
    "story,expected",
    [
        ('http', 'http'),
        ('function', 'function'),
        ('if', 'if'),
        ('loop', 'for'),
        ('twitter', 'twitter'),
    ],
)
def test_write_specified_story(cli, story, expected):
    c = cli('write', story)
    assert expected in c.output
    assert c.exit_code == 0


def test_truth():
    assert True
