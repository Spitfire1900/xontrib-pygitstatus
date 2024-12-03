import contextlib
import os
from collections import abc
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from git import Repo
from xonsh.built_ins import XonshSession
from xonsh.environ import Env
from xonsh.prompt.base import PromptFields, PromptFormatter
from xonsh.xontribs import xontribs_loaded

if TYPE_CHECKING:
    from xonsh.environ import Env

# test_gitstatus: https://github.com/xonsh/xonsh/blob/0.12.5/tests/prompt/test_gitstatus.py#L65


@pytest.fixture
def git_repo(tmpdir):
    Repo.init(tmpdir)
    assert isinstance(tmpdir, PathLike)
    yield tmpdir


@contextlib.contextmanager
def cd(path: PathLike):
    resource = Path(path)
    old_dir = Path.cwd()
    try:
        os.chdir(resource)
        yield
    finally:
        os.chdir(old_dir)


# def test_autoload(load_xontrib):
def test_autoload(xonsh_session: XonshSession):
    from xonsh.main import _autoload_xontribs
    _autoload_xontribs({})
    assert 'pygitstatus' in xontribs_loaded()


def test_untracked(git_repo):
    with cd(git_repo):
        # assert 'pygitstatus.untracked' in prompts
        Path('text.txt').touch()
        assert PromptFormatter()('{pygitstatus.untracked}') == '…1'
