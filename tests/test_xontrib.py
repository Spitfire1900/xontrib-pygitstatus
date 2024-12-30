# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# # pylint: disable=redefined-outer-name
import contextlib
import os
from collections import abc
from os import PathLike
from pathlib import Path
from typing import Any

import pytest
from git import Remote, RemoteReference, Repo
from xonsh.built_ins import XonshSession
from xonsh.environ import Env
from xonsh.prompt.base import PromptFields, PromptFormatter
from xonsh.xontribs import xontribs_loaded

# test_gitstatus: https://github.com/xonsh/xonsh/blob/0.12.5/tests/prompt/test_gitstatus.py#L65


@pytest.fixture
def git_repo(tmpdir):
    repo = Repo.init(tmpdir)
    assert isinstance(tmpdir, PathLike)
    yield repo


@contextlib.contextmanager
def cd(path: PathLike):
    resource = Path(path)
    old_dir = Path.cwd()
    try:
        os.chdir(resource)
        yield
    finally:
        os.chdir(old_dir)


@pytest.fixture(scope="function", autouse=True)
def prompts(load_xontrib: abc.Callable[[str], None],
            xonsh_session: XonshSession) -> abc.Generator[PromptFields, Any, Any]:
    load_xontrib('pygitstatus')
    assert 'pygitstatus' in xontribs_loaded()
    xonsh_env: Env = xonsh_session.env  # type: ignore reportAssignmentType
    prompts: PromptFields = xonsh_env.get(
        'PROMPT_FIELDS')  # type: ignore reportAssignmentType
    assert 'pygitstatus' in prompts
    yield prompts


def test_ahead(git_repo, tmp_path):
    with cd(git_repo.working_tree_dir):
        remote: Remote = git_repo.create_remote('origin', tmp_path)
        remote.fetch()
        git_repo.index.commit('initial commit')
        remote_ref = RemoteReference(
            git_repo, f'refs/remotes/origin/{git_repo.active_branch.name}')
        git_repo.active_branch.set_tracking_branch(remote_ref)
        remote.push()
        git_repo.index.commit('commit 2')
        assert PromptFormatter()('{pygitstatus.ahead}') == '↑·1'


def test_branch(git_repo):
    with cd(git_repo.working_tree_dir):
        git_repo.index.commit('initial commit')
        git_repo.create_head('test_branch')
        git_repo.git.checkout('test_branch')
        assert PromptFormatter()('{pygitstatus.branch}') == '{CYAN}test_branch'


def test_clean(git_repo):
    with cd(git_repo.working_tree_dir):
        assert PromptFormatter()('{pygitstatus.clean}') == '{BOLD_GREEN}✓{RESET}'


def test_untracked(git_repo):
    with cd(git_repo.working_tree_dir):
        Path('text.txt').touch()
        assert PromptFormatter()('{pygitstatus.untracked}') == '…1'
