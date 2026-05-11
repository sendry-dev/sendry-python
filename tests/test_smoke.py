from sendry import AsyncSendry, Sendry, SendryError, __version__


def test_version():
    assert isinstance(__version__, str)
    assert __version__.count(".") >= 2


def test_client_construct():
    client = Sendry("sn_live_test")
    assert client.emails is not None
    assert client.domains is not None


def test_async_client_construct():
    client = AsyncSendry("sn_live_test")
    assert client.emails is not None


def test_error_hierarchy():
    assert issubclass(SendryError, Exception)
