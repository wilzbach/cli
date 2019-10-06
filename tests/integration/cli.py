# -*- coding: utf-8 -*-
import sys

from story.cli import cli


def test_cli_as_module(spawn_process):
    # We don't need space-indents from docstrings
    output = str(cli.__doc__).replace("  ", " ").strip()

    # Python executable path on Windows should be quoted
    path = '"{}"' if sys.platform == "win32" else "{}"
    python = path.format(sys.executable)

    exit_code, stdout, stderr = spawn_process([python, "-m", "story"])

    assert exit_code == 0
    assert output in stdout
    assert "" in stderr
