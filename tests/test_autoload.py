import pytest
from xonsh.xontribs import xontribs_loaded


@pytest.fixture(scope="function", autouse=True)
def xsh_without_pygitstatus():
    from xonsh.built_ins import XSH

    XSH.load()
    yield XSH
    XSH.unload()


def test_autoload():
    from xonsh.main import _autoload_xontribs

    _autoload_xontribs({})
    assert 'pygitstatus' in xontribs_loaded()
