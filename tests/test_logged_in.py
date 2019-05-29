import os
from tempfile import NamedTemporaryFile

import pytest


def test_login(cli):
    c = cli('login')


@pytest.mark.skip
def test_apps_fails(cli):
    c = cli('apps')
    assert c.status_code == 1


def test_apps(cli):
    c = cli('apps')
    print(c.out)
    assert False
    # assert c.return_code == 1
    # assert 'Please specify a template' in c.out
