import pytest


def test_bare_apps(cli):
    c = cli('apps')
    assert 'Usage' in c.out
    # assert c.return_code == 1
    # assert 'Please specify a template' in c.out


def test_no_auth_apps_list_fails(cli):
    c = cli('apps list')
    assert c.status_code == 1
