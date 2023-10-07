import pytest


class TestDouble:
    @pytest.mark.parametrize(
        "double, expected", [
            (1, 1),
            (2, 4),
            (3, 9),
            (5, 25)
        ], indirect=["double"]
    )
    def test_normal(self, double, expected):
        assert double == expected