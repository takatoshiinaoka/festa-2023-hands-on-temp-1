import pytest


@pytest.fixture(scope="function")
def double(request):
    num = request.param
    return num**2