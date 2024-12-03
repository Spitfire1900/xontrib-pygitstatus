import contextlib
import os
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from git import Repo
from xonsh.built_ins import XonshSession
from xonsh.environ import Env
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


def test_it_loads(load_xontrib):
    load_xontrib("pygitstatus")


@pytest.fixture(scope="module", autouse=True)
def xsh():
    from xonsh.built_ins import XSH  # Xonsh session singleton
    XSH.load()
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
def test_clean(xsh, git_repo, load_xontrib, xonsh_session):
    with cd(git_repo):
        Path('text.txt').touch()
        breakpoint()
        _ = prompts.pick("pygitstatus")
        print('')
