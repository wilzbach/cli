# Storyscript CLI

[![Requires.io](https://img.shields.io/requires/github/storyscript/cli.svg?style=flat-square)](https://requires.io/github/storyscript/cli/requirements/?branch=master)
[![CircleCI](https://img.shields.io/circleci/project/github/storyscript/cli.svg?style=flat-square)](https://circleci.com/gh/storyscript/cli)
[![Codecov](https://img.shields.io/codecov/c/github/storyscript/cli.svg?style=flat-square)](https://codecov.io/gh/storyscript/cli)
[![PyPI](https://img.shields.io/pypi/v/storys.svg?style=flat-square)](https://pypi.org/project/storyscript/)
[![Snap Status](https://build.snapcraft.io/badge/storyscript/snapcraft.svg)](https://build.snapcraft.io/user/storyscript/snapcraft)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fstoryscript%2Fcli.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fstoryscript%2Fcli?ref=badge_shield)

The Storyscript CLI is used to manage Storyscript Cloud from the command line.

## Overview

The goals of this project is to provide a utility for developers to interact with all of Asyncy features/services.

## Installation

```shell
$ brew install storyscript/brew/storyscript
```

✨🍰✨

## Usage

Call `story` to get a full list of commands or continue to [read the documentation](https://docs.storyscript.io/cli).

![usage](https://user-images.githubusercontent.com/2041757/42899845-8fe6a3a4-8ac7-11e8-8545-a22f99563368.png)

## Issues

For problems directly related to the CLI, [add an issue on GitHub](https://github.com/storyscript/cli/issues/new).

For other issues, [submit a support ticket](mailto:support@asyncy.com)

[Contributors](https://github.com/storyscript/cli/contributors)

## Developing

Run
```sh
virtualenv venv --python=python3.7
source venv/bin/activate
pip install -r requirements.txt
TOXENV=true python -m story.main
```

Test
```sh
pip install tox
source venv/bin/activate
tox
```

Install
```sh
python setup.py install
asyncy
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fstoryscript%2Fcli.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fstoryscript%2Fcli?ref=badge_large)
