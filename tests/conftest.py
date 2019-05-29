import pytest
import delegator


STORYSCRIPT_CONFIG = """
{"id": "30adbab9-ba60-4d55-a7d4-35a8e26c5e11", "access_token": "lKqGuAFYY9pOrS1Ts28jMw==", "name": "Kenneth Reitz", "email": "me@kennethreitz.com", "username": "kenneth-reitz", "beta": true}⏎
""".strip()


@pytest.fixture
def cli():
    def function(*args):
        args = ' '.join(args)
        return delegator.run(f'story {args}')

    return function


@pytest.fixture
def user_cli():
    def function(*args):
        args = ' '.join(args)
        return delegator.run(
            f'story {args}', env={"STORYSCRIPT_CONFIG": STORYSCRIPT_CONFIG}
        )

    return function
