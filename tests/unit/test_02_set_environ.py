import os

import pytest


@pytest.fixture(scope="function")
def set_environ(request):
    envs: dict = request.param

    for k, v in envs.items():
        os.environ[k] = v

    yield len(envs)

    for k in envs.keys():
        os.unsetenv(k)


class TestSetEnviron:
    @pytest.mark.parametrize(
        "set_environ, expected",
        [
            (
                {
                    "ENV_FIRST": "1st",
                    "ENV_SECOND": "2nd",
                    "ENV_THIRD": "3rd",
                },
                {
                    "ENV_FIRST": "1st",
                    "ENV_SECOND": "2nd",
                    "ENV_THIRD": "3rd",
                },
            ),
            (
                {
                    "ENV_FIRST": "first",
                    "ENV_SECOND": "second",
                    "ENV_THIRD": "third",
                },
                {
                    "ENV_FIRST": "first",
                    "ENV_SECOND": "second",
                    "ENV_THIRD": "third",
                },
            ),
        ],
        indirect=["set_environ"],
    )
    def test_normal(self, set_environ: int, expected: dict):
        assert set_environ == len(expected)
        for k, v in expected.items():
            assert os.getenv(k) == v