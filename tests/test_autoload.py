import pytest
from xonsh.built_ins import XonshSession
from xonsh.xontribs import xontribs_loaded


@pytest.mark.forked  # this pollutes the pytest session
def test_autoload(xonsh_session: XonshSession):
    from xonsh.main import _autoload_xontribs

    _autoload_xontribs({})
    assert 'pygitstatus' in xontribs_loaded()
