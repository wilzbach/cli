import os
from tempfile import NamedTemporaryFile

import pytest
import delegator


STORYSCRIPT_CONFIG = """{
   "id":"cd3fb9d0-fc54-48c5-9a1a-9daead7da490",
   "access_token":"vmlLTkC+Q5lBJ0XU/OHVWA==",
   "name":null,
   "email":"kenneth+tests@storyscript.io",
   "username":"storyscript-cli-test",
   "beta":true
}""".strip()


@pytest.fixture
def cli():
    def function(*args):
        args = ' '.join(args)
        return delegator.run(f'story {args}')

    return function


@pytest.fixture
def user_cli():
    def function(*args):

        tf = NamedTemporaryFile().name
        # Make temporary file.
        args = ' '.join(args)
        c = delegator.run(f'story {args}', env={"STORY_CONFIG": tf})

        os.remove(tf)
        return c

    return function
