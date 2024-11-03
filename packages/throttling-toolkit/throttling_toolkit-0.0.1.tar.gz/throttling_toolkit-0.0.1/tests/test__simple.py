
from throttling_toolkit.simple import(
    ThrottlingError,
    throttle,
)


def test__basic():

    @throttle()
    def foo():
        pass
