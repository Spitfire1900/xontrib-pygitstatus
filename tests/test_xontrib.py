import contextlib
import os
from collections import abc
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from git import Repo
from xonsh.built_ins import XonshSession
from xonsh.environ import Env
from xonsh.prompt.base import PromptFields
from xonsh.shell import Shell
from xonsh.xontribs import xontribs_loaded

if TYPE_CHECKING:
    from xonsh.environ import Env

# test_gitstatus: https://github.com/xonsh/xonsh/blob/0.12.5/tests/prompt/test_gitstatus.py#L65


@pytest.fixture
def prompts(xession: XonshSession):
    #
    print(type(xession.env))
    fields: Env
    fields = xession.env["PROMPT_FIELDS"]  # type: ignore reportAssignmentType
    yield fields
    fields.clear()


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


# @pytest.fixture(scope="module", autouse=True)
def xsh():
    from xonsh.__amalgam__ import _autoload_xontribs
    from xonsh.built_ins import XSH  # Xonsh session singleton
    # from xonsh.built_ins import XonshSession as XSH  # Xonsh session singleton
    from xonsh.environ import default_env

    # XSH.load(env=default_env())
    XSH.load()
    _autoload_xontribs({})

    # XSH.load(env=Env(default_env({'XONTRIBS_AUTOLOAD_DISABLED':
    #                               False})))  # has no effect
    # XSH.load(env=Env(default_env({'XONTRIBS_AUTOLOAD_DISABLED':
    #                               False})))  # has no effect
    xonsh_env: Env = XSH.env  # type: ignore reportAssignmentType
    xonsh_env['XONSH_SHOW_TRACEBACK'] = True
    shell: Shell = XSH.shell  # type: ignore reportAssignmentType
    from xontrib.pygitstatus import entrypoint
    entrypoint._load_xontrib_(XSH)
    xontib_list = shell.default(
        'xontrib list'
    )  # pytest --capture=no -k test_clean prints this: pygitstatus         loaded      manual
    _ = xontribs_loaded()
    breakpoint()
    yield XSH
    XSH.unload()


# def test_prompt_run(xsh_with_aliases: XonshSession):
# def test_clean(xsh, git_repo, load_xontrib, xonsh_session):
def test_untracked(git_repo, load_xontrib: abc.Callable[[str], None],
                   xonsh_session: XonshSession):
    with cd(git_repo):
        load_xontrib('pygitstatus')
        assert 'pygitstatus' in xontribs_loaded()
        xonsh_env: Env = xonsh_session.env  # type: ignore reportAssignmentType
        prompts: PromptFields = xonsh_env.get(
            'PROMPT_FIELDS')  # type: ignore reportAssignmentType
        assert 'pygitstatus.untracked' in prompts
        from xonsh.prompt.base import PromptFormatter
        Path('text.txt').touch()
        assert PromptFormatter()('{pygitstatus.untracked}') == '…1'
        # _ = prompts.pick("pygitstatus")
        # breakpoint()
        # print('')
